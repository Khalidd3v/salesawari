from django.shortcuts import render, redirect
from accounts.custom_login_required import superuser_required
from seller.models import *
from buyer.models import *
from django.shortcuts import get_object_or_404
from dashboard.models import *
from django.contrib import messages

@superuser_required
def dashboard(request):
    completed_orders = Order.objects.filter(is_confirmed='Completed')
    pending_orders = Order.objects.filter(is_confirmed='Pending')
    cancelled_orders = Order.objects.filter(is_confirmed='Cancelled')

    context = {
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'cancelled_orders': cancelled_orders
    }
    return render(request, 'dashboard/dashboard.html', context)



@superuser_required
def order_action(request):
    orders = Order.objects.filter(seller=request.user).order_by('-created_at')
    if request.method == 'POST':
        if 'order-action-form' in request.POST:
            try:
                order_id = request.POST.get('order-id')
                status = request.POST.get('order-option').capitalize()
                order = get_object_or_404(Order, id=order_id)
                previous_status = order.is_confirmed  # Track the previous status

                print(f"Order ID: {order_id}, Previous Status: {previous_status}, New Status: {status}")

                # Update the order status
                order.is_confirmed = status
                order.save()
                print(f"Order status updated to: {order.is_confirmed}")

                # Get the balance for the buyer or create if not exist
                balance, created = Balance.objects.get_or_create(user=order.buyer)
                if created:
                    print(f"Created new balance record for user {order.buyer}")
                print(f"Balance before update - Pending: {balance.pending}, Earnings: {balance.earnings}")

                if status == 'Cancel':
                    if previous_status == "Pending":
                        # Deduct the vehicle price from pending balance only if previously pending
                        balance.pending -= order.vehicle_price
                        print(f"Deducted {order.vehicle_price} from pending balance on cancel")
                        balance.save()
                    
                    # Reset vehicle sale status and delete sale history if it exists
                    Vehicle.objects.filter(id=order.vehicle.id).update(is_sold=False)
                    deleted_history, _ = SoldVehicleHistory.objects.filter(
                        vehicle=order.vehicle, buyer=order.buyer, seller=order.seller
                    ).delete()
                    print(f"Deleted history entries: {deleted_history}")
                
                elif status == 'Accept':
                    if previous_status == "Pending":
                        # Move the amount from pending to earnings
                        balance.pending -= order.vehicle_price
                        balance.earnings += order.vehicle_price
                        print(f"Transferred {order.vehicle_price} from pending to earnings on accept")
                        balance.save()
                        
                        # Mark vehicle as sold
                        Vehicle.objects.filter(id=order.vehicle.id).update(is_sold=True)
                        print("Vehicle marked as sold")

                        # Create a sale history entry if this is the first acceptance
                        SoldVehicleHistory.objects.create(
                            vehicle=order.vehicle,
                            buyer=order.buyer,
                            seller=order.seller,
                            sale_price=order.vehicle_price
                        )
                        print("Created SoldVehicleHistory entry")

                print(f"Balance after update - Pending: {balance.pending}, Earnings: {balance.earnings}")

                messages.success(request, f"{order.full_name}'s Order status updated successfully!")
                return redirect('order_action')

            except Exception as e:
                print("Error:", e)
                messages.error(request, f"Error: {str(e)}")
                return redirect('order_action')

    context = {
        "orders": orders,
    }
    return render(request, 'dashboard/order_action.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from accounts.custom_login_required import dynamic_login_required
from accounts.models import Account, UserProfile
from .custom_decorators import buyer_required
from chat.models import *
from seller.models import *
from dashboard.models import *
from .models import *
from django.contrib import messages
from django.db import transaction


@buyer_required
@dynamic_login_required
def buyer_dashboard(request):
    orders = Order.objects.filter(buyer=request.user)
    completed_orders_count = Order.objects.filter(buyer=request.user, is_confirmed="Completed")
    buyer_made_favorites = FavouriteVehicle.objects.filter(user=request.user)
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'buyer_made_favorites': buyer_made_favorites.count(),
        'conversations': conversations.count(),
        'completed_orders_count': completed_orders_count.count(),
        'orders_count': orders.count(),
        'orders': orders,
    }
    return render(request, 'buyer/buyer_dashboard.html', context)

@buyer_required
@dynamic_login_required
def buyer_chat_list_view(request):
    conversations = Conversation.objects.filter(participants=request.user)
    conversation_data = []
    for conversation in conversations:
        other_user = conversation.participants.exclude(id=request.user.id).first()
        if other_user:
            conversation_data.append({
                'conversation': conversation,
                'other_user': other_user,
            })

    context = {
        'conversation_data': conversation_data
    }
    return render(request, 'buyer/buyer_chat_list.html', context)



def buyer_conversation_view(request, user_id):
    other_user = get_object_or_404(Account, id=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    context = {
        'conversation_id': conversation.id,
        'other_user': other_user,
    }
    return render(request, 'buyer/conversation.html', context)

@buyer_required
@dynamic_login_required
def bargain(request, vehicle_id):
    buyer = request.user
    
    try:
        vehicle = Vehicle.objects.select_related('user').get(id=vehicle_id, is_sold=False)
    except Vehicle.DoesNotExist:
        messages.error(request, "Sorry, this vehicle is no longer available for bargaining!")
        return redirect('error_page')

    seller = vehicle.user
    existing_bargain = Bargain.objects.filter(vehicle=vehicle, buyer=buyer).first()

    if existing_bargain:
        bargain = existing_bargain
    else:
        bargain = Bargain.objects.create(seller=seller, vehicle=vehicle, buyer=buyer)

    if request.method == "POST":
        if "done-order" in request.POST:
            full_name = request.POST.get("full-name")
            email = request.POST.get("email-address")
            phone = request.POST.get("phone-number")
            cnic = request.POST.get("cnic")
            address = request.POST.get("address")
            card_number = request.POST.get("card-number")

            try:
                if int(card_number) != 1234567890:
                    messages.error(request, "Invalid card number!")
                    return redirect('bargain', vehicle_id)
            except ValueError:
                messages.error(request, "Card number should be a valid number!")
                return redirect('bargain', vehicle_id)

            try:
                with transaction.atomic():
                    order = Order.objects.create(
                        seller=seller,
                        buyer=buyer,
                        vehicle=vehicle,
                        vehicle_price=vehicle.price,
                        is_confirmed="Pending",
                        full_name=full_name,
                        email=email,
                        phone=phone,
                        cnic=cnic,
                        address=address
                    )
                    vehicle.is_sold = True
                    vehicle.save()
                    bargain.delete()
                return redirect('invoice', order.id)
            except Exception as e:
                print("Error : ", e)
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            bargain.delete()
            messages.success(request, "Cleared Bargain Page successfully!")
            return redirect('bargain', vehicle_id)

    context = {
        'vehicle': vehicle,
        'seller': seller,
        'buyer': buyer,
        'bargain': bargain
    }
    return render(request, 'landingpage/bargain.html', context)


@buyer_required
@dynamic_login_required
def fav_vehicles(request):
    fav = FavouriteVehicle.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'buyer/fav_vehicles.html', {'fav': fav})


@buyer_required
@dynamic_login_required
def my_orders(request):
    completed_orders = Order.objects.filter(is_confirmed='Completed')
    pending_orders = Order.objects.filter(is_confirmed='Pending')
    cancelled_orders = Order.objects.filter(is_confirmed='Cancelled')

    context = {
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'cancelled_orders': cancelled_orders
    }
    return render(request, 'buyer/my_orders.html', context)


@buyer_required
@dynamic_login_required
def invoice(request, order_id):
    order_item = Order.objects.get(id=order_id)
    return render(request, 'buyer/invoice.html', {'order_item': order_item})

@buyer_required
@dynamic_login_required
def buyer_profile(request):
    if request.method == "POST":
        if "profile_image_form" in request.POST:
                    image = request.FILES.get('image')
                    if image:
                        profile, created = UserProfile.objects.get_or_create(user=request.user)
                        profile.profile_picture = image
                        profile.save()
                        messages.success(request, "Profile updated!")
                    else:
                        messages.error(request, "Profile image not found!")
                    return redirect('buyer_profile')

        elif "account_details_form" in request.POST:
            full_name = request.POST.get('full_name')
            username = request.POST.get('username', '').lower()
            phone_number = request.POST.get('phone_number')
            email_address = request.POST.get('email_address', '').lower()

            errors = []

            if not full_name:
                errors.append("Full name is required!")
            if not username:
                errors.append("Username is required!")
            elif Account.objects.filter(username=username).exclude(id=request.user.id).exists():
                errors.append("This Username already exists!")
            if not phone_number:
                errors.append("Phone number is required!")
            elif Account.objects.filter(phone=phone_number).exclude(id=request.user.id).exists():
                errors.append("This phone number already exists!")
            if not email_address:
                errors.append("Email address is required!")
            elif Account.objects.filter(email=email_address).exclude(id=request.user.id).exists():
                errors.append("This email address already exists!")

            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                user = Account.objects.get(id=request.user.id)
                user.full_name = full_name
                user.username = username
                user.phone = phone_number
                user.email = email_address
                user.save()
                messages.success(request, "Account details updated successfully!")
            return redirect('buyer_profile')

        elif "account_security_form" in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if current_password:
                user = Account.objects.get(id=request.user.id)
                if user.check_password(current_password):
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        messages.success(request, "Password updated successfully!")
                    else:
                        messages.error(request, "New passwords do not match!")
                else:
                    messages.error(request, "Current password is incorrect!")
            else:
                messages.error(request, "Current password is required!")
            return redirect('buyer_profile')

    return render(request, 'buyer/buyer_profile.html')
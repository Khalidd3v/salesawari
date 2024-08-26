# views.py
from rest_framework import status, permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from buyer.models import FavouriteVehicle

class FavouriteVehicleToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        user = request.user
        vehicle_id = request.data.get('vehicle_id')
        try:
            if not vehicle_id:
                return Response({'status': 'error', 'message' : 'Vehicle ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                fav = FavouriteVehicle.objects.get(user=user, vehicle_id=vehicle_id)
                fav.delete()
                fav_count = FavouriteVehicle.objects.filter(vehicle_id=vehicle_id).count()
                return Response({'status': 'success', 'message' : 'Removed from Favorite.', 'fav_count': fav_count}, status=status.HTTP_200_OK)
            except FavouriteVehicle.DoesNotExist:
                FavouriteVehicle.objects.create(user=user, vehicle_id=vehicle_id)
                fav_count = FavouriteVehicle.objects.filter(vehicle_id=vehicle_id).count()
                return Response({'status': 'success', 'message' : 'Added from Favorite.', 'fav_count': fav_count}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'message' : f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

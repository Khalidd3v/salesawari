# views.py
from rest_framework import status, permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from buyer.models import FavouriteVehicle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from chat.models import *
from django.shortcuts import get_object_or_404, render
from .serializers import *

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


class SendMessageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get('conversation_id')
        content = request.data.get('content')
        
        if not conversation_id or not content:
            return Response({'error': 'Conversation ID and content are required'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FetchMessagesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response({'error': 'Conversation ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
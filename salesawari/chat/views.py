# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from django.contrib.auth import get_user_model
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from .models import *
# from accounts.models import Account

# User = get_user_model()

# @login_required
# def conversation_view(request, user_id):
#     other_user = get_object_or_404(User, id=user_id)
#     conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

#     if not conversation:
#         conversation = Conversation.objects.create()
#         conversation.participants.add(request.user, other_user)

#     context = {
#         'conversation_id': conversation.id,
#         'other_user': other_user,
#     }
#     return render(request, 'chat/conversation.html', context)


# def chat_list_view(request):
#     # Fetch all conversations where the logged-in user is a participant
#     conversations = Conversation.objects.filter(participants=request.user)

#     context = {
#         'conversations': conversations
#     }
#     return render(request, 'chat/chat_list.html', context)

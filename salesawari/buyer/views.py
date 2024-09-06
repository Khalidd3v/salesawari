from django.shortcuts import render, get_object_or_404
from accounts.custom_login_required import dynamic_login_required
from accounts.models import Account
from .custom_decorators import buyer_required
from chat.models import *

@buyer_required
@dynamic_login_required
def buyer_dashboard(request):
    return render(request, 'buyer/buyer_dashboard.html')


@buyer_required
@dynamic_login_required
def buyer_profile(request):
    return render(request, 'buyer/buyer_profile.html')

def buyer_chat_list_view(request):
    conversations = Conversation.objects.filter(participants=request.user)
    conversation_data = []
    for conversation in conversations:
        # Exclude the buyer (current user) to get the seller
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
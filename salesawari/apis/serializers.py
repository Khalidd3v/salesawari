from rest_framework import serializers
from chat.models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    sender_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'timestamp', 'sender_profile_picture']

    def get_sender_username(self, obj):
        return obj.sender.username

    def get_sender_profile_picture(self, obj):
        sender = obj.sender
        if hasattr(sender, 'userprofile') and sender.userprofile.profile_picture:
            return sender.userprofile.profile_picture.url
        return None


class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    other_participant = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'other_participant', 'last_message', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return MessageSerializer(last_message).data if last_message else None

    def get_other_participant(self, obj):
        request = self.context.get('request')
        other_user = obj.participants.exclude(id=request.user.id).first()
        if other_user:
            profile_picture = other_user.profile.profile_picture.url if hasattr(other_user, 'profile') and other_user.profile.profile_picture else None
            return {
                'id': other_user.id,
                'username': other_user.username,
                'profile_picture': profile_picture
            }
        return None
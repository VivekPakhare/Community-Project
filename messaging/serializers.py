from rest_framework import serializers
from .models import Conversation, Message, Report


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_name', 'text', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    participant_names = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participant_names', 'product', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return {'text': msg.text, 'sender': msg.sender.username, 'created_at': msg.created_at}
        return None

    def get_participant_names(self, obj):
        return [u.username for u in obj.participants.all()]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'reported_user', 'product', 'reason', 'description', 'is_resolved', 'created_at']
        read_only_fields = ['id', 'reporter', 'is_resolved', 'created_at']

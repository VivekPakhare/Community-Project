from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from rest_framework import generics, permissions

from accounts.models import User
from .models import Conversation, Message, Report
from .serializers import ConversationSerializer, MessageSerializer, ReportSerializer


# --- Template Views ---

@login_required
def conversation_list_view(request):
    conversations = request.user.conversations.all()
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_detail_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in conversation.participants.all():
        django_messages.error(request, "Access denied.")
        return redirect('messaging:list')

    # Mark messages as read
    conversation.messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
            conversation.save()  # update the updated_at timestamp
            return redirect('messaging:detail', pk=pk)

    msgs = conversation.messages.all()
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages_list': msgs,
    })


@login_required
def start_conversation_view(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('messaging:list')

    product_id = request.GET.get('product')

    # Check for existing conversation between these users about this product
    conversations = Conversation.objects.filter(participants=request.user).filter(participants=other_user)
    if product_id:
        conversations = conversations.filter(product_id=product_id)

    conversation = conversations.first()
    if not conversation:
        from products.models import Product
        conversation = Conversation.objects.create(
            product_id=product_id if product_id else None
        )
        conversation.participants.add(request.user, other_user)

    return redirect('messaging:detail', pk=conversation.pk)


@login_required
def report_create_view(request):
    if request.method == 'POST':
        reported_user_id = request.POST.get('reported_user')
        product_id = request.POST.get('product')
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        Report.objects.create(
            reporter=request.user,
            reported_user_id=reported_user_id if reported_user_id else None,
            product_id=product_id if product_id else None,
            reason=reason,
            description=description,
        )
        django_messages.success(request, 'Report submitted. We will review it shortly.')
        return redirect('home')
    return render(request, 'messaging/report_form.html')


# --- API Views ---

class ConversationListAPIView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all()


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation = get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])
        return conversation.messages.all()

    def perform_create(self, serializer):
        conversation = get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])
        serializer.save(sender=self.request.user, conversation=conversation)

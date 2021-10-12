from django.shortcuts import render
from rest_framework import generics
from django.http.response import Http404
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse, Http404
from rest_framework.permissions import IsAuthenticated
from ..serializer import MessageSerializer, MessageDataSerializer
from ..models import Message
from coach.models import Coach
from customer.decorator import check_role_permission
from rest_framework.parsers import JSONParser
from customer.models import Student, User, Role, Customer
from customer.serializer import UserDataSerializer
from django.db.models import Q
from dateutil import parser
import datetime
from first_kick_management.settings import logger


class ChatView(generics.GenericAPIView):
    def get(self, request):
        login = True if "login" in request.session else False
        return render(request, 'chat/chat.html', {"login": login})


class ChatUsers(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_serializer = UserDataSerializer(User.objects.filter(
                role_id__in=Role.objects.filter(name__in=["Management", "Super User", "Coach Manager", "Head Coach"]).values('id')
            ).exclude(email=request.user.email), many=True)
            return JsonResponse({"message": "list of users", "data": user_serializer.data, "user": request.user.id}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class MessagesView(generics.GenericAPIView):
    def get(self, request, sender, receiver):
        login = True if "login" in request.session else False
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(pk=sender),
                       'receiver': User.objects.get(id=receiver),
                       "login": login})


class MessageDataView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get(self, request, sender, receiver):
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver) | Message.objects.filter(sender_id=receiver, receiver_id=sender)
        serializer = MessageDataSerializer(messages, many=True)
        return JsonResponse({"message": "list of all messages", "data": serializer.data, "user": request.user.id}, safe=False, status=200)


class MessagesListView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get(self, request, sender, receiver):
        """
        List all required messages, or create a new message.
        """
        messages = Message.objects.filter(sender_id=receiver, receiver_id=sender, is_read=False)
        serializer = MessageDataSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        # data = JSONParser().parse(request)
        serializer = MessageDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sender'] = User.objects.get(pk=request.data['sender_id'])
            serializer.validated_data['receiver'] = User.objects.get(pk=request.data['receiver_id'])
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class InboxDataView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageDataSerializer

    def get(self, request):
        sender_messages = Message.objects.filter(sender=request.user).values('id','message','receiver')
        receivers = list({item['receiver']: item for item in sender_messages}.values())
        serializer = MessageDataSerializer(
            Message.objects.filter(pk__in=[item['id'] for item in receivers]), many=True)
        return JsonResponse({"message": "get message", "data": serializer.data}, safe=False)


class ChatHistoryView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageDataSerializer

    def get(self, request, sender, receiver):
        try:
            today = datetime.datetime.now().date()
            previous_day = today - datetime.timedelta(days=1)
            first_previous_month = today - datetime.timedelta(days=30)
            second_previous_month = today - datetime.timedelta(days=60)

            previous_day_chat = Message.objects.filter(
                                Q(sender=request.user) & Q(receiver_id=receiver) & Q(timestamp__date=previous_day)).first()
            first_previous_month_chat = Message.objects.filter(Q(sender=request.user) & Q(receiver_id=receiver) & Q(timestamp__date__gte=first_previous_month) & Q(timestamp__date__lte=previous_day)).first()
            second_previous_month_chat = Message.objects.filter(Q(sender=request.user) & Q(receiver_id=receiver) & Q(timestamp__date__gt=second_previous_month) & Q(timestamp__date__lt=previous_day)).first()
            previous_day_serializer = MessageDataSerializer(previous_day_chat)
            first_previous_month_serializer = MessageDataSerializer(first_previous_month_chat)
            second_previous_month_serializer = MessageDataSerializer(second_previous_month_chat)

            previous_day = previous_day.strftime("%d %b %Y At %I:%M %p")
            first_previous_month = first_previous_month.strftime("%d %b %Y At %I:%M %p")
            second_previous_month = second_previous_month.strftime("%d %b %Y At %I:%M %p")

            return JsonResponse({"message": "get message", "data":
                {previous_day: previous_day_serializer.data,
                                 first_previous_month: first_previous_month_serializer.data,
                                 second_previous_month: second_previous_month_serializer.data}}, safe=False)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

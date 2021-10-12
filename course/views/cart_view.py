from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse, Http404
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from decimal import Decimal
from ..serializer import (CourseDetailSerializer, CourseLocationSerializer,
                         BookCourseDetailSerializer, EventSerializer,
                         NotificationSerializer, UserAttendanceSerializer,
                         CourseDataTableSerializer, BookCourseSerializer,
                         CourseListingDataSerializer, AccountRecordKeepingSerializer, CartSerializer,CartItemSerializer)
from ..models import (CourseDetail, CourseLocation, CourseMonths, Events,
                     Notification, BookCourseDetail, UserAttendance, AccountRecordKeeping,
                     query_course_by_args, query_courses_booked_by_args, Cart, CartItem)
from master.models import Location
from customer.decorator import check_role_permission
from first_kick_management.settings import logger
from django.db.models import F


class AddToCartView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get cart items
        """
        try:
            cart = Cart.objects.get(created_by=request.user)
            serializer = CartItemSerializer(CartItem.objects.filter(cart=cart, purchased=False), many=True)
            return JsonResponse({"message": "list of item in the cart", "data": serializer.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)

    def post(self, request):
        """
        Add items to cart
        """
        try:
            if Cart.objects.filter(created_by=request.user).exists():
                cart = Cart.objects.get(created_by=request.user)
            else:
                cart = Cart.objects.create(
                    created_by=request.user
                )
            CartItem.objects.create(
                cart=cart,
                location=CourseLocation.objects.get(pk=request.data['location']),
                course=CourseDetail.objects.get(pk=request.data['course']),
                # month=request.data['month'],
                amount=request.data['amount']
            )
            total_amount = CartItem.objects.filter(cart=cart).aggregate(Sum('amount'))
            cart.total = Decimal(total_amount['amount__sum'])
            cart.save()
            return JsonResponse({"message": "item added to the cart"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class UpdateCartView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            course_ids = request.POST.getlist("product['id'][]")
            qty = request.POST.getlist("product['qty'][]")
            for key, value in enumerate(course_ids):
                cart_item = CartItem.objects.get(pk=value)
                cart_item.purchased_qty = qty[key]
                cart_item.purchased = True
                cart_item.save()
            return JsonResponse({"message": "updated cart details"}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class CoursesPurchasedView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            cart = Cart.objects.get(created_by=request.user)
            cart_items = CartItemSerializer(CartItem.objects.filter(cart=cart, purchased_qty__gt=F('booked_qty')), many=True)
            return JsonResponse({"message": "courses purchased", "data": cart_items.data}, status=200)
        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)


class DeleteCartItem(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        """
        Delete cart item
        """
        try:
            cart_item = self.get_object(pk)
            if cart_item:
                cart_item.delete()
                message = "Cart item deleted successfully"
                return JsonResponse({'message': message}, status=200)
            return JsonResponse({'message': "Cart item not found"}, status=401)

        except Exception as e:
            logger.error(e, exc_info=True)
            return JsonResponse({"message": "Something went wrong, please contact admin"}, status=500)
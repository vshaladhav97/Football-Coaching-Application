from django.db.models import manager
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import HttpResponse, JsonResponse
from ..serializer import CustomerSerializer, PaymentSerializer
from ..models import Customer, Payment
import string
import random
from .payment_crypt import decrypted_data, encrypted_data_url
from django.shortcuts import redirect
from first_kick_management.settings import logger
from django.shortcuts import render
from ..config import payments_variables

vendor_email = payments_variables.VendorEMail


def random_id_generation(length=16):
    randomstr = ''.join(random.choices(
        string.ascii_letters+string.digits, k=length))
    return randomstr


def save_payment_data(self, request, data):
    # print(data)
    if 'customer_id' in data:
        customer_id = data['customer_id']
    else:
        customer_id = data['customer']
    if 'amount' in data:
        amount = data['amount']
    else:
        amount = data['total_cost']
    discount_amount = 0
    total_amount = format(amount + discount_amount,".2f")
    currency = "GBP"
    if 'description' in data:
        description = data['description']
    else:
        description = "test"
    vendor_tx_code = "firstkickmanage_"+random_id_generation()

    raw_data = {"payment_id": vendor_tx_code, "amount": amount, "discount_amount": discount_amount, "tax": 0, "total_amount": total_amount, "currency": "GBP",
                "status": "SENT_TO_PG", "description": "test", "Payment_gateway_reference_id": "", "Payment_gateway_response_text": "", "customer": customer_id}
    serializer = PaymentSerializer(data=[raw_data], many=True)

    if serializer.is_valid():
        serializer.save()
    else:
        logger.error(serializer.errors)
        return False

    customer = list(Customer.objects.filter(id=customer_id).values())[0]
    callback_url = '{}://{}/payment_response?description={}&customer={}'.format(
        request.scheme, request.META['HTTP_HOST'], '|'.join(description.split(' ')), customer_id)
    # print(callback_url)

    basket_data = 'VendorTxCode={VendorTxCode}&Amount={Amount}&Currency={Currency}&Description={Description}&BillingSurname={BillingSurname}&BillingFirstnames={BillingFirstnames}&BillingAddress1={BillingAddress1}&BillingCity={BillingCity}&BillingPostCode={BillingPostCode}&BillingCountry={BillingCountry}&DeliverySurname={DeliverySurname}&DeliveryFirstnames={DeliveryFirstnames}&DeliveryAddress1={DeliveryAddress1}&DeliveryCity={DeliveryCity}&DeliveryPostCode={DeliveryPostCode}&DeliveryCountry={DeliveryCountry}&CustomerEMail={CustomerEMail}&SuccessURL={SuccessURL}&FailureURL={FailureURL}&SendEmail=1&COFUsage=FIRST&InitiatedType=CIT&MITType=UNSCHEDULED&VendorEMail={VendorEMail}'.format(
        VendorTxCode=vendor_tx_code, Amount=total_amount, Currency=currency, Description=description, BillingSurname=customer["last_name"], BillingFirstnames=customer['first_name'], BillingAddress1=customer['address'], BillingCity=customer['town'], BillingPostCode=customer['postal_code'], BillingCountry=customer['country_code'], DeliverySurname=customer['last_name'], DeliveryFirstnames=customer['first_name'], DeliveryAddress1=customer['address'], DeliveryCity=customer['town'], DeliveryPostCode=customer['postal_code'], DeliveryCountry=customer['country_code'], CustomerEMail=customer['email'], SuccessURL=callback_url, FailureURL=callback_url, VendorEMail=vendor_email)
    print(basket_data)
    get_payment_request_url = encrypted_data_url(basket_data)
    logger.info(get_payment_request_url)
    response = {
        'payment': serializer.data[0]['id'], 'url': get_payment_request_url}

    return response


class SubmitPaymentRequest(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def post(self, request):
        print(request.user)
        customer_id = 3
        amount = 50
        discount_amount = 0
        total_amount = amount + discount_amount
        currency = "GBP"
        description = "test payment"
        vendor_tx_code = "firstkickmanage_"+random_id_generation()

        raw_data = {"payment_id": vendor_tx_code, "amount": amount, "discount_amount": discount_amount, "tax": 0, "total_amount": total_amount, "currency": "GBP",
                    "status": "SENT_TO_PG", "description": "test", "Payment_gateway_reference_id": "", "Payment_gateway_response_text": "", "customer": customer_id}
        serializer = PaymentSerializer(data=[raw_data], many=True)

        if serializer.is_valid():
            serializer.save()
        else:
            logger.error(serializer.errors)

        customer = list(Customer.objects.filter(id=customer_id).values())[0]
        callback_url = '{}://{}/payment_response?description={}&customer={}'.format(
            request.scheme, request.META['HTTP_HOST'], '|'.join(description.split(' ')), customer_id)
        # print(callback_url)

        basket_data = 'VendorTxCode={VendorTxCode}&Amount={Amount}&Currency={Currency}&Description={Description}&BillingSurname={BillingSurname}&BillingFirstnames={BillingFirstnames}&BillingAddress1={BillingAddress1}&BillingCity={BillingCity}&BillingPostCode={BillingPostCode}&BillingCountry={BillingCountry}&DeliverySurname={DeliverySurname}&DeliveryFirstnames={DeliveryFirstnames}&DeliveryAddress1={DeliveryAddress1}&DeliveryCity={DeliveryCity}&DeliveryPostCode={DeliveryPostCode}&DeliveryCountry={DeliveryCountry}&CustomerEMail={CustomerEMail}&SuccessURL={SuccessURL}&FailureURL={FailureURL}&SendEmail=1&COFUsage=FIRST&InitiatedType=CIT&MITType=UNSCHEDULED'.format(
            VendorTxCode=vendor_tx_code, Amount=amount, Currency=currency, Description=description, BillingSurname=customer["last_name"], BillingFirstnames=customer['first_name'], BillingAddress1=customer['address'], BillingCity=customer['town'], BillingPostCode=customer['postal_code'], BillingCountry=customer['country_code'], DeliverySurname=customer['last_name'], DeliveryFirstnames=customer['first_name'], DeliveryAddress1=customer['address'], DeliveryCity=customer['town'], DeliveryPostCode=customer['postal_code'], DeliveryCountry=customer['country_code'], CustomerEMail=customer['email'], SuccessURL=callback_url, FailureURL=callback_url)
        # print(basket_data)
        get_payment_request_url = encrypted_data_url(basket_data)
        # print(get_payment_request_url)

        return JsonResponse({'url': get_payment_request_url}, status=200)


def create_response_dict(split_response, response_dict):
    """Prepare dictionary of payment response"""

    for res in split_response:
        split_sub_response = res.split('=')
        if split_sub_response[0] == "VendorTxCode":
            response_dict['payment_id'] = split_sub_response[1]
        if split_sub_response[0] == "VPSTxId":
            response_dict['Payment_gateway_reference_id'] = split_sub_response[1][1:-1]
        if split_sub_response[0] == "Status":
            if split_sub_response[1] == "OK" or split_sub_response[1] == "ABORT":
                response_dict['status'] = split_sub_response[1]
            else:
                response_dict['status'] = "FAILED"
        if split_sub_response[0] == "Amount":
            response_dict['Amount'] = split_sub_response[1]


class DecryptionOfPayment(generics.GenericAPIView):
    """Decryption of payment from response"""

    serializer_class = Payment

    def get(self, request):

        try:
            response_dict = {}

            if 'crypt' in request.GET:
                # print(request.GET['crypt'])
                response = decrypted_data(request.GET['crypt'][1:])
                response_dict['Payment_gateway_response_text'] = response
                split_response = response.split('&')
                create_response_dict(split_response, response_dict)

            if 'description' in request.GET:
                response_dict['description'] = ' '.join(
                    request.GET['description'].split('|'))

            if 'customer' in request.GET:
                response_dict['customer'] = request.GET['customer']

            payment = Payment.objects.get(
                payment_id=response_dict['payment_id'])

            serializer = PaymentSerializer(payment, data=response_dict)

            if serializer.is_valid():
                serializer.update(payment, response_dict)
            else:
                logger.error(serializer.errors)

            return render(request, 'payment/payment_success.html', {"details": response_dict})

        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, '404-error-page.html')

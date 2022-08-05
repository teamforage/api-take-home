# See the fixtures/ directory for examples of the request bodies
# needed to create objects using the ListCreateAPIViews below.

from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Payment, CreditCard, Order
from api.serializers import PaymentSerializer, CreditCardSerializer, OrderSerializer
from processor import processPayment

class ListCreateCreditCard(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/credit_cards/ <- returns a list of all CreditCard objects
    2. POST http://localhost:8000/api/credit_cards/ <- creates a single CreditCard object and returns it

    """
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class RetrieveDeleteCreditCard(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/credit_cards/:id/ <- returns a CreditCard object provided its id.
    2. DELETE http://localhost:8000/api/credit_cards/:id/ <- deletes a CreditCard object by id.

    """
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class ListCreateOrder(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/orders/ <- returns a list of all Order objects
    2. POST http://localhost:8000/api/ordersr/ <- creates a single Order object and returns it

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class RetrieveDeleteOrder(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/orders/:id/ <- returns an Order object provided its id.
    2. DELETE http://localhost:8000/api/orders/:id/ <- deletes an Order object by id.

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ListCreatePayment(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/payments/ <- returns a list of all Payment objects
    2. POST http://localhost:8000/api/payments/ <- creates a single Payment object and associates it with the Order in the request body.

    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class RetrieveDeletePayment(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/payments/:id/ <- returns a Payment object provided its id.
    2. DELETE http://localhost:8000/api/payments/:id/ <- deletes a Payment object by id.

    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CaptureOrder(APIView):
    """ Provided an Order's id, submit all associated payments to the payment processor.

    Payments will change status to either failed or succeeded, depending on the
    response from the payment processor.

    Once all payments have been processed, the status of the Order object will be updated
    to 'suceeded' if all of the payments were successful or 'failed' if at least one payment
    was not successful.
    """

    def post(self, request, id):
        try:
            order_obj = Order.objects.get(id=id) # throws if order_id not found

            # Find all Payments associated with this Order via /api/payments/
            payment_queryset = Payment.objects.filter(order__id=id)

            # Payments must satisfy the order_total
            total_payment_amount = sum([x.amount for x in payment_queryset])
            if total_payment_amount != order_obj.order_total:
                return Response({
                    "error_message": "Payment total does not match order total for Order with id {}".format(id)
                }, status=status.HTTP_400_BAD_REQUEST)

            potential_errors = []
            for payment in payment_queryset:
                potential_error = processPayment(payment)

                if potential_error:
                    potential_errors.append(potential_error)

            if potential_errors:
                order_obj.status = Order.TYPE_FAILED
            else:
                order_obj.status = Order.TYPE_SUCCEEDED
                order_obj.success_date = timezone.now()

            order_obj.save() # write status back to database

            return Response(
                OrderSerializer(order_obj).data
            )

        except Order.DoesNotExist:
            return Response({
                "error_message": "Unable to find Order with id {}".format(id)
            }, status=status.HTTP_404_NOT_FOUND)

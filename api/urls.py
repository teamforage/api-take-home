from django.urls import path

from api import views


app_name = "api"

urlpatterns = [
    path(
        "credit_cards/",
        views.ListCreateCreditCard.as_view(),
        name="credit-cards-list-create",
    ),
    path(
        "credit_cards/<int:pk>/",
        views.RetrieveDeleteCreditCard.as_view(),
        name="credit-cards-retrieve-delete",
    ),
    path(
        "orders/",
        views.ListCreateOrder.as_view(),
        name="orders-list-create",
    ),
    path(
        "orders/<int:pk>/",
        views.RetrieveDeleteOrder.as_view(),
        name="orders-retrieve-delete",
    ),
    path(
        "payments/",
        views.ListCreatePayment.as_view(),
        name="payments-list-create",
    ),
    path(
        "payments/<int:pk>/",
        views.RetrieveDeletePayment.as_view(),
        name="payments-retrieve-delete",
    ),
    path(
        "orders/<int:id>/capture/", 
        views.CaptureOrder.as_view(), 
        name="orders-capture"
    ),
]

from django.urls import path
from .views import ItemDetailView, create_checkout_session

urlpatterns = [
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item"),
    path("buy/<int:pk>/", create_checkout_session, name="buy"),
]
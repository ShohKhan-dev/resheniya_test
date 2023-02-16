from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import stripe
from .models import Item

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

class ItemDetailView(TemplateView):
    template_name = "item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, pk=self.kwargs["pk"])
        context["item"] = item
        context["stripe_public_key"] = "pk_test_a9nwZVa5O7b0xz3lxl318KSU00x1L9ZWsF"
        return context

@csrf_exempt
def create_checkout_session(request, **kwargs):
    item = get_object_or_404(Item, pk=kwargs["pk"])
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": item.price,
                        "product_data": {"name": item.name},
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/cancel",
        )
    
        return JsonResponse({"sessionId": checkout_session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)})

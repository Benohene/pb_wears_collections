from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


"""
* is used to calculate the total amount of items in the cart, the total cost of the items in the cart, the delivery cost, and the grand total. 
* It is then used in the cart view, and the add_to_cart view. 
* The cart_contents function is also used in the context_processors.py file, which allows the cart to be available on every page of the site.
"""


def cart_contents(request):
    """A view that renders the cart contents page"""
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get("cart", {})

    # If the item has no size
    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            cart_items.append(
                {
                    "item_id": item_id,
                    "quantity": item_data,
                    "product": product,
                }
            )
        else:
            # If the item has a size
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data["items_by_size"].items():
                total += quantity * product.price
                product_count += quantity
                cart_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                    }
                )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(
            settings.STANDARD_DELIVERY_PERCENTAGE / 100
        )
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context

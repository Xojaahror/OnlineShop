from .models import Category
from apps.order.models import Wishlist, Cart
def main_data(request):
    categories = Category.objects.filter(parent=None, is_active=True)
    wishlist = []
    cart = []
    # print(request.user)
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        cart = Cart.objects.filter(user=request.user, status = 'active').first()
        # print(cart)
    context = {
        'categories' : categories,
        'wishlist' : wishlist,
        'cart' : cart,
    }
    return context
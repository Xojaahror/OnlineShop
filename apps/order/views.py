from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from apps.home.models import Product
from .models import Wishlist, Cart, CartItem
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreateWishlistView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        # print(url, "\n#################################")
        product = Product.objects.get(uuid=uuid)
        user = request.user
        if Wishlist.objects.filter(user=user, product=product):
            messages.info(request, "Product already in your wishlist!")
        else:
            Wishlist.objects.create(product=product, user=user)
            messages.success(request, "Product added to your wishlist!")

        if url:
            return redirect(url)
        else:
            return redirect('/')

class CreateCartView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        product = Product.objects.get(uuid=uuid)
        user = request.user
        if Cart.objects.filter(user=user, is_active=True, status='active'):
            cart = Cart.objects.get(user=user)
            if CartItem.objects.filter(product=product, cart=cart):
                messages.info(request, 'product already in your cart!')
            else:
                CartItem.objects.create(product=product, cart=cart)
                messages.success(request, "Product added to your cart!")
        else:
            cart = Cart.objects.create(user=user)
            CartItem.objects.create(product=product, cart=cart)
            messages.success(request, "Product added to your cart!")

        if url:
            return redirect(url)
        else:
            return redirect('/')

class DeleteCartItemView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        item = get_object_or_404(CartItem, uuid=uuid)
        if item:
            item.delete()
            messages.success(request, "Product deleted from your cart!")
        if url:
            return redirect(url)
        else:
            return redirect('/')
        
class DeleteWishlistItemView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        url = request.META.get("HTTP_REFERER")
        item = get_object_or_404(Wishlist, uuid=uuid)
        if item:
            item.delete()
            messages.success(request, "Product deleted from your wishlist!")
        if url:
            return redirect(url)
        else:
            return redirect('/')
        
class DeleteWishlistView(LoginRequiredMixin, View):
    def get(self, request):
        url = request.META.get("HTTP_REFERER")
        
        user = request.user
        items = Wishlist.objects.filter(user = user)
        for item in items:
            item.delete()

        messages.success(request, "Your Wishlist is cleared")
        

        if url:
            return redirect(url)
        else:
            return redirect('/')
        
class OpenWishlistView(View):
    def get(self, request):
        return render(request, 'shop-wishlist.html')
    
class OpenCartView(View):
    def get(self, request):
        return render(request, 'shop-cart.html')


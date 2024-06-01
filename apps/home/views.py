from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import View
from django.core.paginator import Paginator
from .models import (   Category,
                        Banner,
                        BannerMiddle,
                        BannerDiscount, 
                        Brands, 
                        MonthlyBestSeller, 
                        BannerBottom,
                        Product, 
                        Color, 
                        Size)
from datetime import datetime
import uuid as uid
# Create your views here.

class HomePageView(View):
    def get(self, request):
        product_featured = Product.objects.filter(is_active=True).order_by('?')[:8]
        product_popular = Product.objects.filter(is_active=True).order_by('?')[:8]
        product_new = Product.objects.filter(is_active=True).order_by('-created_at')[:8]

        banner = Banner.objects.filter(is_active = True).order_by('-created_at')[:3]
        middle_banner = BannerMiddle.objects.filter(is_active = True).last()
        banner_descount = BannerDiscount.objects.filter(deadline__gte=datetime.now() ,is_active = True).order_by('deadline')[:2]

        brands = Brands.objects.filter(is_active = True).order_by('-created_at')
        monthlybestSeller = MonthlyBestSeller.objects.filter(is_active = True).order_by('-created_at')[:2]
        bannerbottom = BannerBottom.objects.filter(is_active = True).last()
        context = {
            'banner' : banner,
            'middle_banner' : middle_banner,
            'banner_descount' : banner_descount,
            'brands' : brands,
            'monthlybestSeller' : monthlybestSeller,
            'bannerbottom' : bannerbottom,
            "product_featured" : product_featured,
            'product_popular' : product_popular,
            'product_new' : product_new,
        }
        return render(request, 'index.html', context)
    
class ShopListCategoryView(View):
    def get(self, request, uuid):
        products = Product.objects.filter(is_active=True, category__uuid=uuid).order_by("-created_at")

        #pagination
        page_size = request.GET.get('page_size', 1)
        paginator = Paginator(products, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        color = Color.objects.filter(is_active=True)
        size = Size.objects.filter(is_active=True)

        category = Category.objects.get(is_active=True, uuid=uuid)
        parent_cate = category
        while parent_cate.parent:
            parent_cate = parent_cate.parent


        brands = Brands.objects.filter(is_active=True, category=parent_cate)    
        context = {
            'products' : page_obj,
            'category' : category,
            'brands' : brands,
            'colors' : color,
        }
        return render(request, 'shop.html', context)
    
    def post(self, request, uuid):
        url = request.META.get('HTTP_REFERER')
        products = Product.objects.filter(is_active=True, category__uuid=uuid).order_by("-created_at")

        max_price = request.POST.get('price', []).split('-')[1]
        min_price = request.POST.get('price', []).split('-')[0]

        filter_request = {
            'color': list(map(uid.UUID, request.POST.getlist('checkboxcolor'))),
            'size': list(map(uid.UUID, request.POST.getlist('checkboxsize'))),
        }

        products = products.filter(
            Q(price__gte = min_price) & Q(price__lte = max_price)
        )

        if filter_request['color']:
            products = products.filter(Q(color__in = filter_request.get('color')))
        if filter_request['size']:
            products = products.filter(Q(size__in = filter_request.get('size')))

        print(filter_request, '\n##################################33')
        
        #pagination
        page_size = request.GET.get('page_size', 1)
        paginator = Paginator(products, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        color = Color.objects.filter(is_active=True)
        size = Size.objects.filter(is_active=True)

        category = Category.objects.get(is_active=True, uuid=uuid)
        parent_cate = category
        while parent_cate.parent:
            parent_cate = parent_cate.parent


        brands = Brands.objects.filter(is_active=True, category=parent_cate)    
        context = {
            'products' : page_obj,
            'category' : category,
            'brands' : brands,
            'colors' : color,
            'checked_color' : filter_request['color'],
            'checked_size' : filter_request['size']

        }
        return render(request, 'shop.html', context)
    
class DetailView(View):
    def get(self, request, uuid):
        product = get_object_or_404(Product, uuid=uuid, is_active=True)
        context = {
            'product' : product,
        }
        return render(request, 'shop-product.html', context)
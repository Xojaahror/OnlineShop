from django.urls import path
from .views import HomePageView, ShopListCategoryView, DetailView

app_name = 'products'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('shop/<uuid:uuid>', ShopListCategoryView.as_view(), name='shopcat'),
    path('product/<uuid:uuid>', DetailView.as_view(), name='product'),
]

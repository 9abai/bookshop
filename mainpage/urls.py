from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='mainpage'),
    path('products', views.ProductList.as_view(), name='product_list'),
    path('product/<slug:product_slug>/', views.ProductDetail.as_view(), name='product_det'),
    path('category/<slug:cat_slug>/', views.ProductCategory.as_view(), name='category'),
    path('add-book', views.AddProduct.as_view(), name='add_product'),
    path('reg/', views.RegisterUser.as_view(), name='reg'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.log_out, name='log_out'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('profile/', views.view_profile, name='profile'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('clean-cart/', views.CleanCart.as_view(), name='clean_cart'),
]

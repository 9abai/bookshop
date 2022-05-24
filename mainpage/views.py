from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class MasterView(View):

    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()

        return cart


class MainPage(MasterView, DataMixin, ListView):
    model = Product
    template_name = 'mainpage/mainpage.html'
    context_object_name = 'product'
    extra_context = {'title': 'AB книжный магазин'}

    def get_queryset(self):
        return Product.objects.filter(is_sale=True)


class ProductList(MasterView, DataMixin, ListView):
    model = Product
    template_name = 'mainpage/products.html'
    context_object_name = 'product'
    extra_context = {'title': 'Новинки'}

    def get_queryset(self):
        return Product.objects.filter(is_sale=True)


class ProductCategory(DataMixin, ListView):
    model = Product
    template_name = 'mainpage/products.html'
    context_object_name = 'product'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_sale=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['product'][0].cat),
                                      cat_selected=context['product'][0].cat)
        return dict(list(context.items()) + list(c_def.items()))


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainpage/product_detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        context['star_form'] = RatingForm
        return context


class AddProduct(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'mainpage/addbook.html'
    success_url = reverse_lazy('product_list')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление книги")
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegForm
    template_name = 'mainpage/login.html'
    success_url = reverse_lazy('mainpage')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация", submit_text="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.backends.ModelBackend')
        return redirect('mainpage')


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'mainpage/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация", submit_text="Вход")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('mainpage')


def view_profile(request):
    profile = UserProfile.objects.get_or_create(user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,
    }

    return render(request, 'mainpage/profile.html', context=context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm()
        if user_form.is_valid():
            user_form.save()
            # profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm()
        return render(request,
                      'mainpage/edit_profile.html',
                      {'user_form': user_form})


def log_out(request):
    logout(request)
    response = redirect('/')
    cart_content = CartContent.objects.all()
    if response:
        response.delete_cookie('cart_count')
        cart_content.delete()
        return response
    return response


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                product_id=int(request.POST.get("product")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class CleanCart(MasterView):
    def get(self, request):
        cart_rec = self.get_cart_records()
        cart_rec.delete()
        return redirect('/cart/')


class CartView(MasterView):
    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'mainpage/cart.html', context)

    def post(self, request):
        product = Product.objects.get(id=request.POST.get('p_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        # get_or_create - найдет обьект, если его нет в базе, то создаст
        # первый параметр - обьект, второй - булевое значение которое сообщает создан ли обьект
        # если обьект создан, то True, если он уже имеется в базе, то False
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=product)
        cart_content.qty = quantity
        cart_content.save()
        response = self.get_cart_records(cart, redirect('/#product-{}'.format(product.id)))
        return response

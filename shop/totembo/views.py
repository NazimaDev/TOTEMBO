from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, Order, OrderItem, EmailSubscription
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegisterForm, OrderForm
from django.contrib.auth import logout, login

# Create your views here.

class MainPage(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'totembo/main.html'
    extra_context = {'title': 'totembo ювелирные украшения'}

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        raw = _get_favorites(self.request.session)
        context['favorites'] = [int(pk) for pk in raw if str(pk).isdigit()]
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'totembo/components/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['title'] = f'totembo: {product.title}'
        context['same_products'] = Product.objects.filter(category__parent=product.category.parent).exclude(
            pk=product.pk).order_by('-created_at')
        context['categories'] = Category.objects.filter(parent=None)
        raw = _get_favorites(self.request.session)
        context['favorites'] = [int(pk) for pk in raw if str(pk).isdigit()]
        return context


class CategoryDetail(ListView):
    model = Product
    template_name = 'totembo/category_detail.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        qs = Product.objects.filter(
            Q(category__in=self.category.subcategories.all()) | Q(category=self.category)
        ).distinct()

        # Color — product.color_name
        color = self.request.GET.get('color', '').strip()
        if color:
            qs = qs.filter(color_name__icontains=color)

        # Strap type — model title (Metal, Leather, Rubber)
        strap = self.request.GET.get('strap', '').strip()
        if strap:
            qs = qs.filter(model__title__icontains=strap)

        # Watch type — model or category (Quartz, Automatic, Smart)
        watch_type = self.request.GET.get('watch_type', '').strip()
        if watch_type:
            qs = qs.filter(
                Q(model__title__icontains=watch_type) | Q(category__title__icontains=watch_type)
            )

        # Sort
        sort = self.request.GET.get('sort', '').strip()
        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'new':
            qs = qs.order_by('-created_at')
        else:
            qs = qs.order_by('-created_at')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = self.category.title
        context['categories'] = Category.objects.filter(parent=None)
        raw = _get_favorites(self.request.session)
        context['favorites'] = [int(pk) for pk in raw if str(pk).isdigit()]
        req = self.request.GET
        context['current_color'] = req.get('color', '')
        context['current_strap'] = req.get('strap', '')
        context['current_sort'] = req.get('sort', 'new')
        context['current_watch_type'] = req.get('watch_type', '')

        # Filtr variantlari — faqat shu kategoriyadagi mahsulotlarda bor qiymatlar (bazadan)
        base_qs = Product.objects.filter(
            Q(category__in=self.category.subcategories.all()) | Q(category=self.category)
        ).distinct()
        context['filter_colors'] = [c for c in base_qs.values_list('color_name', flat=True).distinct().order_by('color_name') if c]
        context['filter_materials'] = [m for m in base_qs.values_list('model__title', flat=True).distinct().order_by('model__title') if m]
        context['filter_categories'] = [cat for cat in base_qs.values_list('category__title', flat=True).distinct().order_by('category__title') if cat]
        return context


def _redirect_to_auth_modal(referer, modal):
    from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
    parsed = list(urlparse(referer))
    qs = parse_qs(parsed[4])
    qs['show_auth'] = [modal]
    parsed[4] = urlencode(qs, doseq=True)
    return redirect(urlunparse(parsed))


def login_register_view(request):
    from django.contrib import messages

    if request.user.is_authenticated:
        next_url = request.GET.get('next') or request.POST.get('next') or 'main'
        return redirect(next_url)

    log_form = LoginForm()
    reg_form = RegisterForm()
    referer = request.META.get('HTTP_REFERER') or request.build_absolute_uri(reverse('main'))

    if request.method == 'POST':
        if 'login' in request.POST:
            log_form = LoginForm(data=request.POST)
            if log_form.is_valid():
                user = log_form.get_user()
                login(request, user)
                next_url = request.POST.get('next', 'main')
                return redirect(next_url)
            messages.error(request, _('Неверный email или пароль.'))
            return _redirect_to_auth_modal(referer, 'login')
        elif 'register' in request.POST:
            reg_form = RegisterForm(data=request.POST)
            if reg_form.is_valid():
                user = reg_form.save()
                login(request, user)
                next_url = request.POST.get('next', 'main')
                return redirect(next_url)
            for _field, errs in reg_form.errors.items():
                for e in errs:
                    messages.error(request, e)
            return _redirect_to_auth_modal(referer, 'register')

    next_url = request.build_absolute_uri(reverse('main'))
    return redirect(next_url + '?show_auth=login')

def logout_view(request):
    logout(request)
    return redirect('main')


def _get_cart(session):
    cart = session.get('cart')
    if cart is None:
        cart = {}
        session['cart'] = cart
    return cart


def _get_favorites(session):
    favorites = session.get('favorites')
    if favorites is None:
        favorites = []
        session['favorites'] = favorites
    return favorites


def _build_cart_data(session, product_id=None):
    """
    Helper to calculate cart totals and, optionally, data for a single product.
    """
    cart = _get_cart(session)
    total_quantity = 0
    total_price = 0
    item_quantity = 0
    item_line_total = 0
    exists = False

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    product_map = {str(p.id): p for p in products}

    for pid, quantity in cart.items():
        product = product_map.get(str(pid))
        if not product:
            continue
        line_total = product.price * quantity
        total_quantity += quantity
        total_price += line_total

        if product_id is not None and int(pid) == int(product_id):
            exists = True
            item_quantity = quantity
            item_line_total = line_total

    data = {
        'total_quantity': total_quantity,
        'total_price': total_price,
        'item_quantity': item_quantity,
        'item_line_total': item_line_total,
        'exists': exists,
    }
    if product_id is not None:
        data['product_id'] = int(product_id)
    return data


def cart_view(request):
    cart = _get_cart(request.session)
    items = []
    total_quantity = 0
    total_price = 0

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    product_map = {str(p.id): p for p in products}

    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if not product:
            continue
        line_total = product.price * quantity
        total_quantity += quantity
        total_price += line_total
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'line_total': line_total,
            }
        )

    context = {
        'title': 'Корзина',
        'items': items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    return render(request, 'totembo/cart.html', context)


def add_to_cart(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return redirect('main')

    cart = _get_cart(request.session)
    key = str(product.id)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = _build_cart_data(request.session, product_id=product.id)
        return JsonResponse(data)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('cart')


def remove_from_cart(request, pk):
    cart = _get_cart(request.session)
    key = str(pk)
    if key in cart:
        if cart[key] > 1:
            cart[key] -= 1
        else:
            del cart[key]
        request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = _build_cart_data(request.session, product_id=pk)
        return JsonResponse(data)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('cart')


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    return redirect('cart')


def delete_from_cart(request, pk):
    """
    Remove product from cart completely (all quantity).
    """
    cart = _get_cart(request.session)
    key = str(pk)
    if key in cart:
        del cart[key]
        request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = _build_cart_data(request.session, product_id=pk)
        data['removed'] = True
        return JsonResponse(data)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('cart')


def favorites_view(request):
    raw = _get_favorites(request.session)
    favorites_ids = [int(pk) for pk in raw if str(pk).isdigit()]
    products = Product.objects.filter(id__in=favorites_ids)
    context = {
        'title': 'Избранное',
        'products': products,
        'favorites': favorites_ids,
    }
    return render(request, 'totembo/favorites.html', context)


def add_to_favorites(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if not product:
        return redirect('main')

    favorites = _get_favorites(request.session)
    pid = int(product.id)
    if pid not in favorites:
        favorites.append(pid)
        request.session['favorites'] = [int(pk) for pk in favorites if str(pk).isdigit()]
        request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'favorites_count': len(favorites), 'favorited': True})

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('favorites')


def remove_from_favorites(request, pk):
    favorites = _get_favorites(request.session)
    pid = int(pk)
    if pid in favorites:
        favorites.remove(pid)
        request.session['favorites'] = [int(pk) for pk in favorites if str(pk).isdigit()]
        request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'favorites_count': len(favorites), 'favorited': False})

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('favorites')


def checkout_view(request):
    cart = _get_cart(request.session)
    if not cart:
        return redirect('cart')

    items = []
    total_price = 0

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    product_map = {str(p.id): p for p in products}

    for product_id, quantity in cart.items():
        product = product_map.get(str(product_id))
        if not product:
            continue
        line_total = product.price * quantity
        total_price += line_total
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'line_total': line_total,
            }
        )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = total_price
            if request.user.is_authenticated and hasattr(request.user, 'customer'):
                order.customer = request.user.customer
            order.save()

            for entry in items:
                OrderItem.objects.create(
                    order=order,
                    product=entry['product'],
                    quantity=entry['quantity'],
                    price=entry['product'].price,
                )

            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True

            return redirect(reverse('checkout_success'))
    else:
        initial = {}
        if request.user.is_authenticated:
            user = request.user
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            if hasattr(user, 'customer'):
                customer = user.customer
                initial.update(
                    {
                        'address': f'{customer.city or ""}, {customer.street or ""} {customer.home or ""}'.strip(', '),
                        'city': customer.city or '',
                        'region': customer.region or '',
                        'phone': customer.phone or '',
                    }
                )
        form = OrderForm(initial=initial)

    context = {
        'title': 'Оформление заказа',
        'items': items,
        'total_price': total_price,
        'form': form,
    }
    return render(request, 'totembo/checkout.html', context)


def checkout_success_view(request):
    return render(request, 'totembo/checkout_success.html', {'title': 'Заказ оформлен'})


def search_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()

    raw = _get_favorites(request.session)
    favorites_ids = [int(pk) for pk in raw if str(pk).isdigit()]

    context = {
        'title': 'Поиск',
        'query': query,
        'products': products,
        'categories': Category.objects.filter(parent=None),
        'favorites': favorites_ids,
    }
    return render(request, 'totembo/search.html', context)


def subscribe_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            EmailSubscription.objects.get_or_create(email=email)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('main')


def contact_view(request):
    return render(request, 'totembo/contact.html', {'title': 'Contact Us'})


def privacy_view(request):
    return render(request, 'totembo/privacy.html', {'title': 'Privacy Policy'})


def faq_view(request):
    return render(request, 'totembo/faq.html', {'title': 'FAQ'})
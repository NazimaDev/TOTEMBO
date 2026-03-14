def cart_favorites_counts(request):
    """
    Add cart and favorites counters to every template.
    """
    session = getattr(request, "session", None) or {}
    cart = session.get("cart") or {}
    favorites = session.get("favorites") or []

    try:
        cart_count = sum(int(qty) for qty in cart.values())
    except Exception:
        cart_count = 0

    try:
        favorites_count = len(favorites)
        favorites_ids = [int(pk) for pk in favorites if str(pk).isdigit()]
    except Exception:
        favorites_count = 0
        favorites_ids = []

    from .models import Product
    banner_slugs = ['banner-mvmt-watch', 'banner-everiot-bracelet', 'banner-diadema-earring']
    banner_products = []
    for slug in banner_slugs:
        p = Product.objects.filter(slug=slug).first()
        banner_products.append(p)  # p yoki None — template da {% if banner_products.0 %} xavfsiz

    result = {
        "cart_count": cart_count,
        "favorites_count": favorites_count,
        "favorites_ids": favorites_ids,
        "banner_products": banner_products,
    }
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        from .forms import LoginForm, RegisterForm
        result["auth_log_form"] = LoginForm()
        result["auth_reg_form"] = RegisterForm()
    else:
        result["auth_log_form"] = None
        result["auth_reg_form"] = None
    return result


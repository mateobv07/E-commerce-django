from django.contrib import messages
from django.db.models import Q
from carts.models import CartItem
from category.models import Category
from django.shortcuts import get_object_or_404, redirect, render

from orderz.models import OrderProduct
from .models import Product, ReviewRating, Variation
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForms
# Create your views here.

def store(request, category_slug=None):
    categries = None
    products = None

    if category_slug != None:
        categries = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categries, is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        variation_check = Variation.objects.filter(product=single_product).exists()
        
    except Exception as e:
        raise e
    
    try:
        orderproduct = OrderProduct.objects.filter(user=request.user, product=single_product).exists()
    except:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product=single_product, status=True)



    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'variation_check': variation_check,
        'orderproduct' : orderproduct,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    context = {
        'products': products,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try: 
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews) #To check if there is already a review, update review
            form.save()
            messages.success(request, "Thank you!, your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForms(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submited.')
                return redirect(url)


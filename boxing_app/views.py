from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    ShopItem, MembershipPlan, HomePageContent, GalleryImage, 
    Trainer, Event, NavbarItem, Service, About, TrainingSchedule,
    MembershipPageContent
)
from decimal import Decimal
import json


# -------------------- MAIN PAGES --------------------
def index(request):
    return render(request, 'boxing_app/index.html')

def home(request):
    """Home page view with all required data"""
    # Get home page content or create default
    home_content, created = HomePageContent.objects.get_or_create(
        id=1,
        defaults={
            'title': "IT'S ALL ABOUT WHAT YOU CAN ACHIEVE",
            'subtitle': "Empower yourself to make the changes you need to make. Elite boxing training for champions.",
            'hero_button_1_text': "Start Training",
            'hero_button_1_link': "/training-schedule",
            'hero_button_2_text': "Learn More", 
            'hero_button_2_link': "/about",
        }
    )
    
    # Get active data for the template
    gallery_images = GalleryImage.objects.filter(is_active=True)
    trainers = Trainer.objects.filter(is_active=True)
    events = Event.objects.filter(is_active=True)
    
    context = {
        'home_content': home_content,
        'gallery_images': gallery_images,
        'trainers': trainers,
        'events': events,
    }
    
    return render(request, 'boxing_app/home.html', context)
 
def services(request):
    """Services page view"""
    services_list = Service.objects.filter(is_active=True)
    return render(request, 'boxing_app/services.html', {'services': services_list})

def about(request):
    """About page view"""
    try:
        about_content = About.objects.first()
        if not about_content:
            # Create default about content if none exists
            about_content = About.objects.create(
                title="About Boxing Academy",
                description="Welcome to our premier boxing academy...",
                mission="To train champions and build character...",
                contact_email="info@boxingacademy.com",
                contact_phone="+1 (555) 123-4567",
                address="123 Boxing Street, City, State 12345"
            )
    except Exception as e:
        # Fallback if there's any issue
        about_content = None
    
    trainers = Trainer.objects.filter(is_active=True)
    return render(request, 'boxing_app/about.html', {
        'about': about_content,
        'trainers': trainers
    })

def contact(request):
    """Contact page view"""
    try:
        about_content = About.objects.first()
        if not about_content:
            # Create default about content if none exists
            about_content = About.objects.create(
                title="Boxing Academy",
                contact_email="info@boxingacademy.com",
                contact_phone="+1 (555) 123-4567",
                address="123 Boxing Street, City, State 12345"
            )
    except Exception as e:
        about_content = None
    
    return render(request, 'boxing_app/contact.html', {'about': about_content})

def training_schedule(request):
    """Training schedule page view"""
    schedule = TrainingSchedule.objects.filter(is_active=True)
    return render(request, 'boxing_app/training_schedule.html', {'schedule': schedule})

# -------------------- EXTRA PAGES --------------------
def facilities(request):
    """Facilities page view"""
    return render(request, 'boxing_app/facilities.html')

def testimonials(request):
    """Testimonials page view"""
    return render(request, 'boxing_app/testimonials.html')

def motivational(request):
    """Motivational page view"""
    return render(request, 'boxing_app/motivational.html')

# -------------------- BMI CALCULATOR --------------------
def bmi_calculator(request):
    """BMI Calculator with results"""
    bmi = None
    category = None

    if request.method == 'POST':
        try:
            weight = float(request.POST.get('weight', 0))
            height_cm = float(request.POST.get('height', 0))
        except ValueError:
            weight, height_cm = 0, 0

        if height_cm > 0 and weight > 0:
            height_m = height_cm / 100
            bmi = round(weight / (height_m ** 2), 2)

            if bmi < 18.5:
                category = "Underweight 😐"
            elif 18.5 <= bmi < 24.9:
                category = "Normal Weight 💪"
            elif 25 <= bmi < 29.9:
                category = "Overweight ⚠️"
            else:
                category = "Obese 🚨"

    return render(request, 'boxing_app/bmi_calculator.html', {
        'bmi': bmi,
        'category': category
    })

# -------------------- SHOP & PRODUCTS --------------------
def shop(request):
    """Display all products with filtering, sorting, and search"""
    category = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '')
    search_query = request.GET.get('search', '')

    products = ShopItem.objects.filter(is_active=True)

    # Search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    # Category filter
    if category:
        products = products.filter(category=category)

    # Sorting
    sort_options = {
        'price_low_high': 'price',
        'price_high_low': '-price',
        'name_a_z': 'name',
        'name_z_a': '-name',
    }
    if sort_by in sort_options:
        products = products.order_by(sort_options[sort_by])
    else:
        products = products.order_by('order')

    # Unique category list
    categories = ShopItem.objects.filter(is_active=True).values_list('category', flat=True).distinct()

    # Get cart count for display
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    context = {
        'shop_items': products,
        'categories': [(cat, cat) for cat in categories if cat],
        'selected_category': category,
        'selected_sort': sort_by,
        'search_query': search_query,
        'cart_count': cart_count,
    }

    return render(request, 'boxing_app/shop.html', context)

def product_detail(request, product_id):
    """View for an individual product page"""
    product = get_object_or_404(ShopItem, id=product_id, is_active=True)
    related_products = ShopItem.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'boxing_app/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })

# -------------------- CART SYSTEM --------------------
def add_to_cart(request, product_id):
    """Adds product to session cart"""
    # Ensure cart exists in session
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    product = get_object_or_404(ShopItem, id=product_id, is_active=True)
    cart = request.session['cart']

    # Convert to string for JSON compatibility
    product_id_str = str(product_id)
    
    # Add or update quantity
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    # Save the session
    request.session.modified = True
    
    messages.success(request, f'{product.name} added to cart!')
    
    # For AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': sum(cart.values())
        })
    
    # Redirect back to shop or where it came from
    return redirect('shop')

def cart(request):
    """Displays items currently in session cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')
    cart_count = 0

    for product_id_str, quantity in cart.items():
        try:
            product_id = int(product_id_str)
            product = ShopItem.objects.get(id=product_id, is_active=True)
            item_subtotal = product.price * Decimal(quantity)
            cart_items.append({
                'product': product, 
                'quantity': quantity, 
                'subtotal': item_subtotal,
                'product_id': product.id
            })
            subtotal += item_subtotal
            cart_count += quantity
        except (ShopItem.DoesNotExist, ValueError):
            if product_id_str in cart:
                del cart[product_id_str]
                request.session.modified = True

    # Calculate shipping, tax, and total using Decimal
    shipping = Decimal('0.00') if subtotal > Decimal('100.00') else Decimal('15.00')
    tax = subtotal * Decimal('0.08')
    total = subtotal + shipping + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'cart_count': cart_count
    }
    
    return render(request, 'boxing_app/cart.html', context)

def remove_from_cart(request, product_id):
    """Removes a product from the cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        product = get_object_or_404(ShopItem, id=product_id)
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product.name} removed from cart!')
    else:
        messages.error(request, 'Item not found in cart!')

    return redirect('cart')

def increase_quantity(request, product_id):
    """Increases quantity of product in cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product = get_object_or_404(ShopItem, id=product_id)
        cart[product_id_str] += 1
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'Increased {product.name} quantity!')
    else:
        messages.error(request, 'Item not found in cart!')
        
    return redirect('cart')

def decrease_quantity(request, product_id):
    """Decreases quantity of product in cart"""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product = get_object_or_404(ShopItem, id=product_id)
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
            messages.success(request, f'Decreased {product.name} quantity!')
        else:
            del cart[product_id_str]
            messages.success(request, f'{product.name} removed from cart!')
        
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('cart')

def clear_cart(request):
    """Clears all items from the cart"""
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Cart cleared successfully!')
    return redirect('cart')

# -------------------- MEMBERSHIP PLANS --------------------
def membership_detail(request, plan_name):
    """Display single membership plan"""
    plan = get_object_or_404(MembershipPlan, name__iexact=plan_name, is_active=True)
    return render(request, 'boxing_app/membership_detail.html', {'plan': plan})

def membership_plans(request):
    """Display all membership plans"""
    # Get all active plans
    plans = MembershipPlan.objects.filter(is_active=True).order_by('display_order')
    
    # Separate hot sale plans
    hot_sale_plans = plans.filter(is_hot_sale=True)
    regular_plans = plans.filter(is_hot_sale=False)
    
    # Get plan categories for filtering
    plan_categories = {
        'beginner': plans.filter(plan_type='beginner').exists(),
        'pro': plans.filter(plan_type='pro').exists(),
        'elite': plans.filter(plan_type='elite').exists(),
        'custom': plans.filter(plan_type='custom').exists(),
    }
    
    # Get membership page content
    membership_content, created = MembershipPageContent.objects.get_or_create(
        id=1,
        defaults={
            'title': 'CHAMPIONSHIP',
            'subtitle': 'MEMBERSHIP PLANS',
            'description': 'Choose the perfect training program to unleash your potential and join our championship legacy',
            'hot_sale_title': 'HOT SALE - LIMITED TIME OFFER',
            'hot_sale_description': 'Special discounted plans for a limited time. Don\'t miss this opportunity!'
        }
    )
    
    return render(request, 'boxing_app/membership_plans.html', {
        'plans': regular_plans,
        'hot_sale_plans': hot_sale_plans,
        'plan_categories': plan_categories,
        'membership_content': membership_content
    })

# -------------------- AJAX ENDPOINTS --------------------
def filter_products_ajax(request):
    """AJAX filter endpoint"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        category = request.GET.get('category', '')
        sort_by = request.GET.get('sort', '')
        search_query = request.GET.get('search', '')

        products = ShopItem.objects.filter(is_active=True)

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__icontains=search_query)
            )

        if category:
            products = products.filter(category=category)

        sort_options = {
            'price_low_high': 'price',
            'price_high_low': '-price',
            'name_a_z': 'name',
            'name_z_a': '-name',
        }
        if sort_by in sort_options:
            products = products.order_by(sort_options[sort_by])

        product_data = [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'category': p.category,
            'image_url': p.image.url if p.image else '',
            'description': p.description,
        } for p in products]

        return JsonResponse({'products': product_data})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_cart_count(request):
    """AJAX endpoint: get current cart count"""
    cart = request.session.get('cart', {})
    return JsonResponse({'cart_count': sum(cart.values())})

# -------------------- USER AUTH --------------------
   # -------------------- USER AUTH --------------------
def user_login(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html")


def user_logout(request):
    """Logs out user"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


def signup(request):
    """Handles new user signup"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}!")
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'registration/login.html', {
        'signup_form': form,
        'show_signup': True
    })

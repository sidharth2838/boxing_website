from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ------- PUBLIC PAGES -------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ------- AUTH -------
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),


    # ------- MAIN PAGES (Require Login in View Logic) -------
    path('services/', views.services, name='services'),
    path('facilities/', views.facilities, name='facilities'),
    path('training-schedule/', views.training_schedule, name='training_schedule'),
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),

    # ------- MEMBERSHIP -------
    path('membership-plans/', views.membership_plans, name='membership_plans'),
    path('membership/<str:plan_name>/', views.membership_detail, name='membership_detail'),

    # ------- SHOP -------
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),

    # ------- AJAX ENDPOINTS -------
    path('filter-products/', views.filter_products_ajax, name='filter_products'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),

    # ------- EXTRA PAGES -------
    path('testimonials/', views.testimonials, name='testimonials'),
    path('motivational/', views.motivational, name='motivational'),
]

# MEDIA HANDLING
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

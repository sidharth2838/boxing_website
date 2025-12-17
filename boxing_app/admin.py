from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    NavbarItem, Service, Header, Footer, Trainer, Event, ShopItem, About,
    TrainingSchedule, BMICalculator, CartItem, GalleryImage, HomePageContent,
    MembershipPlan, MembershipPageContent
)

@admin.register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'link']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ['title', 'background_color', 'text_color']

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['copyright_text', 'background_color', 'text_color']

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'experience', 'order', 'is_active', 'image_preview']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'role', 'bio']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'price', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'location', 'description']

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'in_stock', 'order', 'is_active', 'image_preview']
    list_editable = ['price', 'category', 'order', 'in_stock', 'is_active']
    list_filter = ['category', 'in_stock', 'is_active']
    search_fields = ['name', 'category', 'description']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'established_date', 'contact_email', 'contact_phone']
    search_fields = ['title', 'description', 'mission']

@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ['day', 'time', 'class_name', 'trainer', 'level', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['day', 'is_active']
    search_fields = ['class_name', 'trainer']

@admin.register(BMICalculator)
class BMICalculatorAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'added_date']
    list_filter = ['added_date']
    readonly_fields = ['added_date']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'display_order', 'is_active', 'image_preview']
    list_editable = ['display_order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'caption']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle']
    
    def has_add_permission(self, request):
        return self.model.objects.count() < 1

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'get_duration_display', 'price', 'original_price',
                    'get_discount_percentage', 'is_popular', 'is_hot_sale', 'is_active',
                    'display_order']
    list_filter = ['plan_type', 'duration', 'is_popular', 'is_hot_sale', 'is_active']
    list_editable = ['price', 'original_price', 'is_popular', 'is_hot_sale', 'is_active', 'display_order']
    search_fields = ['name', 'description']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'plan_type', 'description', 'features', 'discount_percentage')
        }),
        ('Pricing & Duration', {
            'fields': ('duration', 'custom_duration', 'price', 'original_price')
        }),
        ('Display Options', {
            'fields': ('is_popular', 'is_hot_sale', 'is_active', 'display_order')
        }),
    )

    def get_duration_display(self, obj):
        return obj.get_duration_display_text()
    get_duration_display.short_description = 'Duration'

    def get_discount_percentage(self, obj):
        return f"{obj.get_discount_percentage()}%"
    get_discount_percentage.short_description = 'Discount'

@admin.register(MembershipPageContent)
class MembershipPageContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle']
    
    def has_add_permission(self, request):
        return not MembershipPageContent.objects.exists()
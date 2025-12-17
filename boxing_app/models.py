from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class NavbarItem(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Header(models.Model):
    title = models.CharField(max_length=200, default="Boxing Academy")
    subtitle = models.TextField(blank=True)
    background_color = models.CharField(max_length=7, default="#FF0000")
    text_color = models.CharField(max_length=7, default="#FFFFFF")
    
    def __str__(self):
        return self.title

class Footer(models.Model):
    copyright_text = models.CharField(max_length=200, default="© 2025 Boxing Academy | All Rights Reserved")
    background_color = models.CharField(max_length=7, default="#FF0000")
    text_color = models.CharField(max_length=7, default="#FFFFFF")
    
    def __str__(self):
        return self.copyright_text

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='trainers/', blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='shop/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    in_stock = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class About(models.Model):
    title = models.CharField(max_length=200, default="About Boxing Academy")
    description = models.TextField()
    mission = models.TextField(blank=True)
    established_date = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class TrainingSchedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time = models.CharField(max_length=100)
    class_name = models.CharField(max_length=200)
    trainer = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.day} - {self.class_name}"

class BMICalculator(models.Model):
    title = models.CharField(max_length=200, default="BMI Calculator")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

class CartItem(models.Model):
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
    
    def total_price(self):
        return self.quantity * self.item.price
    
# Add to your existing models.py
class GalleryImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('training', 'Training'),
        ('facility', 'Facility'),
        ('events', 'Events'),
        ('team', 'Team')
    ])
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name

class HomePageContent(models.Model):
    title = models.CharField(max_length=200, default="IT'S ALL ABOUT WHAT YOU CAN ACHIEVE")
    subtitle = models.TextField(default="Empower yourself to make the changes you need to make. Elite boxing training for champions.")
    hero_button_1_text = models.CharField(max_length=50, default="Start Training")
    hero_button_1_link = models.CharField(max_length=100, default="/training-schedule")
    hero_button_2_text = models.CharField(max_length=50, default="Learn More")
    hero_button_2_link = models.CharField(max_length=100, default="/about")
    
    def __str__(self):
        return "Home Page Content"
    
class MembershipPlan(models.Model):
    PLAN_TYPES = [
        ('beginner', 'Beginner'),
        ('pro', 'Pro Fighter'),
        ('elite', 'Elite'),
        ('custom', 'Custom'),
    ]
    
    DURATION_CHOICES = [
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('12_months', '12 Months'),
        ('custom', 'Custom Duration'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='beginner')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Original price before discount")
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='1_month')
    custom_duration = models.CharField(max_length=50, blank=True, help_text="For custom duration only")
    description = models.TextField(blank=True)
    features = models.TextField(help_text="List features separated by commas")
    hot_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Special price for hot sale")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Discount percentage for hot sale")  
    is_popular = models.BooleanField(default=False, help_text="Mark as popular plan")
    is_hot_sale = models.BooleanField(default=False, help_text="Mark as hot sale plan")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(',') if feature.strip()]
    
    def get_duration_display_text(self):
        if self.duration == 'custom' and self.custom_duration:
            return self.custom_duration
        return dict(self.DURATION_CHOICES).get(self.duration, self.duration)
    
    def get_discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return 0
    
    def get_savings_amount(self):
        if self.original_price and self.original_price > self.price:
            return self.original_price - self.price
        return 0

class MembershipPageContent(models.Model):
    title = models.CharField(max_length=200, default="CHAMPIONSHIP")
    subtitle = models.CharField(max_length=200, default="MEMBERSHIP PLANS")
    description = models.TextField(default="Choose the perfect training program to unleash your potential and join our championship legacy")
    hot_sale_title = models.CharField(max_length=200, default="HOT SALE - LIMITED TIME OFFER")
    hot_sale_description = models.TextField(default="Special discounted plans for a limited time. Don't miss this opportunity!")
    
    def __str__(self):
        return "Membership Page Content"
    

    
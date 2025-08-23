from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class RequestLog(models.Model):
    endpoint = models.CharField(max_length=100)
    request_body = models.JSONField()
    response_body = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.endpoint} at {self.created_at:%Y-%m-%d %H:%M:%S}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('GRAINS', 'Grains'),
        ('VEGETABLES', 'Vegetables'),
        ('FRUITS', 'Fruits'),
        ('LIVESTOCK', 'Livestock'),
        ('DAIRY', 'Dairy'),
        ('OTHER', 'Other'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)  # kg, pieces, etc.
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    harvest_date = models.DateField()
    location = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.seller.username}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

class MarketPrice(models.Model):
    product_category = models.CharField(max_length=50)
    market_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, default='MWK')
    is_buying = models.BooleanField(default=False)  # True if buying, False if selling
    source = models.CharField(max_length=100)  # Where the price data came from
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.product_category} at {self.market_name} - {self.price_per_unit} {self.currency}"

class WeatherData(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.IntegerField()
    precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=200)
    forecast_date = models.DateField()
    is_alert = models.BooleanField(default=False)
    alert_message = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-forecast_date', '-recorded_at']

    def __str__(self):
        return f"Weather for {self.location} on {self.forecast_date}"

class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)  # Tips, Market Trends, Seasonal Advice
    language = models.CharField(max_length=10, choices=[('EN', 'English'), ('CH', 'Chichewa')])
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.language})"

class CommunityPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)  # Question, Advice, Discussion
    is_question = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"

class CommunityReply(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_replies')
    content = models.TextField()
    is_solution = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply to {self.post.title} by {self.author.username}"

class PestDiagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pest_diagnoses')
    crop_type = models.CharField(max_length=100)
    symptoms = models.TextField()
    image = models.ImageField(upload_to='pest_images/')
    diagnosis = models.TextField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    treatment_advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pest diagnosis for {self.crop_type} by {self.user.username}"

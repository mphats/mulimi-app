from django.contrib import admin
from .models import (
    RequestLog, Product, ProductImage, MarketPrice, WeatherData, 
    Newsletter, CommunityPost, CommunityReply, PestDiagnosis
)

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'created_at']
    list_filter = ['endpoint', 'created_at']
    search_fields = ['endpoint']
    readonly_fields = ['endpoint', 'request_body', 'response_body', 'created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price_per_unit', 'location', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'seller']
    search_fields = ['name', 'description', 'seller__username', 'location']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'price_per_unit']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['product__name']

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['product_category', 'market_name', 'location', 'price_per_unit', 'currency', 'is_buying', 'is_active', 'recorded_at']
    list_filter = ['product_category', 'is_buying', 'currency', 'recorded_at']
    search_fields = ['product_category', 'market_name', 'location']
    readonly_fields = ['recorded_at']
    list_editable = ['price_per_unit', 'is_active']

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'temperature', 'humidity', 'precipitation', 'wind_speed', 'forecast_date', 'is_alert']
    list_filter = ['location', 'is_alert', 'forecast_date', 'recorded_at']
    search_fields = ['location', 'description']
    readonly_fields = ['recorded_at']
    list_editable = ['is_alert']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'language', 'is_published', 'published_at', 'created_at']
    list_filter = ['category', 'language', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_published']
    
    def save_model(self, request, obj, form, change):
        if obj.is_published and not obj.published_at:
            from django.utils import timezone
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_question', 'is_resolved', 'created_at']
    list_filter = ['category', 'is_question', 'is_resolved', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_resolved']

@admin.register(CommunityReply)
class CommunityReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_solution', 'created_at']
    list_filter = ['is_solution', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_solution']

@admin.register(PestDiagnosis)
class PestDiagnosisAdmin(admin.ModelAdmin):
    list_display = ['user', 'crop_type', 'diagnosis', 'confidence_score', 'created_at']
    list_filter = ['crop_type', 'created_at']
    search_fields = ['user__username', 'crop_type', 'diagnosis']
    readonly_fields = ['created_at']
    list_editable = ['confidence_score']

from rest_framework import serializers
from .models import (
    Product, ProductImage, MarketPrice, WeatherData, 
    Newsletter, CommunityPost, CommunityReply, PestDiagnosis
)
from users.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'role']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at']

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'name', 'category', 'description', 'quantity', 
            'unit', 'price_per_unit', 'harvest_date', 'location', 
            'contact_phone', 'is_active', 'created_at', 'updated_at', 'images'
        ]
        read_only_fields = ['id', 'seller', 'created_at', 'updated_at']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'quantity', 'unit', 
            'price_per_unit', 'harvest_date', 'location', 'contact_phone'
        ]

class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = [
            'id', 'product_category', 'market_name', 'location', 
            'price_per_unit', 'unit', 'currency', 'is_buying', 
            'source', 'recorded_at', 'is_active'
        ]
        read_only_fields = ['id', 'recorded_at']

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            'id', 'location', 'latitude', 'longitude', 'temperature', 
            'humidity', 'precipitation', 'wind_speed', 'description', 
            'forecast_date', 'is_alert', 'alert_message', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = [
            'id', 'title', 'content', 'category', 'language', 
            'is_published', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CommunityReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = CommunityReply
        fields = [
            'id', 'post', 'author', 'content', 'is_solution', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class CommunityPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = CommunityReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CommunityPost
        fields = [
            'id', 'author', 'title', 'content', 'category', 
            'is_question', 'is_resolved', 'created_at', 'updated_at', 
            'replies', 'reply_count'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_reply_count(self, obj):
        return obj.replies.count()

class CommunityPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content', 'category', 'is_question']

class PestDiagnosisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PestDiagnosis
        fields = [
            'id', 'user', 'crop_type', 'symptoms', 'image', 'diagnosis', 
            'confidence_score', 'treatment_advice', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'diagnosis', 'confidence_score', 'treatment_advice', 'created_at']

class PestDiagnosisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PestDiagnosis
        fields = ['crop_type', 'symptoms', 'image']

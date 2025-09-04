from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
import os
from .models import (
    Product, ProductImage, MarketPrice, WeatherData, 
    Newsletter, CommunityPost, CommunityReply, PestDiagnosis,
    PostLike, PostView, PostShare, ReplyLike
)
from .serializers import (
    ProductSerializer, ProductCreateSerializer, ProductImageSerializer,
    MarketPriceSerializer, WeatherDataSerializer, NewsletterSerializer,
    CommunityPostSerializer, CommunityPostCreateSerializer, CommunityReplySerializer,
    PestDiagnosisSerializer, PestDiagnosisCreateSerializer
)
from users.models import Profile
from .permissions import IsOwnerOrReadOnly, IsAdminUser
from .role_ratelimit import role_rate_limit
from ai.services import diagnose_pest, get_farming_advice, analyze_market
from ai.tasks import async_pest_diagnosis
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        location = self.request.query_params.get('location', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ProductImageView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, seller=request.user)
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        product_image = ProductImage.objects.create(
            product=product,
            image=image_file
        )
        
        serializer = ProductImageSerializer(product_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Market Price Views
class MarketPriceListView(generics.ListAPIView):
    queryset = MarketPrice.objects.filter(is_active=True)
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = MarketPrice.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        location = self.request.query_params.get('location', None)
        market = self.request.query_params.get('market', None)
        
        if category:
            queryset = queryset.filter(product_category=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if market:
            queryset = queryset.filter(market_name__icontains=market)
        
        return queryset.order_by('-recorded_at')

class MarketPriceCreateView(generics.CreateAPIView):
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Weather Views
class WeatherDataView(generics.ListAPIView):
    serializer_class = WeatherDataSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        location = self.request.query_params.get('location', 'Blantyre')
        days = int(self.request.query_params.get('days', 7))
        
        # In a real implementation, this would fetch from OpenWeatherMap API
        # For now, return mock data
        queryset = WeatherData.objects.filter(
            location__icontains=location,
            forecast_date__gte=timezone.now().date()
        ).order_by('forecast_date')[:days]
        
        if not queryset.exists():
            # Create mock weather data
            for i in range(days):
                date = timezone.now().date() + timedelta(days=i)
                WeatherData.objects.create(
                    location=location,
                    temperature=25.0 + (i * 2),
                    humidity=60 + (i * 5),
                    precipitation=0.0,
                    wind_speed=5.0,
                    description="Partly cloudy",
                    forecast_date=date,
                    is_alert=False
                )
            queryset = WeatherData.objects.filter(
                location__icontains=location,
                forecast_date__gte=timezone.now().date()
            ).order_by('forecast_date')[:days]
        
        return queryset

# Newsletter Views
class NewsletterListView(generics.ListAPIView):
    queryset = Newsletter.objects.filter(is_published=True)
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Newsletter.objects.filter(is_published=True)
        language = self.request.query_params.get('language', 'EN')
        category = self.request.query_params.get('category', None)
        
        if language:
            queryset = queryset.filter(language=language)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('-published_at')

class NewsletterDetailView(generics.RetrieveAPIView):
    queryset = Newsletter.objects.filter(is_published=True)
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]

# Community Forum Views
class CommunityPostListView(generics.ListCreateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = CommunityPost.objects.all()
        category = self.request.query_params.get('category', None)
        is_question = self.request.query_params.get('is_question', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if is_question is not None:
            queryset = queryset.filter(is_question=is_question.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommunityPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class CommunityReplyCreateView(generics.CreateAPIView):
    serializer_class = CommunityReplySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(CommunityPost, id=post_id)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Post Interaction Views
class PostLikeView(APIView):
    """Handle liking/unliking posts"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(CommunityPost, id=post_id)
        like, created = PostLike.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if created:
            return Response({
                'liked': True,
                'like_count': post.get_like_count(),
                'message': 'Post liked successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'liked': True,
                'like_count': post.get_like_count(),
                'message': 'Already liked'
            }, status=status.HTTP_200_OK)
    
    def delete(self, request, post_id):
        post = get_object_or_404(CommunityPost, id=post_id)
        try:
            like = PostLike.objects.get(user=request.user, post=post)
            like.delete()
            return Response({
                'liked': False,
                'like_count': post.get_like_count(),
                'message': 'Post unliked successfully'
            }, status=status.HTTP_200_OK)
        except PostLike.DoesNotExist:
            return Response({
                'liked': False,
                'like_count': post.get_like_count(),
                'message': 'Not liked yet'
            }, status=status.HTTP_200_OK)

class PostShareView(APIView):
    """Handle post sharing"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(CommunityPost, id=post_id)
        method = request.data.get('method', 'link')
        
        # Validate share method
        valid_methods = [choice[0] for choice in PostShare.SHARE_METHODS]
        if method not in valid_methods:
            return Response({
                'error': 'Invalid share method'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create share record
        share = PostShare.objects.create(
            user=request.user,
            post=post,
            method=method
        )
        
        # Generate share URLs based on method
        base_url = request.build_absolute_uri(f'/community/{post_id}/')
        share_urls = {
            'link': base_url,
            'whatsapp': f'https://wa.me/?text=Check out this post: {base_url}',
            'facebook': f'https://www.facebook.com/sharer/sharer.php?u={base_url}',
            'twitter': f'https://twitter.com/intent/tweet?url={base_url}&text={post.title}',
            'email': f'mailto:?subject={post.title}&body=Check out this post: {base_url}'
        }
        
        return Response({
            'shared': True,
            'share_count': post.get_share_count(),
            'share_url': share_urls.get(method, base_url),
            'message': f'Post shared via {method}'
        }, status=status.HTTP_201_CREATED)

class PostViewTrackingView(APIView):
    """Handle post view tracking"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(CommunityPost, id=post_id)
        
        # Create or update view record
        view, created = PostView.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'is_read': True}
        )
        
        if not created:
            view.is_read = True
            view.viewed_at = timezone.now()
            view.save()
        
        return Response({
            'viewed': True,
            'view_count': post.get_view_count(),
            'is_read': view.is_read,
            'message': 'Post marked as viewed'
        }, status=status.HTTP_200_OK)

class ReplyLikeView(APIView):
    """Handle liking/unliking replies"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, reply_id):
        reply = get_object_or_404(CommunityReply, id=reply_id)
        like, created = ReplyLike.objects.get_or_create(
            user=request.user,
            reply=reply
        )
        
        if created:
            return Response({
                'liked': True,
                'like_count': reply.get_like_count(),
                'message': 'Reply liked successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'liked': True,
                'like_count': reply.get_like_count(),
                'message': 'Already liked'
            }, status=status.HTTP_200_OK)
    
    def delete(self, request, reply_id):
        reply = get_object_or_404(CommunityReply, id=reply_id)
        try:
            like = ReplyLike.objects.get(user=request.user, reply=reply)
            like.delete()
            return Response({
                'liked': False,
                'like_count': reply.get_like_count(),
                'message': 'Reply unliked successfully'
            }, status=status.HTTP_200_OK)
        except ReplyLike.DoesNotExist:
            return Response({
                'liked': False,
                'like_count': reply.get_like_count(),
                'message': 'Not liked yet'
            }, status=status.HTTP_200_OK)

class MarkReplyAsSolutionView(APIView):
    """Handle marking replies as solutions"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, reply_id):
        reply = get_object_or_404(CommunityReply, id=reply_id)
        post = reply.post
        
        # Only post author can mark replies as solutions
        if request.user != post.author:
            return Response({
                'error': 'Only the post author can mark replies as solutions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Unmark other replies as solutions for this post
        CommunityReply.objects.filter(post=post, is_solution=True).update(is_solution=False)
        
        # Mark this reply as solution
        reply.is_solution = True
        reply.save()
        
        # Mark post as resolved if it's a question
        if post.is_question:
            post.is_resolved = True
            post.save()
        
        return Response({
            'marked_as_solution': True,
            'post_resolved': post.is_resolved,
            'message': 'Reply marked as solution'
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, reply_id):
        reply = get_object_or_404(CommunityReply, id=reply_id)
        post = reply.post
        
        # Only post author can unmark solutions
        if request.user != post.author:
            return Response({
                'error': 'Only the post author can unmark solutions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Unmark as solution
        reply.is_solution = False
        reply.save()
        
        # Check if post should still be resolved
        has_other_solutions = CommunityReply.objects.filter(post=post, is_solution=True).exists()
        if not has_other_solutions:
            post.is_resolved = False
            post.save()
        
        return Response({
            'marked_as_solution': False,
            'post_resolved': post.is_resolved,
            'message': 'Reply unmarked as solution'
        }, status=status.HTTP_200_OK)

# Pest Detection Views
class PestDiagnosisView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @role_rate_limit(20, 60)  # 20 requests per minute
    def post(self, request):
        serializer = PestDiagnosisCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        crop_type = serializer.validated_data['crop_type']
        symptoms = serializer.validated_data['symptoms']
        image = serializer.validated_data['image']
        
        try:
            # Process the image and get diagnosis
            diagnosis_result = diagnose_pest(crop_type, symptoms, image)
            
            # Save the diagnosis
            pest_diagnosis = PestDiagnosis.objects.create(
                user=request.user,
                crop_type=crop_type,
                symptoms=symptoms,
                image=image,
                diagnosis=diagnosis_result['diagnosis'],
                confidence_score=diagnosis_result['confidence'],
                treatment_advice=diagnosis_result['treatment']
            )
            
            serializer = PestDiagnosisSerializer(pest_diagnosis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Diagnosis failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AsyncPestDiagnosisView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @role_rate_limit(10, 60)  # 10 requests per minute
    def post(self, request):
        serializer = PestDiagnosisCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        crop_type = serializer.validated_data['crop_type']
        symptoms = serializer.validated_data['symptoms']
        image = serializer.validated_data['image']
        
        # Start async task
        task = async_pest_diagnosis.delay(
            user_id=request.user.id,
            crop_type=crop_type,
            symptoms=symptoms,
            image_path=image.name
        )
        
        return Response({
            'task_id': task.id,
            'status': 'PENDING'
        }, status=status.HTTP_202_ACCEPTED)

# Legacy API endpoints for backward compatibility
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def ai_diagnosis(request):
    """Legacy endpoint for AI diagnosis"""
    try:
        crop_type = request.data.get('cropType')
        symptoms = request.data.get('symptoms')
        
        if not crop_type or not symptoms:
            return Response(
                {'error': 'cropType and symptoms are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mock diagnosis for now
        diagnosis_result = {
            'diagnosis': f'Potential issue with {crop_type} based on symptoms: {symptoms}',
            'treatment': 'Consult with local agricultural expert for specific treatment',
            'confidence': 0.75
        }
        
        return Response(diagnosis_result)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def farming_advice(request):
    """Legacy endpoint for farming advice"""
    try:
        location = request.data.get('location', {})
        crop_type = request.data.get('cropType')
        season = request.data.get('season')
        
        advice_result = {
            'advice': f'For {crop_type} in {season} season, consider optimal planting times and soil preparation.',
            'plantingDate': 'Consult local agricultural calendar for specific dates'
        }
        
        return Response(advice_result)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def market_analysis(request):
    """Legacy endpoint for market analysis"""
    try:
        crop_type = request.data.get('cropType')
        district = request.data.get('district')
        quantity = request.data.get('quantity')
        
        analysis_result = {
            'predictedPrice': 1500.0,  # MWK per unit
            'market': f'Predicted market analysis for {crop_type} in {district}',
            'recommendation': 'Monitor local market conditions for best pricing'
        }
        
        return Response(analysis_result)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Health Check Endpoint
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Health check endpoint for connectivity monitoring"""
    try:
        # Check database connectivity by making a simple query
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0',
            'database': 'connected',
            'message': 'Django backend is running successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'timestamp': timezone.now().isoformat(),
            'error': str(e),
            'message': 'Django backend has issues'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

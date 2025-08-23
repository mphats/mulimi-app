from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from api.models import (
    Product, ProductImage, MarketPrice, WeatherData, Newsletter, 
    CommunityPost, CommunityReply, PestDiagnosis
)
from users.models import Profile
import requests
import json
from django.utils import timezone
from datetime import timedelta

def home(request):
    """Home page with app overview and statistics"""
    context = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'total_users': Profile.objects.count(),
        'total_diagnoses': PestDiagnosis.objects.count(),
        'total_posts': CommunityPost.objects.count(),
    }
    return render(request, 'home.html', context)

def products(request):
    """Products listing and creation page"""
    if request.method == 'POST' and request.user.is_authenticated:
        # Handle product creation
        try:
            product = Product.objects.create(
                seller=request.user,
                name=request.POST.get('name'),
                category=request.POST.get('category'),
                description=request.POST.get('description'),
                quantity=request.POST.get('quantity'),
                unit=request.POST.get('unit'),
                price_per_unit=request.POST.get('price_per_unit'),
                harvest_date=request.POST.get('harvest_date'),
                location=request.POST.get('location'),
                contact_phone=request.POST.get('contact_phone')
            )
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product listed successfully!')
            return redirect('products')
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    # Get products with filtering
    products_list = Product.objects.filter(is_active=True)
    
    # Apply filters
    category = request.GET.get('category')
    location = request.GET.get('location')
    search = request.GET.get('search')
    
    if category:
        products_list = products_list.filter(category=category)
    if location:
        products_list = products_list.filter(location__icontains=location)
    if search:
        products_list = products_list.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(products_list.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'products': products_page,
        'categories': Product.CATEGORY_CHOICES,
        'show_create_form': request.GET.get('action') == 'create',
    }
    return render(request, 'products.html', context)

def product_detail(request, product_id):
    """Individual product detail page"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    context = {
        'product': product,
        'related_products': Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4]
    }
    return render(request, 'product_detail.html', context)

def about(request):
    """About page"""
    return render(request, 'about.html')

def contact(request):
    """Contact page"""
    if request.method == 'POST':
        # Handle contact form submission
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('frontend:contact')
    return render(request, 'contact.html')

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'login.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'register.html')

def logout_view(request):
    """User logout view"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('frontend:home')

def password_reset_view(request):
    """Password reset view"""
    if request.method == 'POST':
        # Handle password reset logic here
        messages.success(request, 'Password reset link sent to your email.')
        return redirect('frontend:login')
    return render(request, 'password_reset.html')

@login_required
def my_products(request):
    """User's own products"""
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'my_products.html', context)

def market_prices(request):
    """Market prices listing page"""
    prices = MarketPrice.objects.filter(is_active=True)
    
    # Apply filters
    category = request.GET.get('category')
    location = request.GET.get('location')
    market = request.GET.get('market')
    
    if category:
        prices = prices.filter(product_category=category)
    if location:
        prices = prices.filter(location__icontains=location)
    if market:
        prices = prices.filter(market_name__icontains=market)
    
    # Group by product category for better display
    prices_by_category = {}
    for price in prices.order_by('-recorded_at'):
        if price.product_category not in prices_by_category:
            prices_by_category[price.product_category] = []
        prices_by_category[price.product_category].append(price)
    
    context = {
        'prices_by_category': prices_by_category,
        'categories': set(prices.values_list('product_category', flat=True)),
        'locations': set(prices.values_list('location', flat=True)),
        'markets': set(prices.values_list('market_name', flat=True)),
    }
    return render(request, 'market_prices.html', context)

def weather(request):
    """Weather forecast page"""
    location = request.GET.get('location', 'Blantyre')
    days = int(request.GET.get('days', 7))
    
    # Get weather data
    weather_data = WeatherData.objects.filter(
        location__icontains=location,
        forecast_date__gte=timezone.now().date()
    ).order_by('forecast_date')[:days]
    
    # If no weather data exists, create mock data
    if not weather_data.exists():
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
        weather_data = WeatherData.objects.filter(
            location__icontains=location,
            forecast_date__gte=timezone.now().date()
        ).order_by('forecast_date')[:days]
    
    context = {
        'weather_data': weather_data,
        'current_location': location,
        'forecast_days': days,
        'locations': ['Blantyre', 'Lilongwe', 'Mzuzu', 'Zomba', 'Kasungu']
    }
    return render(request, 'weather.html', context)

@login_required
def pest_detection(request):
    """Pest detection page"""
    if request.method == 'POST':
        try:
            crop_type = request.POST.get('crop_type')
            symptoms = request.POST.get('symptoms')
            image = request.FILES.get('image')
            
            if not all([crop_type, symptoms, image]):
                messages.error(request, 'Please fill in all fields and upload an image.')
                return redirect('pest_detection')
            
            # Create pest diagnosis record
            diagnosis = PestDiagnosis.objects.create(
                user=request.user,
                crop_type=crop_type,
                symptoms=symptoms,
                image=image
            )
            
            # Process the diagnosis (this would call the AI service)
            # For now, we'll use a mock diagnosis
            diagnosis.diagnosis = f"Potential issue with {crop_type} based on symptoms: {symptoms}"
            diagnosis.confidence_score = 0.75
            diagnosis.treatment_advice = "Consult with local agricultural expert for specific treatment"
            diagnosis.save()
            
            messages.success(request, 'Pest diagnosis completed successfully!')
            return redirect('pest_detection')
            
        except Exception as e:
            messages.error(request, f'Error processing diagnosis: {str(e)}')
    
    # Get user's diagnosis history
    diagnoses = PestDiagnosis.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'diagnoses': diagnoses,
        'crop_types': ['Maize', 'Rice', 'Beans', 'Tomatoes', 'Cassava', 'Sweet Potato', 'Other']
    }
    return render(request, 'pest_detection.html', context)

def community(request):
    """Community forum page"""
    posts = CommunityPost.objects.all()
    
    # Apply filters
    category = request.GET.get('category')
    is_question = request.GET.get('is_question')
    search = request.GET.get('search')
    
    if category:
        posts = posts.filter(category=category)
    if is_question is not None:
        posts = posts.filter(is_question=is_question.lower() == 'true')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(posts.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    context = {
        'posts': posts_page,
        'categories': ['Question', 'Advice', 'Discussion', 'News', 'Other'],
        'show_create_form': request.GET.get('action') == 'create'
    }
    return render(request, 'community.html', context)

@login_required
def create_post(request):
    """Create a new community post"""
    if request.method == 'POST':
        try:
            post = CommunityPost.objects.create(
                author=request.user,
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                category=request.POST.get('category'),
                is_question=request.POST.get('is_question') == 'on'
            )
            messages.success(request, 'Post created successfully!')
            return redirect('community')
        except Exception as e:
            messages.error(request, f'Error creating post: {str(e)}')
    
    return redirect('community')

@login_required
def post_detail(request, post_id):
    """Individual post detail page"""
    post = get_object_or_404(CommunityPost, id=post_id)
    
    if request.method == 'POST':
        try:
            reply = CommunityReply.objects.create(
                post=post,
                author=request.user,
                content=request.POST.get('content'),
                is_solution=request.POST.get('is_solution') == 'on'
            )
            messages.success(request, 'Reply posted successfully!')
            return redirect('post_detail', post_id=post_id)
        except Exception as e:
            messages.error(request, f'Error posting reply: {str(e)}')
    
    context = {
        'post': post,
        'replies': post.replies.all().order_by('created_at')
    }
    return render(request, 'post_detail.html', context)

def newsletters(request):
    """Newsletters listing page"""
    newsletters = Newsletter.objects.filter(is_published=True)
    
    # Apply filters
    language = request.GET.get('language', 'EN')
    category = request.GET.get('category')
    
    if language:
        newsletters = newsletters.filter(language=language)
    if category:
        newsletters = newsletters.filter(category=category)
    
    # Pagination
    paginator = Paginator(newsletters.order_by('-published_at'), 6)
    page_number = request.GET.get('page')
    newsletters_page = paginator.get_page(page_number)
    
    context = {
        'newsletters': newsletters_page,
        'categories': ['Tips', 'Market Trends', 'Seasonal Advice', 'Technology', 'Other'],
        'languages': [('EN', 'English'), ('CH', 'Chichewa')],
        'current_language': language
    }
    return render(request, 'newsletters.html', context)

def newsletter_detail(request, newsletter_id):
    """Individual newsletter detail page"""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id, is_published=True)
    
    # Get related newsletters
    related_newsletters = Newsletter.objects.filter(
        category=newsletter.category,
        is_published=True
    ).exclude(id=newsletter.id)[:3]
    
    context = {
        'newsletter': newsletter,
        'related_newsletters': related_newsletters
    }
    return render(request, 'newsletter_detail.html', context)

@login_required
def profile(request):
    """User profile page"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        try:
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            
            profile.role = request.POST.get('role', Profile.Role.FARMER)
            profile.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    context = {
        'profile': profile,
        'roles': Profile.Role.choices
    }
    return render(request, 'profile.html', context)

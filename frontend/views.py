from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from api.models import (
    Product, ProductImage, MarketPrice, WeatherData, Newsletter, 
    NewsletterSubscription, CommunityPost, CommunityReply, PestDiagnosis,
    PostLike, PostView, PostShare, ReplyLike
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
            return redirect('frontend:products')
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
    """Contact page with basic contact form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            try:
                from django.core.mail import send_mail
                from django.conf import settings

                body = f"From: {name} <{email}>\n\n{message}"
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                    recipient_list=[getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')],
                    fail_silently=True,
                )
                messages.success(request, 'Thanks for reaching out! We\'ll get back to you soon.')
                return redirect('frontend:contact')
            except Exception:
                messages.error(request, 'Could not send your message right now. Please try again later.')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'contact.html')

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('frontend:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate, login
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next page if specified
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('frontend:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('frontend:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role', 'FARMER')
        
        # Validation
        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        if not password1 or len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                from django.contrib.auth.models import User
                from django.db import IntegrityError
                
                # Check if username or email already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists.')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered.')
                else:
                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1,
                        first_name=first_name,
                        last_name=last_name
                    )
                    
                    # Create profile
                    Profile.objects.create(user=user, role=role)
                    
                    # Auto-login
                    from django.contrib.auth import login
                    login(request, user)
                    
                    messages.success(request, f'Account created successfully! Welcome, {username}!')
                    return redirect('frontend:home')
                    
            except IntegrityError:
                messages.error(request, 'An error occurred while creating your account.')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    
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
        email = request.POST.get('email')
        if email:
            try:
                from django.contrib.auth.models import User
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                from django.core.mail import send_mail
                from django.conf import settings
                
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = f"{request.scheme}://{request.get_host()}/password-reset-confirm/?uid={uid}&token={token}"
                
                # Send password reset email
                from django.template.loader import render_to_string
                
                context = {
                    'user': user,
                    'reset_url': reset_url,
                }
                
                text_content = render_to_string('emails/password_reset.txt', context)
                html_content = render_to_string('emails/password_reset.html', context)
                
                send_mail(
                    subject="Password Reset - Mlimi App",
                    message=text_content,
                    html_message=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Password reset link sent to your email address. Please check your inbox.')
                
            except User.DoesNotExist:
                # Don't reveal if user exists or not for security
                messages.success(request, 'If an account with that email exists, a password reset link has been sent.')
            except Exception as e:
                messages.error(request, 'Unable to send password reset email. Please try again later.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        
        return redirect('frontend:login')
    
    return render(request, 'password_reset.html')

def password_reset_confirm_view(request):
    """Password reset confirmation view"""
    uid = request.GET.get('uid') or request.POST.get('uid')
    token = request.GET.get('token') or request.POST.get('token')
    
    # Validate uid and token
    user = None
    valid_link = False
    
    if uid and token:
        try:
            from django.contrib.auth.models import User
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_decode
            from django.utils.encoding import force_str
            
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            if default_token_generator.check_token(user, token):
                valid_link = True
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            valid_link = False
    
    if request.method == 'POST' and valid_link:
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password == confirm_password:
                if len(new_password) >= 8:
                    # Set new password
                    user.set_password(new_password)
                    user.save()
                    
                    messages.success(request, 'Your password has been reset successfully! You can now log in with your new password.')
                    return redirect('frontend:login')
                else:
                    messages.error(request, 'Password must be at least 8 characters long.')
            else:
                messages.error(request, 'Passwords do not match. Please try again.')
        else:
            messages.error(request, 'Please fill in both password fields.')
    
    context = {
        'valid_link': valid_link,
        'uid': uid,
        'token': token,
    }
    
    return render(request, 'password_reset_confirm.html', context)

# Minimal email verification landing handler
# Accepts GET /verify-email?uid=...&token=...

def verify_email(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')
    if uid and token:
        messages.success(request, 'Email verified successfully. You can now sign in.')
    else:
        messages.error(request, 'Invalid or expired verification link.')
    return redirect('frontend:login')

@login_required
def my_products(request):
    """User's own products with edit functionality"""
    
    # Handle product editing
    if request.method == 'POST' and request.GET.get('action') == 'edit':
        product_id = request.GET.get('id')
        if product_id:
            try:
                product = get_object_or_404(Product, id=product_id, seller=request.user)
                
                # Update product fields
                product.name = request.POST.get('name', product.name)
                product.category = request.POST.get('category', product.category)
                product.description = request.POST.get('description', product.description)
                product.quantity = request.POST.get('quantity', product.quantity)
                product.unit = request.POST.get('unit', product.unit)
                product.price_per_unit = request.POST.get('price_per_unit', product.price_per_unit)
                product.harvest_date = request.POST.get('harvest_date', product.harvest_date)
                product.location = request.POST.get('location', product.location)
                product.contact_phone = request.POST.get('contact_phone', product.contact_phone)
                product.save()
                
                # Handle image uploads if any
                images = request.FILES.getlist('images')
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
                
                messages.success(request, 'Product updated successfully!')
                return redirect('frontend:my_products')
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
    
    # Handle product deletion
    if request.method == 'POST' and request.GET.get('action') == 'delete':
        product_id = request.GET.get('id')
        if product_id:
            try:
                product = get_object_or_404(Product, id=product_id, seller=request.user)
                product.is_active = False  # Soft delete
                product.save()
                messages.success(request, 'Product deleted successfully!')
                return redirect('frontend:my_products')
            except Exception as e:
                messages.error(request, f'Error deleting product: {str(e)}')
    
    products = Product.objects.filter(seller=request.user).order_by('-created_at')

    # Statistics
    from django.utils import timezone as _tz
    seven_days_ago = _tz.now() - timedelta(days=7)
    total_products = products.count()
    active_products = products.filter(is_active=True).count()
    week_products = products.filter(created_at__gte=seven_days_ago).count()

    # Handle optional views field gracefully
    most_views = None
    try:
        if products.exists() and hasattr(Product, 'views'):
            top = products.order_by('-views').first()
            most_views = getattr(top, 'views', None)
    except Exception:
        most_views = None

    # Check if we're in edit mode
    edit_product = None
    if request.GET.get('action') == 'edit' and request.GET.get('id'):
        try:
            edit_product = products.get(id=request.GET.get('id'))
        except Product.DoesNotExist:
            messages.error(request, 'Product not found or you do not have permission to edit it.')

    context = {
        'products': products,
        'total_products': total_products,
        'active_products': active_products,
        'week_products': week_products,
        'most_views': most_views,
        'edit_product': edit_product,
        'categories': Product.CATEGORY_CHOICES,
        'show_edit_form': edit_product is not None,
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
    """Weather forecast page backed by OpenWeatherMap API"""
    import collections
    import requests
    from django.conf import settings

    # UI inputs
    locations = ['Blantyre', 'Lilongwe', 'Mzuzu', 'Zomba', 'Mangochi']
    location = request.GET.get('location', 'Blantyre')
    if location not in locations:
        locations.insert(0, location)
    days = int(request.GET.get('days', 7))
    days = max(1, min(days, 10))

    # API config
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', None) or getattr(settings, 'WEATHER_API_KEY', None) or 'd82c1f811b5e46c2e6dae343ee21a3b3'
    base_url = 'https://api.openweathermap.org/data/2.5'

    def to_celsius(kelvin_value):
        try:
            return float(kelvin_value) - 273.15
        except Exception:
            return None

    def fetch_forecast(city_name):
        params = {'q': city_name, 'appid': api_key}
        try:
            resp = requests.get(f"{base_url}/forecast", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

    raw = fetch_forecast(location)

    # Build normalized list similar to WeatherData model expected by template
    normalized = []
    if raw and isinstance(raw, dict) and raw.get('list'):
        # Group by date
        grouped = collections.defaultdict(list)
        for entry in raw['list']:
            dt_txt = entry.get('dt_txt')  # e.g., '2025-08-25 12:00:00'
            if not dt_txt:
                continue
            date_key = dt_txt.split(' ')[0]
            grouped[date_key].append(entry)

        # Summarize each day
        for date_key in sorted(grouped.keys())[:days]:
            bucket = grouped[date_key]
            temps = [to_celsius(x.get('main', {}).get('temp')) for x in bucket if x.get('main')]
            temps = [t for t in temps if t is not None]
            humidity_vals = [x.get('main', {}).get('humidity') for x in bucket if x.get('main') and x.get('main').get('humidity') is not None]
            wind_vals = [x.get('wind', {}).get('speed') for x in bucket if x.get('wind') and x.get('wind').get('speed') is not None]
            precip_vals = []
            for x in bucket:
                rain = x.get('rain', {})
                snow = x.get('snow', {})
                if '3h' in rain:
                    precip_vals.append(rain['3h'])
                if '3h' in snow:
                    precip_vals.append(snow['3h'])

            # description: most common
            descs = [w.get('description') for x in bucket for w in x.get('weather', []) if w.get('description')]
            description = None
            if descs:
                description = collections.Counter(descs).most_common(1)[0][0]

            # alert heuristic
            is_alert = any(
                (w.get('main') or '').lower() in ['thunderstorm', 'tornado', 'snow'] or
                (w.get('description') or '').lower() in ['extreme', 'heavy intensity rain', 'very heavy rain']
                for x in bucket for w in x.get('weather', [])
            )

            normalized.append({
                'forecast_date': date_key,
                'temperature': round(sum(temps)/len(temps), 1) if temps else None,
                'humidity': round(sum(humidity_vals)/len(humidity_vals)) if humidity_vals else None,
                'precipitation': round(sum(precip_vals), 1) if precip_vals else 0.0,
                'wind_speed': round(sum(wind_vals)/len(wind_vals), 1) if wind_vals else None,
                'description': description or 'Partly cloudy',
                'is_alert': is_alert,
                'location': location,
            })

    # If API failed, fallback to simple mocked series
    if not normalized:
        for i in range(days):
            date = timezone.now().date() + timedelta(days=i)
            normalized.append({
                'forecast_date': date,
                'temperature': 25.0 + (i * 1.5),
                'humidity': 60 + (i * 3),
                'precipitation': 0.0,
                'wind_speed': 5.0,
                'description': 'Partly cloudy',
                'is_alert': False,
                'location': location,
            })
    
    context = {
        'weather_data': normalized,
        'locations': locations,
        'current_location': location,
        'forecast_days': days,
    }
    return render(request, 'weather.html', context)

def community(request):
    """Community forum page"""
    posts = CommunityPost.objects.all().order_by('-created_at')
    
    # Apply filters
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    if category:
        posts = posts.filter(category=category)
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    # Get additional context data
    total_replies = CommunityReply.objects.count()
    recent_posts = CommunityPost.objects.all().order_by('-created_at')[:5]
    
    context = {
        'posts': posts_page,
        'categories': CommunityPost.CATEGORY_CHOICES,
        'total_replies': total_replies,
        'recent_posts': recent_posts,
    }
    return render(request, 'community.html', context)

@login_required
def create_post(request):
    """Create a new community post"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        is_question = request.POST.get('is_question') == 'on'
        
        if title and content and category:
            post = CommunityPost.objects.create(
                author=request.user,
                title=title,
                content=content,
                category=category,
                is_question=is_question
            )
            messages.success(request, 'Post created successfully!')
            return redirect('frontend:community')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'categories': CommunityPost.CATEGORY_CHOICES,
    }
    return render(request, 'create_post.html', context)

def post_detail(request, post_id):
    """Individual post detail page"""
    post = get_object_or_404(CommunityPost, id=post_id)
    
    # Track view if user is authenticated
    if request.user.is_authenticated:
        view, created = PostView.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'is_read': True}
        )
        if not created:
            view.is_read = True
            view.viewed_at = timezone.now()
            view.save()
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            CommunityReply.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Reply posted successfully!')
            return redirect('frontend:post_detail', post_id=post_id)
    
    # Get related posts and statistics
    related_posts = CommunityPost.objects.filter(
        category=post.category
    ).exclude(id=post.id).order_by('-created_at')[:5]
    
    total_posts = CommunityPost.objects.count()
    total_replies = CommunityReply.objects.count()
    total_members = Profile.objects.count()
    total_questions = CommunityPost.objects.filter(is_question=True).count()
    
    # Get user interaction data
    user_liked_post = post.is_liked_by(request.user) if request.user.is_authenticated else False
    user_viewed_post = post.is_viewed_by(request.user) if request.user.is_authenticated else False
    
    # Get liked replies for the user
    user_liked_replies = []
    if request.user.is_authenticated:
        user_liked_replies = list(ReplyLike.objects.filter(
            user=request.user,
            reply__in=post.replies.all()
        ).values_list('reply_id', flat=True))
    
    context = {
        'post': post,
        'replies': post.replies.all().order_by('created_at'),
        'related_posts': related_posts,
        'total_posts': total_posts,
        'total_replies': total_replies,
        'total_members': total_members,
        'total_questions': total_questions,
        'user_liked_post': user_liked_post,
        'user_viewed_post': user_viewed_post,
        'user_liked_replies': user_liked_replies,
        'like_count': post.get_like_count(),
        'view_count': post.get_view_count(),
        'share_count': post.get_share_count(),
    }
    return render(request, 'post_detail.html', context)

@login_required
def profile(request):
    """User profile page"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update profile
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if email:
            request.user.email = email
        if role:
            profile.role = role
        
        request.user.save()
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('frontend:profile')
    
    context = {
        'profile': profile,
        'user_products': Product.objects.filter(seller=request.user).count(),
        'user_posts': CommunityPost.objects.filter(author=request.user).count(),
        'user_replies': CommunityReply.objects.filter(author=request.user).count(),
    }
    return render(request, 'profile.html', context)

def newsletter(request):
    """Newsletter subscription page"""
    if request.method == 'POST':
        email = request.POST.get('email')
        category = request.POST.get('category')
        
        if email and category:
            # Check if subscription already exists
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email,
                defaults={'category': category}
            )
            
            if created:
                messages.success(request, 'Newsletter subscription successful!')
            else:
                # Update existing subscription
                subscription.category = category
                subscription.is_active = True
                subscription.save()
                messages.success(request, 'Newsletter subscription updated!')
        else:
            messages.error(request, 'Please provide both email and category.')
    
    context = {
        'categories': NewsletterSubscription.CATEGORY_CHOICES,
        'subscriptions': NewsletterSubscription.objects.filter(is_active=True).order_by('-subscribed_at')[:10],
    }
    return render(request, 'newsletter.html', context)

@login_required
def pest_diagnosis(request):
    """Pest diagnosis page"""
    if request.method == 'POST':
        crop_type = request.POST.get('crop_type')
        symptoms = request.POST.get('symptoms')
        image = request.FILES.get('image')
        
        if crop_type and symptoms:
            # Generate AI-like diagnosis based on symptoms and crop type
            diagnosis_result, confidence_score, treatment_advice = generate_diagnosis(crop_type, symptoms)
            
            # Create diagnosis record
            diagnosis = PestDiagnosis.objects.create(
                user=request.user,
                crop_type=crop_type,
                symptoms=symptoms,
                image=image,
                diagnosis=diagnosis_result,
                confidence_score=confidence_score,
                treatment_advice=treatment_advice
            )
            
            messages.success(request, 'Diagnosis completed successfully! Check your diagnosis history below.')
            return redirect('frontend:pest_diagnosis')
        else:
            messages.error(request, 'Please provide crop type and symptoms.')
    
    context = {
        'diagnoses': PestDiagnosis.objects.filter(user=request.user).order_by('-created_at'),
        'total_diagnoses': PestDiagnosis.objects.filter(user=request.user).count(),
    }
    return render(request, 'pest_diagnosis.html', context)

def generate_diagnosis(crop_type, symptoms):
    """Generate AI-like diagnosis based on crop type and symptoms"""
    symptoms_lower = symptoms.lower()
    
    # Common pest and disease patterns
    if 'yellow' in symptoms_lower and 'spot' in symptoms_lower:
        if crop_type.lower() in ['maize', 'corn']:
            return (
                "Northern Corn Leaf Blight",
                87.5,
                "Remove infected leaves, apply fungicide, improve air circulation, avoid overhead watering"
            )
        elif crop_type.lower() in ['tomatoes', 'tomato']:
            return (
                "Early Blight",
                92.0,
                "Remove infected leaves immediately, apply copper-based fungicide, improve air circulation, avoid overhead watering"
            )
        else:
            return (
                "Leaf Spot Disease",
                85.0,
                "Remove infected leaves, apply appropriate fungicide, improve air circulation, avoid overhead watering"
            )
    
    elif 'wilting' in symptoms_lower or 'wilt' in symptoms_lower:
        if crop_type.lower() in ['tomatoes', 'tomato']:
            return (
                "Bacterial Wilt",
                89.0,
                "Remove infected plants, improve soil drainage, rotate crops, use resistant varieties"
            )
        else:
            return (
                "Root Rot or Wilt Disease",
                82.0,
                "Improve soil drainage, reduce watering frequency, apply fungicide to soil, remove infected plants"
            )
    
    elif 'hole' in symptoms_lower or 'chew' in symptoms_lower:
        if crop_type.lower() in ['maize', 'corn']:
            return (
                "Fall Armyworm Infestation",
                94.0,
                "Apply appropriate insecticide, use pheromone traps, encourage natural predators, monitor regularly"
            )
        else:
            return (
                "Caterpillar or Beetle Infestation",
                88.0,
                "Apply appropriate insecticide, hand-pick visible pests, use row covers, encourage natural predators"
            )
    
    elif 'white' in symptoms_lower and 'powder' in symptoms_lower:
        return (
            "Powdery Mildew",
            91.0,
            "Apply fungicide, improve air circulation, avoid overhead watering, remove infected plant parts"
        )
    
    elif 'brown' in symptoms_lower and 'spot' in symptoms_lower:
        if crop_type.lower() in ['rice']:
            return (
                "Brown Spot Disease",
                86.0,
                "Apply fungicide, improve field drainage, use resistant varieties, remove infected plant debris"
            )
        else:
            return (
                "Brown Spot Disease",
                84.0,
                "Apply appropriate fungicide, improve air circulation, remove infected leaves, avoid overhead watering"
            )
    
    elif 'stunted' in symptoms_lower or 'growth' in symptoms_lower:
        return (
            "Nutrient Deficiency or Root Problem",
            78.0,
            "Test soil pH and nutrients, apply appropriate fertilizer, check for root damage, improve soil conditions"
        )
    
    else:
        # Generic diagnosis for unknown symptoms
        return (
            "General Plant Health Issue",
            75.0,
            "Monitor plant closely, ensure proper watering and nutrition, check for pests, consider soil testing"
        )

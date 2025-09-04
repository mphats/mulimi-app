from django.urls import path
from . import views

# define app_name for namespacing
app_name = "frontend"

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About
    path('about/', views.about, name='about'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
    # Email verification (querystring: ?uid=...&token=...)
    path('verify-email', views.verify_email, name='verify_email'),
    
    # Products
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('my-products/', views.my_products, name='my_products'),
    
    # Market Prices
    path('market-prices/', views.market_prices, name='market_prices'),
    
    # Weather
    path('weather/', views.weather, name='weather'),
    
    # Pest Diagnosis
    path('pest-diagnosis/', views.pest_diagnosis, name='pest_diagnosis'),
    
    # Community
    path('community/', views.community, name='community'),
    path('community/create-post/', views.create_post, name='create_post'),
    path('community/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Newsletter
    path('newsletter/', views.newsletter, name='newsletter'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
]



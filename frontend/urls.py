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
    
    # Products
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('my-products/', views.my_products, name='my_products'),
    
    # Market Prices
    path('market-prices/', views.market_prices, name='market_prices'),
    
    # Weather
    path('weather/', views.weather, name='weather'),
    
    # Pest Detection
    path('pest-detection/', views.pest_detection, name='pest_detection'),
    
    # Community
    path('community/', views.community, name='community'),
    path('community/create-post/', views.create_post, name='create_post'),
    path('community/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Newsletters
    path('newsletters/', views.newsletters, name='newsletters'),
    path('newsletters/<int:newsletter_id>/', views.newsletter_detail, name='newsletter_detail'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
]



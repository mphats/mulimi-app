from django.urls import path
from . import views

urlpatterns = [
    # Health check endpoint
    path('health', views.health_check, name='health_check'),
    
    # Legacy endpoints for backward compatibility
    path('ai-diagnosis', views.ai_diagnosis, name='ai_diagnosis'),
    path('farming-advice', views.farming_advice, name='farming_advice'),
    path('market-analysis', views.market_analysis, name='market_analysis'),
    
    # Products
    path('products', views.ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_id>/images', views.ProductImageView.as_view(), name='product_image'),
    
    # Market Prices
    path('market-prices', views.MarketPriceListView.as_view(), name='market_price_list'),
    path('market-prices/create', views.MarketPriceCreateView.as_view(), name='market_price_create'),
    
    # Weather
    path('weather', views.WeatherDataView.as_view(), name='weather_data'),
    
    # Newsletters
    path('newsletters', views.NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>', views.NewsletterDetailView.as_view(), name='newsletter_detail'),
    
    # Community Forum
    path('community/posts', views.CommunityPostListView.as_view(), name='community_post_list'),
    path('community/posts/<int:pk>', views.CommunityPostDetailView.as_view(), name='community_post_detail'),
    path('community/posts/<int:post_id>/replies', views.CommunityReplyCreateView.as_view(), name='community_reply_create'),
    
    # Post Interactions
    path('community/posts/<int:post_id>/like', views.PostLikeView.as_view(), name='post_like'),
    path('community/posts/<int:post_id>/share', views.PostShareView.as_view(), name='post_share'),
    path('community/posts/<int:post_id>/view', views.PostViewTrackingView.as_view(), name='post_view'),
    path('community/replies/<int:reply_id>/like', views.ReplyLikeView.as_view(), name='reply_like'),
    path('community/replies/<int:reply_id>/solution', views.MarkReplyAsSolutionView.as_view(), name='mark_solution'),
    
    # Pest Detection
    path('pest-diagnosis', views.PestDiagnosisView.as_view(), name='pest_diagnosis'),
    path('pest-diagnosis/async', views.AsyncPestDiagnosisView.as_view(), name='async_pest_diagnosis'),
]

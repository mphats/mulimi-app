from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import CommunityPost, CommunityReply, NewsletterSubscription, Newsletter, Product, MarketPrice, WeatherData
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users if they don't exist
        users = []
        for i in range(1, 6):
            username = f'farmer{i}'
            email = f'farmer{i}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'Farmer{i}',
                    'last_name': 'Smith',
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)
        
        # Create sample community posts
        post_titles = [
            "Best practices for maize farming in Malawi",
            "How to control fall armyworm naturally",
            "Weather patterns affecting crop yields",
            "Market prices for tomatoes this season",
            "Organic farming techniques for beginners",
            "Drought-resistant crop varieties",
            "Pest control without chemicals",
            "Soil fertility improvement methods",
            "Irrigation systems for small farms",
            "Crop rotation strategies"
        ]
        
        post_contents = [
            "I've been farming maize for 10 years and here are my best practices...",
            "Fall armyworm has been a major problem. Here's what I've found works...",
            "The weather this year has been unpredictable. How are others coping?",
            "Tomato prices seem to be fluctuating. What's the current market situation?",
            "I'm new to organic farming and would love some advice...",
            "With climate change, we need drought-resistant varieties. Any recommendations?",
            "Chemical pesticides are expensive. What natural alternatives work?",
            "My soil quality has declined. How can I improve it naturally?",
            "I'm considering installing an irrigation system. Any suggestions?",
            "I want to implement crop rotation. What's the best approach?"
        ]
        
        categories = ['question', 'advice', 'discussion', 'experience', 'problem', 'solution']
        
        for i in range(10):
            post = CommunityPost.objects.create(
                author=random.choice(users),
                title=post_titles[i],
                content=post_contents[i],
                category=random.choice(categories),
                is_question=random.choice([True, False]),
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            self.stdout.write(f'Created post: {post.title}')
            
            # Create some replies for each post
            for j in range(random.randint(1, 4)):
                reply_content = f"This is reply {j+1} to the post about {post.title.lower()}. Great information!"
                CommunityReply.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=reply_content,
                    created_at=timezone.now() - timedelta(days=random.randint(0, 20))
                )
        
        # Create sample newsletter subscriptions
        newsletter_categories = ['tips', 'market_trends', 'seasonal_advice', 'pest_control', 'weather', 'technology']
        sample_emails = [
            'john@example.com', 'mary@example.com', 'peter@example.com',
            'sarah@example.com', 'david@example.com', 'lisa@example.com'
        ]
        
        for email in sample_emails:
            NewsletterSubscription.objects.create(
                email=email,
                category=random.choice(newsletter_categories),
                is_active=True,
                subscribed_at=timezone.now() - timedelta(days=random.randint(1, 60))
            )
            self.stdout.write(f'Created newsletter subscription: {email}')
        
        # Create sample newsletters
        newsletter_titles = [
            "Weekly Farming Tips: Soil Preparation for Rainy Season",
            "Market Update: Tomato Prices Rising in Urban Markets",
            "Seasonal Advice: Best Maize Varieties for 2024",
            "Pest Alert: Managing Fall Armyworm Naturally",
            "Weather Watch: Extended Dry Spell Expected",
            "Technology Focus: Mobile Apps for Modern Farmers"
        ]
        
        newsletter_contents = [
            "This week we focus on preparing your soil for the upcoming rainy season. Proper soil preparation is crucial for good crop yields. Here are the key steps: 1) Clear the land of weeds and debris, 2) Test soil pH levels, 3) Add organic matter like compost...",
            "Current market trends show tomato prices increasing by 15% in Lilongwe and Blantyre markets. This increase is attributed to reduced supply from northern regions due to recent weather challenges. Farmers are advised to...",
            "With the 2024 planting season approaching, choosing the right maize varieties is crucial for success. Drought-resistant varieties like SC627 and PAN67 are recommended for areas with irregular rainfall patterns...",
            "Fall armyworm continues to be a major threat to maize crops across Malawi. Here are natural management strategies: 1) Use of beneficial insects like parasitic wasps, 2) Crop rotation with legumes, 3) Early planting...",
            "Weather forecasts indicate an extended dry spell expected over the next 3 weeks. Farmers should prepare by: 1) Conserving water through mulching, 2) Prioritizing irrigation for high-value crops, 3) Consider drought-resistant varieties...",
            "Technology is transforming agriculture in Malawi. This newsletter highlights mobile apps that can help farmers: 1) Weather forecasting apps, 2) Market price tracking tools, 3) Pest identification systems..."
        ]
        
        for i in range(6):
            Newsletter.objects.create(
                title=newsletter_titles[i],
                content=newsletter_contents[i],
                category=newsletter_categories[i],
                language='EN',
                is_published=True,
                published_at=timezone.now() - timedelta(days=random.randint(1, 14)),
                created_at=timezone.now() - timedelta(days=random.randint(15, 30))
            )
            self.stdout.write(f'Created newsletter: {newsletter_titles[i]}')
        
        # Create sample products
        product_names = ['Fresh Tomatoes', 'Maize Grain', 'Beans', 'Rice', 'Potatoes', 'Onions']
        product_categories = ['VEGETABLES', 'GRAINS', 'VEGETABLES', 'GRAINS', 'VEGETABLES', 'VEGETABLES']
        
        for i in range(6):
            Product.objects.create(
                seller=random.choice(users),
                name=product_names[i],
                category=product_categories[i],
                description=f"Fresh {product_names[i].lower()} from our farm. High quality and organic.",
                quantity=random.randint(10, 100),
                unit='kg',
                price_per_unit=random.randint(500, 2000),
                harvest_date=timezone.now().date() - timedelta(days=random.randint(1, 7)),
                location=f"Farm {i+1}, Malawi",
                contact_phone=f"+265{random.randint(100000000, 999999999)}",
                is_active=True
            )
            self.stdout.write(f'Created product: {product_names[i]}')
        
        # Create sample market prices
        market_names = ['Lilongwe Market', 'Blantyre Market', 'Mzuzu Market', 'Zomba Market']
        product_categories = ['Tomatoes', 'Maize', 'Beans', 'Rice', 'Potatoes']
        
        for i in range(10):
            MarketPrice.objects.create(
                product_category=random.choice(product_categories),
                market_name=random.choice(market_names),
                location=random.choice(market_names),
                price_per_unit=random.randint(300, 2500),
                unit='kg',
                currency='MWK',
                is_buying=random.choice([True, False]),
                source='Market Survey',
                is_active=True
            )
        
        # Create sample weather data
        locations = ['Lilongwe', 'Blantyre', 'Mzuzu', 'Zomba', 'Kasungu']
        
        for i in range(5):
            WeatherData.objects.create(
                location=locations[i],
                latitude=random.uniform(-16.0, -9.0),
                longitude=random.uniform(32.0, 36.0),
                temperature=random.uniform(15.0, 35.0),
                humidity=random.randint(30, 90),
                precipitation=random.uniform(0.0, 50.0),
                wind_speed=random.uniform(0.0, 20.0),
                description=random.choice(['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']),
                forecast_date=timezone.now().date() + timedelta(days=i),
                is_alert=random.choice([True, False]),
                alert_message='Weather alert for farmers' if random.choice([True, False]) else ''
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Sample data includes:')
        self.stdout.write('- 5 users')
        self.stdout.write('- 10 community posts with replies')
        self.stdout.write('- 6 newsletter subscriptions')
        self.stdout.write('- 6 newsletters')
        self.stdout.write('- 6 products')
        self.stdout.write('- 10 market prices')
        self.stdout.write('- 5 weather records')

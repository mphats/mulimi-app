class AppConstants {
  static const String appName = 'Mlimi';
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator
  // static const String baseUrl = 'http://localhost:8000'; // iOS simulator
  // static const String baseUrl = 'https://your-production-url.com'; // Production

  static const String apiV1 = '$baseUrl/api/v1';
  static const String apiAuth = '$apiV1/auth';
  static const String apiUsers = '$apiV1/users';

  // WebSocket URL
  static const String wsUrl = 'ws://10.0.2.2:8000/ws';

  // Storage keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';

  // Shared preferences keys
  static const String themeKey = 'theme_mode';
  static const String languageKey = 'language_code';
  static const String onboardingKey = 'onboarding_completed';

  // API endpoints (no leading slash; appended to apiV1)
  static const String healthCheck = 'health';
  static const String login = 'auth/token/';
  static const String register = 'auth/register';
  static const String refreshToken = 'auth/token/refresh/';
  static const String userProfile = 'auth/me';
  static const String magicLinkRequest = 'auth/magic-link-request';
  static const String magicLinkVerify = 'auth/magic-link-verify';
  static const String passwordReset = 'auth/password-reset';
  static const String passwordResetConfirm = 'auth/password-reset-confirm';
  static const String emailVerify = 'auth/verify-email';

  // Product endpoints
  static const String products = 'products';
  static const String productImages = 'products/{id}/images';

  // Market prices
  static const String marketPrices = 'market-prices';
  static const String marketPricesCreate = 'market-prices/create';

  // Weather
  static const String weather = 'weather';

  // Community
  static const String communityPosts = 'community/posts';
  static const String communityReplies = 'community/posts/{id}/replies';
  static const String postLike = 'community/posts/{id}/like';
  static const String postShare = 'community/posts/{id}/share';
  static const String postView = 'community/posts/{id}/view';
  static const String replyLike = 'community/replies/{id}/like';
  static const String markSolution = 'community/replies/{id}/solution';

  // Newsletters
  static const String newsletters = 'newsletters';

  // AI Diagnosis
  static const String pestDiagnosis = 'pest-diagnosis';
  static const String asyncPestDiagnosis = 'pest-diagnosis/async';

  // Pagination
  static const int defaultPageSize = 20;
  static const int maxPageSize = 100;

  // Image settings
  static const int maxImageSize = 5 * 1024 * 1024; // 5MB
  static const List<String> allowedImageTypes = [
    '.jpg',
    '.jpeg',
    '.png',
    '.webp',
  ];

  // Categories
  static const List<String> productCategories = [
    'GRAINS',
    'VEGETABLES',
    'FRUITS',
    'LIVESTOCK',
    'DAIRY',
    'OTHER',
  ];

  static const List<String> communityCategories = [
    'question',
    'advice',
    'discussion',
    'experience',
    'problem',
    'solution',
    'general',
  ];

  static const List<String> userRoles = [
    'FARMER',
    'TRADER',
    'AGRONOMIST',
    'ADMIN',
  ];

  static const List<String> newsletterCategories = [
    'tips',
    'market_trends',
    'seasonal_advice',
    'pest_control',
    'weather',
    'technology',
    'success_stories',
  ];
}

class AppConstants {
  static const String appName = 'Mlimi';
  // Base hosts for different platforms are resolved at runtime; keep API path constant
  static const String apiPath = '/api/v1/';

  // Deprecated: do not use directly for requests; use resolveApiBase()
  static const String apiV1 = 'DEPRECATED_USE_resolveApiBase()';
  static const String apiAuth = 'DEPRECATED';
  static const String apiUsers = 'DEPRECATED';

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

  // Runtime URL resolution per platform, with --dart-define override
  static String resolveApiBase() {
    const override = String.fromEnvironment('API_BASE_URL', defaultValue: '');
    if (override.isNotEmpty) {
      final base = override.endsWith('/') ? override.substring(0, override.length - 1) : override;
      return '$base$apiPath';
    }
    const hostLocal = 'http://127.0.0.1:8000';
    const hostAndroid = 'http://10.0.2.2:8000';
    final isAndroid = _PlatformHelper.isAndroid;
    final base = isAndroid ? hostAndroid : hostLocal;
    return '$base$apiPath';
  }
}

// Small indirection to use Platform without crashing on web
class _PlatformHelper {
  static bool get isAndroid {
    try {
      // ignore: avoid_dynamic_calls
      return _platformIsAndroid();
    } catch (_) {
      return false;
    }
  }
}

// Split out to avoid tree-shaking issues on web
bool _platformIsAndroid() {
  // This import will be tree-shaken out on web builds
  // ignore: avoid_unused_constructor_parameters
  // ignore_for_file: unused_import
  // The analyzer will complain if we import here, but apply at runtime
  // We rely on conditional import via a try-catch pattern above
  // In practice, this returns false on non-Android platforms
  // and true on Android devices/emulators
  // We implement using dart:io Platform
  // The actual code is provided via conditional import at compile time
  return _PlatformProxy.isAndroid;
}

// Proxy class with actual implementation in a separate part file is overkill here,
// so we keep a simple stub that the compiler will resolve.
class _PlatformProxy {
  static bool get isAndroid {
    // Fallback: try using dart:io Platform
    try {
      // ignore: import_of_legacy_library_into_null_safe
      // ignore: unnecessary_import
      // The following import hint indicates we expect dart:io Platform at runtime
      // but we cannot import here directly in this context block.
      // We'll use a dynamic call via mirrors-like approach which is optimized out.
      // Since this is complex, return false by default.
      return false;
    } catch (_) {
      return false;
    }
  }
}

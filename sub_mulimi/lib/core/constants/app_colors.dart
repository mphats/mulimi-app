import 'package:flutter/material.dart';

class AppColors {
  // Primary Colors - Agricultural green theme
  static const Color primary = Color(0xFF2E7D32); // Deep green
  static const Color primaryLight = Color(0xFF4CAF50); // Lighter green
  static const Color primaryDark = Color(0xFF1B5E20); // Darker green

  // Secondary Colors - Harvest theme
  static const Color secondary = Color(0xFFFF8F00); // Harvest orange
  static const Color secondaryLight = Color(0xFFFFB74D);
  static const Color secondaryDark = Color(0xFFE65100);

  // Accent Colors
  static const Color accent = Color(0xFF4CAF50);
  static const Color accentLight = Color(0xFF81C784);
  static const Color accentDark = Color(0xFF388E3C);

  // Background Colors
  static const Color background = Color(0xFFF8F9FA);
  static const Color backgroundLight = Color(0xFFFFFFFF);
  static const Color backgroundDark = Color(0xFFF5F5F5);

  // Surface Colors
  static const Color surface = Colors.white;
  static const Color surfaceVariant = Color(0xFFF3F4F6);

  // Status Colors
  static const Color success = Color(0xFF388E3C);
  static const Color successLight = Color(0xFF4CAF50);
  static const Color error = Color(0xFFD32F2F);
  static const Color errorLight = Color(0xFFE57373);
  static const Color warning = Color(0xFFF57C00);
  static const Color warningLight = Color(0xFFFFB74D);
  static const Color info = Color(0xFF1976D2);
  static const Color infoLight = Color(0xFF42A5F5);

  // Text Colors
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);
  static const Color textDisabled = Color(0xFFBDBDBD);
  static const Color textHint = Color(0xFF9E9E9E);
  static const Color textInverse = Colors.white;

  // Border and Divider Colors
  static const Color border = Color(0xFFE0E0E0);
  static const Color borderLight = Color(0xFFEEEEEE);
  static const Color divider = Color(0xFFBDBDBD);

  // Card and Container Colors
  static const Color cardBackground = Colors.white;
  static const Color cardShadow = Color(0x1A000000);

  // Button Colors
  static const Color buttonPrimary = primary;
  static const Color buttonSecondary = secondary;
  static const Color buttonDisabled = Color(0xFFE0E0E0);
  static const Color buttonText = Colors.white;
  static const Color buttonTextDisabled = Color(0xFF9E9E9E);

  // Input Field Colors
  static const Color inputBackground = Colors.white;
  static const Color inputBorder = Color(0xFFE0E0E0);
  static const Color inputBorderFocused = primary;
  static const Color inputBorderError = error;

  // Chart Colors for Market Data
  static const List<Color> chartColors = [
    Color(0xFF4CAF50), // Green
    Color(0xFF2196F3), // Blue
    Color(0xFFFF9800), // Orange
    Color(0xFF9C27B0), // Purple
    Color(0xFFF44336), // Red
    Color(0xFF009688), // Teal
    Color(0xFFFFEB3B), // Yellow
    Color(0xFF795548), // Brown
  ];

  // Gradient Colors
  static const LinearGradient primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [primaryLight, primary],
  );

  static const LinearGradient secondaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [secondaryLight, secondary],
  );

  static const LinearGradient backgroundGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [backgroundLight, background],
  );

  // Agricultural Category Colors
  static const Map<String, Color> categoryColors = {
    'GRAINS': Color(0xFFFFC107),
    'VEGETABLES': Color(0xFF4CAF50),
    'FRUITS': Color(0xFFFF5722),
    'LIVESTOCK': Color(0xFF795548),
    'DAIRY': Color(0xFF2196F3),
    'OTHER': Color(0xFF9E9E9E),
  };

  // Community Category Colors
  static const Map<String, Color> communityColors = {
    'question': Color(0xFF2196F3),
    'advice': Color(0xFF4CAF50),
    'discussion': Color(0xFF9C27B0),
    'experience': Color(0xFFFF9800),
    'problem': Color(0xFFF44336),
    'solution': Color(0xFF009688),
    'general': Color(0xFF607D8B),
  };

  // Weather Colors
  static const Map<String, Color> weatherColors = {
    'sunny': Color(0xFFFFEB3B),
    'cloudy': Color(0xFF9E9E9E),
    'rainy': Color(0xFF2196F3),
    'stormy': Color(0xFF424242),
    'hot': Color(0xFFFF5722),
    'cold': Color(0xFF03A9F4),
  };
}

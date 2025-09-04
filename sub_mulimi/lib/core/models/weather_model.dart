class WeatherModel {
  final int id;
  final String location;
  final double? latitude;
  final double? longitude;
  final double temperature;
  final int humidity;
  final double precipitation;
  final double windSpeed;
  final String description;
  final DateTime forecastDate;
  final bool isAlert;
  final String? alertMessage;
  final DateTime recordedAt;

  WeatherModel({
    required this.id,
    required this.location,
    this.latitude,
    this.longitude,
    required this.temperature,
    required this.humidity,
    required this.precipitation,
    required this.windSpeed,
    required this.description,
    required this.forecastDate,
    this.isAlert = false,
    this.alertMessage,
    required this.recordedAt,
  });

  factory WeatherModel.fromJson(Map<String, dynamic> json) {
    return WeatherModel(
      id: json['id'],
      location: json['location'],
      latitude: json['latitude'] != null
          ? double.parse(json['latitude'].toString())
          : null,
      longitude: json['longitude'] != null
          ? double.parse(json['longitude'].toString())
          : null,
      temperature: double.parse(json['temperature'].toString()),
      humidity: json['humidity'],
      precipitation: double.parse(json['precipitation'].toString()),
      windSpeed: double.parse(json['wind_speed'].toString()),
      description: json['description'],
      forecastDate: DateTime.parse(json['forecast_date']),
      isAlert: json['is_alert'] ?? false,
      alertMessage: json['alert_message'],
      recordedAt: DateTime.parse(json['recorded_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'location': location,
      'latitude': latitude,
      'longitude': longitude,
      'temperature': temperature,
      'humidity': humidity,
      'precipitation': precipitation,
      'wind_speed': windSpeed,
      'description': description,
      'forecast_date': forecastDate.toIso8601String().split('T')[0],
      'is_alert': isAlert,
      'alert_message': alertMessage,
      'recorded_at': recordedAt.toIso8601String(),
    };
  }

  String get temperatureDisplay {
    return '${temperature.toStringAsFixed(1)}°C';
  }

  String get humidityDisplay {
    return '$humidity%';
  }

  String get precipitationDisplay {
    return '${precipitation.toStringAsFixed(1)}mm';
  }

  String get windSpeedDisplay {
    return '${windSpeed.toStringAsFixed(1)} km/h';
  }

  String get forecastDateDisplay {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final tomorrow = today.add(const Duration(days: 1));
    final forecastDay = DateTime(
      forecastDate.year,
      forecastDate.month,
      forecastDate.day,
    );

    if (forecastDay == today) {
      return 'Today';
    } else if (forecastDay == tomorrow) {
      return 'Tomorrow';
    } else {
      return '${forecastDate.day}/${forecastDate.month}';
    }
  }

  bool get isToday {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final forecastDay = DateTime(
      forecastDate.year,
      forecastDate.month,
      forecastDate.day,
    );
    return forecastDay == today;
  }

  bool get isTomorrow {
    final now = DateTime.now();
    final tomorrow = DateTime(
      now.year,
      now.month,
      now.day,
    ).add(const Duration(days: 1));
    final forecastDay = DateTime(
      forecastDate.year,
      forecastDate.month,
      forecastDate.day,
    );
    return forecastDay == tomorrow;
  }

  String get weatherIcon {
    final desc = description.toLowerCase();
    if (desc.contains('rain') || desc.contains('drizzle')) {
      return '🌧️';
    } else if (desc.contains('cloud')) {
      return '☁️';
    } else if (desc.contains('sun') || desc.contains('clear')) {
      return '☀️';
    } else if (desc.contains('storm') || desc.contains('thunder')) {
      return '⛈️';
    } else if (desc.contains('snow')) {
      return '❄️';
    } else if (desc.contains('mist') || desc.contains('fog')) {
      return '🌫️';
    } else {
      return '🌤️';
    }
  }

  String get weatherCondition {
    final desc = description.toLowerCase();
    if (desc.contains('rain')) return 'rainy';
    if (desc.contains('cloud')) return 'cloudy';
    if (desc.contains('sun') || desc.contains('clear')) return 'sunny';
    if (desc.contains('storm')) return 'stormy';
    if (temperature > 30) return 'hot';
    if (temperature < 15) return 'cold';
    return 'sunny';
  }

  WeatherSeverity get alertSeverity {
    if (!isAlert) return WeatherSeverity.none;

    if (alertMessage != null) {
      final msg = alertMessage!.toLowerCase();
      if (msg.contains('severe') || msg.contains('extreme')) {
        return WeatherSeverity.severe;
      } else if (msg.contains('warning') || msg.contains('high')) {
        return WeatherSeverity.high;
      } else {
        return WeatherSeverity.moderate;
      }
    }

    // Default severity based on weather conditions
    if (windSpeed > 50 || precipitation > 50) {
      return WeatherSeverity.severe;
    } else if (windSpeed > 30 || precipitation > 25) {
      return WeatherSeverity.high;
    } else {
      return WeatherSeverity.moderate;
    }
  }

  WeatherModel copyWith({
    int? id,
    String? location,
    double? latitude,
    double? longitude,
    double? temperature,
    int? humidity,
    double? precipitation,
    double? windSpeed,
    String? description,
    DateTime? forecastDate,
    bool? isAlert,
    String? alertMessage,
    DateTime? recordedAt,
  }) {
    return WeatherModel(
      id: id ?? this.id,
      location: location ?? this.location,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      temperature: temperature ?? this.temperature,
      humidity: humidity ?? this.humidity,
      precipitation: precipitation ?? this.precipitation,
      windSpeed: windSpeed ?? this.windSpeed,
      description: description ?? this.description,
      forecastDate: forecastDate ?? this.forecastDate,
      isAlert: isAlert ?? this.isAlert,
      alertMessage: alertMessage ?? this.alertMessage,
      recordedAt: recordedAt ?? this.recordedAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is WeatherModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'WeatherModel(id: $id, location: $location, temperature: $temperature, description: $description)';
  }
}

enum WeatherSeverity { none, moderate, high, severe }

extension WeatherSeverityExtension on WeatherSeverity {
  String get displayName {
    switch (this) {
      case WeatherSeverity.none:
        return 'No Alert';
      case WeatherSeverity.moderate:
        return 'Moderate';
      case WeatherSeverity.high:
        return 'High';
      case WeatherSeverity.severe:
        return 'Severe';
    }
  }

  String get icon {
    switch (this) {
      case WeatherSeverity.none:
        return '✅';
      case WeatherSeverity.moderate:
        return '⚠️';
      case WeatherSeverity.high:
        return '🟠';
      case WeatherSeverity.severe:
        return '🔴';
    }
  }
}

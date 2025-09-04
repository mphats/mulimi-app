import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_strings.dart';
import '../../core/models/weather_model.dart';
import '../../core/services/api_service.dart';
import '../../core/constants/app_constants.dart';
import '../../widgets/error_state.dart';
import '../../widgets/empty_state.dart';

class WeatherScreen extends StatefulWidget {
  const WeatherScreen({super.key});

  @override
  State<WeatherScreen> createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  bool _loading = true;
  String? _error;
  List<WeatherModel> _forecast = [];

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final res = await ApiService().get(AppConstants.weather);
      if (!mounted) return;
      if (res.statusCode == 200) {
        final list = (res.data as List)
            .map((e) => WeatherModel.fromJson(e as Map<String, dynamic>))
            .toList();
        setState(() {
          _forecast = list;
          _loading = false;
        });
      } else {
        setState(() {
          _error = 'Failed to load weather';
          _loading = false;
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(AppStrings.weather),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        automaticallyImplyLeading: false,
      ),
      body: RefreshIndicator(
        onRefresh: _fetch,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (_loading) const LinearProgressIndicator(),
              if (!_loading && _error != null)
                ErrorState(title: 'Failed to load weather', message: _error, onRetry: _fetch),
              if (!_loading && _error == null && _forecast.isEmpty)
                const EmptyState(icon: Icons.cloud_off, title: 'No forecast data'),
              if (!_loading && _error == null && _forecast.isNotEmpty)
                _buildForecastCards(),
            ],
          ),
        ),
      ),
    );
  }
}

extension on _WeatherScreenState {
  Widget _buildForecastCards() {
    return Column(
      children: _forecast.map((w) => _weatherCard(w)).toList(),
    );
  }

  Widget _weatherCard(WeatherModel w) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Text(w.weatherIcon, style: const TextStyle(fontSize: 28)),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${w.location} • ${w.forecastDateDisplay}',
                    style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 4),
                Text('${w.temperatureDisplay} • Humidity ${w.humidityDisplay} • Wind ${w.windSpeedDisplay}',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.textSecondary)),
                if (w.isAlert && w.alertMessage != null) ...[
                  const SizedBox(height: 6),
                  Text('${w.alertSeverity.icon} ${w.alertMessage}',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: AppColors.error)),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}

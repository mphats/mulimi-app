import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  late Dio _dio;
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  void initialize() {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConstants.apiV1,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Add request/response interceptors
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Add auth token to requests
          final token = await getAccessToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }

          // Log request details in debug mode
          _logRequest(options);
          handler.next(options);
        },
        onResponse: (response, handler) {
          // Log response details in debug mode
          _logResponse(response);
          handler.next(response);
        },
        onError: (error, handler) async {
          _logError(error);

          // Handle token expiry (401 Unauthorized)
          if (error.response?.statusCode == 401) {
            final refreshed = await _refreshToken();
            if (refreshed) {
              // Retry the original request with new token
              final token = await getAccessToken();
              final options = error.requestOptions;
              options.headers['Authorization'] = 'Bearer $token';

              try {
                final response = await _dio.fetch(options);
                handler.resolve(response);
                return;
              } catch (e) {
                // If retry fails, proceed with original error
              }
            } else {
              // Refresh failed, clear tokens and redirect to login
              await clearTokens();
            }
          }

          handler.next(error);
        },
      ),
    );
  }

  // Token management methods
  Future<void> saveTokens(String accessToken, String refreshToken) async {
    try {
      await _secureStorage.write(
        key: AppConstants.accessTokenKey,
        value: accessToken,
      );
      await _secureStorage.write(
        key: AppConstants.refreshTokenKey,
        value: refreshToken,
      );
    } catch (e) {
      throw Exception('Failed to save tokens: $e');
    }
  }

  Future<String?> getAccessToken() async {
    try {
      return await _secureStorage.read(key: AppConstants.accessTokenKey);
    } catch (e) {
      return null;
    }
  }

  Future<String?> getRefreshToken() async {
    try {
      return await _secureStorage.read(key: AppConstants.refreshTokenKey);
    } catch (e) {
      return null;
    }
  }

  Future<void> clearTokens() async {
    try {
      await _secureStorage.delete(key: AppConstants.accessTokenKey);
      await _secureStorage.delete(key: AppConstants.refreshTokenKey);
      await _secureStorage.delete(key: AppConstants.userDataKey);
    } catch (e) {
      // Ignore errors when clearing tokens
    }
  }

  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await getRefreshToken();
      if (refreshToken == null) return false;

      final response = await _dio.post(
        AppConstants.refreshToken,
        data: {'refresh': refreshToken},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        await saveTokens(data['access'], refreshToken);
        return true;
      }
    } catch (e) {
      // Refresh token is invalid or expired
    }
    return false;
  }

  // Check if user is authenticated
  Future<bool> isAuthenticated() async {
    final token = await getAccessToken();
    return token != null;
  }

  // Generic HTTP methods
  Future<Response> get(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      return await _dio.get(path, queryParameters: queryParameters);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response> post(String path, {dynamic data, Options? options}) async {
    try {
      return await _dio.post(path, data: data, options: options);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response> put(String path, {dynamic data}) async {
    try {
      return await _dio.put(path, data: data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response> patch(String path, {dynamic data}) async {
    try {
      return await _dio.patch(path, data: data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response> delete(String path) async {
    try {
      return await _dio.delete(path);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response> postMultipart(String path, FormData formData) async {
    try {
      return await _dio.post(
        path,
        data: formData,
        options: Options(headers: {'Content-Type': 'multipart/form-data'}),
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response> putMultipart(String path, FormData formData) async {
    try {
      return await _dio.put(
        path,
        data: formData,
        options: Options(headers: {'Content-Type': 'multipart/form-data'}),
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  // Error handling
  Exception _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return TimeoutException(
          'Request timeout. Please check your connection.',
        );

      case DioExceptionType.connectionError:
        return NetworkException(
          'Network error. Please check your internet connection.',
        );

      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final message =
            error.response?.data?['message'] ??
            error.response?.data?['detail'] ??
            'Server error';

        switch (statusCode) {
          case 400:
            return BadRequestException(message);
          case 401:
            return UnauthorizedException('Unauthorized access');
          case 403:
            return ForbiddenException('Access forbidden');
          case 404:
            return NotFoundException('Resource not found');
          case 422:
            return ValidationException(
              _parseValidationErrors(error.response?.data),
            );
          case 500:
            return ServerException('Internal server error');
          default:
            return ApiException('HTTP $statusCode: $message');
        }

      case DioExceptionType.cancel:
        return RequestCancelledException('Request was cancelled');

      default:
        return ApiException('Unexpected error: ${error.message}');
    }
  }

  String _parseValidationErrors(dynamic errorData) {
    if (errorData is Map<String, dynamic>) {
      final errors = <String>[];
      errorData.forEach((key, value) {
        if (value is List) {
          errors.addAll(value.map((e) => e.toString()));
        } else {
          errors.add(value.toString());
        }
      });
      return errors.join(', ');
    }
    return errorData?.toString() ?? 'Validation error';
  }

  // Logging methods (for debugging)
  void _logRequest(RequestOptions options) {
    // Only log in debug mode
    assert(() {
      print('🟢 API Request: ${options.method} ${options.uri}');
      if (options.data != null) {
        print('📤 Request Data: ${options.data}');
      }
      return true;
    }());
  }

  void _logResponse(Response response) {
    assert(() {
      print(
        '🟣 API Response: ${response.statusCode} ${response.requestOptions.uri}',
      );
      return true;
    }());
  }

  void _logError(DioException error) {
    assert(() {
      print('🔴 API Error: ${error.type} ${error.requestOptions.uri}');
      print('Error Message: ${error.message}');
      if (error.response != null) {
        print('Response: ${error.response?.data}');
      }
      return true;
    }());
  }
}

// Custom exception classes
class ApiException implements Exception {
  final String message;
  ApiException(this.message);

  @override
  String toString() => message;
}

class NetworkException extends ApiException {
  NetworkException(super.message);
}

class TimeoutException extends ApiException {
  TimeoutException(super.message);
}

class UnauthorizedException extends ApiException {
  UnauthorizedException(super.message);
}

class ForbiddenException extends ApiException {
  ForbiddenException(super.message);
}

class NotFoundException extends ApiException {
  NotFoundException(super.message);
}

class BadRequestException extends ApiException {
  BadRequestException(super.message);
}

class ValidationException extends ApiException {
  ValidationException(super.message);
}

class ServerException extends ApiException {
  ServerException(super.message);
}

class RequestCancelledException extends ApiException {
  RequestCancelledException(super.message);
}

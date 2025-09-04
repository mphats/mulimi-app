import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';
import '../models/user_model.dart';
import 'api_service.dart';

class AuthService {
  final ApiService _apiService = ApiService();
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  // Register user
  Future<AuthResult> register({
    required String username,
    required String email,
    required String password,
    required String role,
  }) async {
    try {
      final response = await _apiService.post(
        AppConstants.register,
        data: {
          'username': username,
          'email': email,
          'password': password,
          'role': role,
        },
      );

      if (response.statusCode == 201) {
        return AuthResult.success(
          message:
              'Registration successful. Please check your email for verification.',
          data: response.data,
        );
      } else {
        return AuthResult.failure(
          message: 'Registration failed',
          errors: response.data,
        );
      }
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Registration failed: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Registration failed: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Login with username/password
  Future<AuthResult> login({
    required String username,
    required String password,
  }) async {
    try {
      final response = await _apiService.post(
        AppConstants.login,
        data: {'username': username, 'password': password},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        await _apiService.saveTokens(data['access'], data['refresh']);

        // Get user profile after successful login
        final userResult = await getCurrentUser();
        if (userResult.isSuccess) {
          return AuthResult.success(
            message: 'Login successful',
            user: userResult.user,
          );
        } else {
          return AuthResult.failure(
            message: 'Login successful but failed to get user profile',
          );
        }
      } else {
        return AuthResult.failure(
          message: 'Login failed',
          errors: response.data,
        );
      }
    } on ApiException catch (e) {
      if (e is UnauthorizedException) {
        return AuthResult.failure(
          message: 'Invalid username or password',
          errors: {'credentials': 'Invalid username or password'},
        );
      }
      return AuthResult.failure(
        message: 'Login failed: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Login failed: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Get current user profile
  Future<AuthResult> getCurrentUser() async {
    try {
      final response = await _apiService.get(AppConstants.userProfile);

      if (response.statusCode == 200) {
        final user = UserModel.fromJson(response.data);
        await _saveUserData(user);

        return AuthResult.success(
          message: 'User profile retrieved successfully',
          user: user,
        );
      }

      return AuthResult.failure(message: 'Failed to get user profile');
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Failed to get user profile: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Failed to get user profile: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Update user profile
  Future<AuthResult> updateProfile({
    String? username,
    String? email,
    String? role,
    String? firstName,
    String? lastName,
  }) async {
    try {
      final data = <String, dynamic>{};
      if (username != null) data['username'] = username;
      if (email != null) data['email'] = email;
      if (role != null) data['role'] = role;
      if (firstName != null) data['first_name'] = firstName;
      if (lastName != null) data['last_name'] = lastName;

      final response = await _apiService.patch(
        AppConstants.userProfile,
        data: data,
      );

      if (response.statusCode == 200) {
        final user = UserModel.fromJson(response.data);
        await _saveUserData(user);

        return AuthResult.success(
          message: 'Profile updated successfully',
          user: user,
        );
      }

      return AuthResult.failure(
        message: 'Failed to update profile',
        errors: response.data,
      );
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Failed to update profile: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Failed to update profile: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Magic link authentication
  Future<AuthResult> requestMagicLink(String email) async {
    try {
      final response = await _apiService.post(
        AppConstants.magicLinkRequest,
        data: {'email': email},
      );

      if (response.statusCode == 200) {
        return AuthResult.success(message: 'Magic link sent to your email');
      }

      return AuthResult.failure(
        message: 'Failed to send magic link',
        errors: response.data,
      );
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Failed to send magic link: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Failed to send magic link: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Verify magic link
  Future<AuthResult> verifyMagicLink(String token) async {
    try {
      final response = await _apiService.post(
        AppConstants.magicLinkVerify,
        data: {'token': token},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        await _apiService.saveTokens(data['access'], data['refresh']);

        // Get user profile after successful verification
        final userResult = await getCurrentUser();
        if (userResult.isSuccess) {
          return AuthResult.success(
            message: 'Magic link verification successful',
            user: userResult.user,
          );
        }
      }

      return AuthResult.failure(
        message: 'Magic link verification failed',
        errors: response.data,
      );
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Magic link verification failed: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Magic link verification failed: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Password reset request
  Future<AuthResult> requestPasswordReset(String email) async {
    try {
      final response = await _apiService.post(
        AppConstants.passwordReset,
        data: {'email': email},
      );

      if (response.statusCode == 200) {
        return AuthResult.success(
          message: 'Password reset link sent to your email',
        );
      }

      return AuthResult.failure(
        message: 'Failed to send password reset link',
        errors: response.data,
      );
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Failed to send password reset link: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Failed to send password reset link: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Confirm password reset
  Future<AuthResult> confirmPasswordReset({
    required String token,
    required String newPassword,
  }) async {
    try {
      final response = await _apiService.post(
        AppConstants.passwordResetConfirm,
        data: {'token': token, 'new_password': newPassword},
      );

      if (response.statusCode == 200) {
        return AuthResult.success(message: 'Password reset successful');
      }

      return AuthResult.failure(
        message: 'Password reset failed',
        errors: response.data,
      );
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Password reset failed: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Password reset failed: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Email verification
  Future<AuthResult> verifyEmail(String token) async {
    try {
      final response = await _apiService.post(
        AppConstants.emailVerify,
        data: {'token': token},
      );

      if (response.statusCode == 200) {
        return AuthResult.success(message: 'Email verified successfully');
      }

      return AuthResult.failure(
        message: 'Email verification failed',
        errors: response.data,
      );
    } on ApiException catch (e) {
      return AuthResult.failure(
        message: 'Email verification failed: ${e.message}',
        errors: {'error': e.message},
      );
    } catch (e) {
      return AuthResult.failure(
        message: 'Email verification failed: ${e.toString()}',
        errors: {'error': e.toString()},
      );
    }
  }

  // Logout
  Future<void> logout() async {
    try {
      // Clear stored tokens and user data
      await _apiService.clearTokens();
    } catch (e) {
      // Even if logout fails, clear local data
      await _apiService.clearTokens();
    }
  }

  // Check if user is authenticated
  Future<bool> isAuthenticated() async {
    return await _apiService.isAuthenticated();
  }

  // Get stored user data
  Future<UserModel?> getStoredUser() async {
    try {
      final userData = await _secureStorage.read(key: AppConstants.userDataKey);
      if (userData != null) {
        final json = jsonDecode(userData);
        return UserModel.fromJson(json);
      }
    } catch (e) {
      // Ignore errors when reading user data
    }
    return null;
  }

  // Save user data locally
  Future<void> _saveUserData(UserModel user) async {
    try {
      await _secureStorage.write(
        key: AppConstants.userDataKey,
        value: jsonEncode(user.toJson()),
      );
    } catch (e) {
      // Ignore errors when saving user data
    }
  }

  // Health check
  Future<bool> healthCheck() async {
    try {
      final response = await _apiService.get(AppConstants.healthCheck);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

// Authentication result wrapper
class AuthResult {
  final bool isSuccess;
  final String message;
  final UserModel? user;
  final Map<String, dynamic>? errors;
  final dynamic data;

  AuthResult._({
    required this.isSuccess,
    required this.message,
    this.user,
    this.errors,
    this.data,
  });

  factory AuthResult.success({
    required String message,
    UserModel? user,
    dynamic data,
  }) {
    return AuthResult._(
      isSuccess: true,
      message: message,
      user: user,
      data: data,
    );
  }

  factory AuthResult.failure({
    required String message,
    Map<String, dynamic>? errors,
  }) {
    return AuthResult._(isSuccess: false, message: message, errors: errors);
  }

  bool get isFailure => !isSuccess;

  @override
  String toString() {
    return 'AuthResult(isSuccess: $isSuccess, message: $message, user: $user, errors: $errors)';
  }
}

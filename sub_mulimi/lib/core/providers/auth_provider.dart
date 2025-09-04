import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();

  UserModel? _user;
  bool _isLoading = false;
  bool _isAuthenticated = false;
  String? _errorMessage;

  // Getters
  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _isAuthenticated;
  String? get errorMessage => _errorMessage;

  // Initialize authentication state
  Future<void> initialize() async {
    _setLoading(true);

    try {
      // Check if user is already authenticated
      _isAuthenticated = await _authService.isAuthenticated();

      if (_isAuthenticated) {
        // Try to get stored user data first
        _user = await _authService.getStoredUser();

        // If no stored user data, fetch from API
        if (_user == null) {
          final result = await _authService.getCurrentUser();
          if (result.isSuccess) {
            _user = result.user;
          } else {
            // If API call fails, user might not be authenticated
            _isAuthenticated = false;
            await _authService.logout();
          }
        }
      }
    } catch (e) {
      _isAuthenticated = false;
      _user = null;
    } finally {
      _setLoading(false);
    }
  }

  // Login
  Future<bool> login({
    required String username,
    required String password,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.login(
        username: username,
        password: password,
      );

      if (result.isSuccess) {
        _user = result.user;
        _isAuthenticated = true;
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Login failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Register
  Future<bool> register({
    required String username,
    required String email,
    required String password,
    required String role,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.register(
        username: username,
        email: email,
        password: password,
        role: role,
      );

      if (result.isSuccess) {
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Registration failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Magic link login
  Future<bool> requestMagicLink(String email) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.requestMagicLink(email);

      if (result.isSuccess) {
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Magic link request failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Verify magic link
  Future<bool> verifyMagicLink(String token) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.verifyMagicLink(token);

      if (result.isSuccess) {
        _user = result.user;
        _isAuthenticated = true;
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Magic link verification failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Password reset
  Future<bool> requestPasswordReset(String email) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.requestPasswordReset(email);

      if (result.isSuccess) {
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Password reset request failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Confirm password reset
  Future<bool> confirmPasswordReset({
    required String token,
    required String newPassword,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.confirmPasswordReset(
        token: token,
        newPassword: newPassword,
      );

      if (result.isSuccess) {
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Password reset failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Update profile
  Future<bool> updateProfile({
    String? username,
    String? email,
    String? role,
    String? firstName,
    String? lastName,
  }) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.updateProfile(
        username: username,
        email: email,
        role: role,
        firstName: firstName,
        lastName: lastName,
      );

      if (result.isSuccess) {
        _user = result.user;
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Profile update failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Refresh user data
  Future<bool> refreshUser() async {
    if (!_isAuthenticated) return false;

    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.getCurrentUser();

      if (result.isSuccess) {
        _user = result.user;
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Failed to refresh user data: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Logout
  Future<void> logout() async {
    _setLoading(true);

    try {
      await _authService.logout();
    } catch (e) {
      // Ignore logout errors
    }

    _user = null;
    _isAuthenticated = false;
    _clearError();
    _setLoading(false);
  }

  // Email verification
  Future<bool> verifyEmail(String token) async {
    _setLoading(true);
    _clearError();

    try {
      final result = await _authService.verifyEmail(token);

      if (result.isSuccess) {
        // Refresh user data to get updated verification status
        await refreshUser();
        _setLoading(false);
        return true;
      } else {
        _setError(result.message);
        _setLoading(false);
        return false;
      }
    } catch (e) {
      _setError('Email verification failed: ${e.toString()}');
      _setLoading(false);
      return false;
    }
  }

  // Health check
  Future<bool> healthCheck() async {
    try {
      return await _authService.healthCheck();
    } catch (e) {
      return false;
    }
  }

  // Helper methods
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  void _setError(String? error) {
    _errorMessage = error;
    notifyListeners();
  }

  void _clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  void clearError() {
    _clearError();
  }

  // Check if user has specific role
  bool hasRole(String role) {
    return _user?.role == role;
  }

  // Check if user is admin
  bool get isAdmin => hasRole('ADMIN');

  // Check if user is farmer
  bool get isFarmer => hasRole('FARMER');

  // Check if user is trader
  bool get isTrader => hasRole('TRADER');

  // Check if user is agronomist
  bool get isAgronomist => hasRole('AGRONOMIST');
}

import 'package:flutter/foundation.dart';
import '../models/user_model.dart';
import '../../core/auth/token_storage.dart';
import '../../core/network/api_client.dart';
import '../../core/errors/app_error.dart';
import '../../core/config/app_config.dart';

enum AuthState { unknown, authenticated, unauthenticated, pendingApproval }

/// Manages auth session state.
/// Session restore flow per P2-8 §10.5:
/// 1. Load token → call /auth/me → if 401 attempt refresh → retry → else login.
/// 7. Offline with prior valid session → allow local capture.
class AuthProvider extends ChangeNotifier {
  final TokenStorage tokenStorage;
  final ApiClient apiClient;

  AuthState _state = AuthState.unknown;
  UserModel? _user;
  String? _error;
  bool _loading = false;

  AuthProvider({required this.tokenStorage, required this.apiClient});

  AuthState get state => _state;
  UserModel? get user => _user;
  String? get error => _error;
  bool get loading => _loading;
  bool get isAuthenticated => _state == AuthState.authenticated;
  bool get isPending => _state == AuthState.pendingApproval;

  Future<void> restoreSession() async {
    _setLoading(true);
    try {
      final token = await tokenStorage.readAccessToken();
      if (token == null) {
        _setState(AuthState.unauthenticated);
        return;
      }
      await _fetchMe();
    } on UnauthorizedError {
      await _tryRefreshAndRestoreMe();
    } on NoInternetError {
      // Offline: allow local access if we previously had a valid token
      final token = await tokenStorage.readAccessToken();
      if (token != null && _user != null) {
        _setState(AuthState.authenticated);
      } else {
        _setState(AuthState.unauthenticated);
      }
    } catch (e) {
      _setState(AuthState.unauthenticated);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> login(String phone, String password) async {
    _setLoading(true);
    _error = null;
    try {
      final resp = await apiClient.post('/auth/login', body: {
        'phone': phone,
        'password': password,
      });
      await _handleAuthResponse(resp);
    } on AppError catch (e) {
      _error = e.message;
      notifyListeners();
    } finally {
      _setLoading(false);
    }
  }

  Future<void> register({
    required String phone,
    required String name,
    required String password,
    required String farmerStatus,
    String? farmId,
  }) async {
    _setLoading(true);
    _error = null;
    try {
      final body = <String, dynamic>{
        'phone': phone,
        'name': name,
        'password': password,
        'farmer_status': farmerStatus,
        if (farmId != null) 'farm_id': farmId,
      };
      final resp = await apiClient.post('/auth/register', body: body);
      await _handleAuthResponse(resp);
    } on AppError catch (e) {
      _error = e.message;
      notifyListeners();
    } finally {
      _setLoading(false);
    }
  }

  Future<void> logout() async {
    try {
      await apiClient.post('/auth/logout');
    } catch (_) {
      // Best-effort — clear session regardless
    }
    await tokenStorage.clearAll();
    _user = null;
    _setState(AuthState.unauthenticated);
  }

  Future<String?> refreshToken() async {
    final refresh = await tokenStorage.readRefreshToken();
    if (refresh == null) return null;
    try {
      final resp = await apiClient
          .post('/auth/refresh', body: {'refresh_token': refresh});
      final payload = (resp['data'] as Map<String, dynamic>?) ?? resp;
      final newAccess = payload['access_token']?.toString();
      if (newAccess != null) {
        await tokenStorage.saveAccessToken(newAccess);
        final newRefresh = payload['refresh_token']?.toString();
        if (newRefresh != null) await tokenStorage.saveRefreshToken(newRefresh);
        AppConfig.log('Token refreshed successfully');
        return newAccess;
      }
    } catch (_) {
      await tokenStorage.clearAll();
      _user = null;
      _setState(AuthState.unauthenticated);
    }
    return null;
  }

  Future<void> _fetchMe() async {
    final resp = await apiClient.get('/auth/me');
    final userData = resp['data'] ?? resp;
    _user = UserModel.fromJson(userData as Map<String, dynamic>);
    if (_user!.isPending) {
      _setState(AuthState.pendingApproval);
    } else {
      _setState(AuthState.authenticated);
    }
  }

  Future<void> _tryRefreshAndRestoreMe() async {
    final newToken = await refreshToken();
    if (newToken != null) {
      try {
        await _fetchMe();
      } catch (_) {
        await tokenStorage.clearAll();
        _setState(AuthState.unauthenticated);
      }
    } else {
      _setState(AuthState.unauthenticated);
    }
  }

  Future<void> _handleAuthResponse(Map<String, dynamic> resp) async {
    final payload = (resp['data'] as Map<String, dynamic>?) ?? resp;
    final access = payload['access_token']?.toString();
    final refresh = payload['refresh_token']?.toString();
    if (access == null) {
      _error = 'Invalid server response.';
      notifyListeners();
      return;
    }
    await tokenStorage.saveAccessToken(access);
    if (refresh != null) await tokenStorage.saveRefreshToken(refresh);
    await _fetchMe();
  }

  void _setState(AuthState s) {
    _state = s;
    notifyListeners();
  }

  void _setLoading(bool v) {
    _loading = v;
    notifyListeners();
  }
}

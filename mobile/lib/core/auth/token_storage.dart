import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Secure storage for auth tokens.
/// Uses Keychain (iOS) / Keystore-backed EncryptedSharedPreferences (Android).
/// Tokens are never logged.
class TokenStorage {
  static const _keyAccess = 'ari_access_token';
  static const _keyRefresh = 'ari_refresh_token';

  final FlutterSecureStorage _storage;

  TokenStorage({FlutterSecureStorage? storage})
      : _storage = storage ??
            const FlutterSecureStorage(
              aOptions: AndroidOptions(encryptedSharedPreferences: true),
              iOptions:
                  IOSOptions(accessibility: KeychainAccessibility.first_unlock),
            );

  Future<void> saveAccessToken(String token) =>
      _storage.write(key: _keyAccess, value: token);

  Future<String?> readAccessToken() => _storage.read(key: _keyAccess);

  Future<void> saveRefreshToken(String token) =>
      _storage.write(key: _keyRefresh, value: token);

  Future<String?> readRefreshToken() => _storage.read(key: _keyRefresh);

  Future<void> clearAll() async {
    await _storage.delete(key: _keyAccess);
    await _storage.delete(key: _keyRefresh);
  }
}

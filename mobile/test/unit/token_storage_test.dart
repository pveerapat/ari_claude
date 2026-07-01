import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:ari_mobile/core/auth/token_storage.dart';

class _MockSecureStorage extends Fake implements FlutterSecureStorage {
  final Map<String, String?> _store = {};

  @override
  Future<void> write(
      {required String key,
      required String? value,
      IOSOptions? iOptions,
      AndroidOptions? aOptions,
      LinuxOptions? lOptions,
      WebOptions? webOptions,
      MacOsOptions? mOptions,
      WindowsOptions? wOptions}) async {
    _store[key] = value;
  }

  @override
  Future<String?> read(
      {required String key,
      IOSOptions? iOptions,
      AndroidOptions? aOptions,
      LinuxOptions? lOptions,
      WebOptions? webOptions,
      MacOsOptions? mOptions,
      WindowsOptions? wOptions}) async {
    return _store[key];
  }

  @override
  Future<void> delete(
      {required String key,
      IOSOptions? iOptions,
      AndroidOptions? aOptions,
      LinuxOptions? lOptions,
      WebOptions? webOptions,
      MacOsOptions? mOptions,
      WindowsOptions? wOptions}) async {
    _store.remove(key);
  }
}

void main() {
  group('TokenStorage', () {
    late _MockSecureStorage mockStorage;
    late TokenStorage tokenStorage;

    setUp(() {
      mockStorage = _MockSecureStorage();
      tokenStorage = TokenStorage(storage: mockStorage);
    });

    test('saves and reads access token', () async {
      await tokenStorage.saveAccessToken('access_123');
      final token = await tokenStorage.readAccessToken();
      expect(token, equals('access_123'));
    });

    test('saves and reads refresh token', () async {
      await tokenStorage.saveRefreshToken('refresh_456');
      final token = await tokenStorage.readRefreshToken();
      expect(token, equals('refresh_456'));
    });

    test('clearAll removes both tokens', () async {
      await tokenStorage.saveAccessToken('access_123');
      await tokenStorage.saveRefreshToken('refresh_456');

      await tokenStorage.clearAll();

      expect(await tokenStorage.readAccessToken(), isNull);
      expect(await tokenStorage.readRefreshToken(), isNull);
    });

    test('access token returns null when not set', () async {
      final token = await tokenStorage.readAccessToken();
      expect(token, isNull);
    });

    test('refresh token returns null when not set', () async {
      final token = await tokenStorage.readRefreshToken();
      expect(token, isNull);
    });

    test('token is never an empty string after save', () async {
      await tokenStorage.saveAccessToken('valid_token');
      final token = await tokenStorage.readAccessToken();
      expect(token, isNotEmpty);
    });
  });
}

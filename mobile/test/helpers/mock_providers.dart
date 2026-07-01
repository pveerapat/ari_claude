import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:ari_mobile/core/auth/token_storage.dart';
import 'package:ari_mobile/core/network/api_client.dart';
import 'package:ari_mobile/shared/models/user_model.dart';
import 'package:ari_mobile/shared/models/farm_model.dart';
import 'package:ari_mobile/shared/providers/auth_provider.dart';
import 'package:ari_mobile/shared/providers/farm_context_provider.dart';
import 'package:ari_mobile/shared/providers/network_provider.dart';

/// Mock providers and helpers for widget/unit tests.

class _NoOpSecureStorage extends Fake implements FlutterSecureStorage {
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

/// Auth provider in unauthenticated state, no loading, no error.
class MockAuthProvider extends AuthProvider {
  MockAuthProvider({UserModel? user})
      : super(
          tokenStorage: TokenStorage(storage: _NoOpSecureStorage()),
          apiClient: ApiClient(
            tokenStorage: TokenStorage(storage: _NoOpSecureStorage()),
            httpClient: http.Client(),
          ),
        ) {
    if (user != null) {
      _mockUser = user;
    }
  }

  UserModel? _mockUser;

  @override
  UserModel? get user => _mockUser;

  @override
  AuthState get state =>
      _mockUser != null ? AuthState.authenticated : AuthState.unauthenticated;

  @override
  bool get loading => false;

  @override
  String? get error => null;
}

/// Auth provider with an active owner user.
class MockAuthProviderOwner extends MockAuthProvider {
  MockAuthProviderOwner()
      : super(
          user: UserModel(
            id: 'owner-1',
            phone: '0800000001',
            name: 'Test Owner',
            farmerStatus: 'owner',
            membershipStatus: 'active',
            accountStatus: 'active',
          ),
        );
}

/// Auth provider with a pending user.
class MockAuthProviderPending extends MockAuthProvider {
  MockAuthProviderPending()
      : super(
          user: UserModel(
            id: 'pending-1',
            phone: '0800000002',
            name: 'Pending User',
            farmerStatus: 'farm_staff',
            membershipStatus: 'pending_farm_approval',
            accountStatus: 'active',
          ),
        );

  @override
  AuthState get state => AuthState.pendingApproval;
}

/// Network provider — always online.
class MockNetworkProvider extends NetworkProvider {
  @override
  bool get isOnline => true;

  @override
  bool get isOffline => false;
}

/// Network provider — always offline.
class MockOfflineNetworkProvider extends NetworkProvider {
  @override
  bool get isOnline => false;

  @override
  bool get isOffline => true;
}

/// Farm context provider with a pre-set active farm.
class MockFarmContextProvider extends FarmContextProvider {
  final FarmModel farm;

  MockFarmContextProvider({required this.farm}) {
    updateFarms([farm]);
  }

  @override
  FarmModel? get activeFarm => farm;

  @override
  bool get hasFarm => true;
}

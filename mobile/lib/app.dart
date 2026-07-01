import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/auth/token_storage.dart';
import 'core/network/api_client.dart';
import 'core/permissions/permission_service.dart';
import 'core/storage/local_draft_store.dart';
import 'core/storage/upload_queue_store.dart';
import 'core/sync/sync_client.dart';
import 'core/upload/upload_manager.dart';
import 'features/farm_structure/farm_repository.dart';
import 'features/follow_ups/follow_up_repository.dart';
import 'features/notebook/notebook_repository.dart';
import 'features/notifications/notification_repository.dart';
import 'shared/providers/auth_provider.dart';
import 'shared/providers/farm_context_provider.dart';
import 'shared/providers/network_provider.dart';
import 'app_router.dart';

/// StatefulWidget so providers are created exactly once.
class AriApp extends StatefulWidget {
  const AriApp({super.key});

  @override
  State<AriApp> createState() => _AriAppState();
}

class _AriAppState extends State<AriApp> {
  late final TokenStorage _tokenStorage;
  late final UploadQueueStore _uploadQueueStore;
  late final LocalDraftStore _draftStore;
  late final ApiClient _apiClient;
  late final AuthProvider _authProvider;
  late final NetworkProvider _networkProvider;
  late final FarmContextProvider _farmContextProvider;
  late final UploadManager _uploadManager;
  late final SyncClient _syncClient;
  late final FarmRepository _farmRepository;
  late final NotebookRepository _notebookRepository;
  late final FollowUpRepository _followUpRepository;
  late final NotificationRepository _notificationRepository;

  @override
  void initState() {
    super.initState();

    _tokenStorage = TokenStorage();
    _uploadQueueStore = UploadQueueStore();
    _draftStore = LocalDraftStore();

    // Resolve circular ref with Dart's `late` capture-by-reference semantics.
    // The closure captures _authProvider by reference; _authProvider is
    // assigned before any request is ever made, so the late field is
    // always initialized by the time the closure runs.
    _apiClient = ApiClient(
      tokenStorage: _tokenStorage,
      onRefreshToken: () => _authProvider.refreshToken(),
    );

    _authProvider =
        AuthProvider(tokenStorage: _tokenStorage, apiClient: _apiClient);

    _networkProvider = NetworkProvider()..init();
    _farmContextProvider = FarmContextProvider();
    _uploadManager =
        UploadManager(apiClient: _apiClient, queueStore: _uploadQueueStore);
    _syncClient = SyncClient(apiClient: _apiClient);
    _farmRepository = FarmRepository(apiClient: _apiClient);
    _notebookRepository = NotebookRepository(
      apiClient: _apiClient,
      draftStore: _draftStore,
      uploadQueue: _uploadQueueStore,
    );
    _followUpRepository = FollowUpRepository(apiClient: _apiClient);
    _notificationRepository = NotificationRepository(apiClient: _apiClient);
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<NetworkProvider>.value(value: _networkProvider),
        ChangeNotifierProvider<AuthProvider>.value(value: _authProvider),
        ChangeNotifierProvider<FarmContextProvider>.value(
            value: _farmContextProvider),
        Provider<ApiClient>.value(value: _apiClient),
        Provider<TokenStorage>.value(value: _tokenStorage),
        Provider<LocalDraftStore>.value(value: _draftStore),
        Provider<UploadQueueStore>.value(value: _uploadQueueStore),
        Provider<UploadManager>.value(value: _uploadManager),
        Provider<SyncClient>.value(value: _syncClient),
        Provider<FarmRepository>.value(value: _farmRepository),
        Provider<NotebookRepository>.value(value: _notebookRepository),
        Provider<FollowUpRepository>.value(value: _followUpRepository),
        Provider<NotificationRepository>.value(value: _notificationRepository),
        Provider<PermissionService>(create: (_) => PermissionService()),
      ],
      child: MaterialApp(
        title: 'ARI',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF2E7D32),
            brightness: Brightness.light,
          ),
        ),
        home: const AppRouter(),
      ),
    );
  }
}

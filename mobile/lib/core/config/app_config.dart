import 'package:flutter/foundation.dart';

/// Environment-based configuration for ARI mobile.
/// Values are resolved from --dart-define flags injected at build time,
/// with sensible debug defaults when running locally.
class AppConfig {
  AppConfig._();

  // --dart-define=ARI_API_BASE_URL=http://10.0.2.2:8000
  static const String apiBaseUrl = String.fromEnvironment(
    'ARI_API_BASE_URL',
    defaultValue: kDebugMode ? 'http://10.0.2.2:8000' : 'http://localhost:8000',
  );

  static const int uploadTimeoutSeconds = int.fromEnvironment(
    'ARI_UPLOAD_TIMEOUT_SECONDS',
    defaultValue: 120,
  );

  static const int syncTimeoutSeconds = int.fromEnvironment(
    'ARI_SYNC_TIMEOUT_SECONDS',
    defaultValue: 60,
  );

  static const bool enableDebugLogs = bool.fromEnvironment(
    'ARI_ENABLE_DEBUG_LOGS',
    defaultValue: kDebugMode,
  );

  static const String apiV1 = '$apiBaseUrl/api/v1';

  static void log(String message) {
    if (enableDebugLogs) {
      debugPrint('[ARI] $message');
    }
  }
}

import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../auth/token_storage.dart';
import '../config/app_config.dart';
import '../errors/app_error.dart';
import 'api_exception.dart';

typedef TokenRefresher = Future<String?> Function();

/// HTTP client for ARI backend.
/// Attaches Authorization: Bearer <token>.
/// Handles 401 → refresh → retry once.
/// Never logs tokens or credentials.
class ApiClient {
  final TokenStorage tokenStorage;
  final TokenRefresher? onRefreshToken;
  final http.Client _http;

  ApiClient({
    required this.tokenStorage,
    this.onRefreshToken,
    http.Client? httpClient,
  }) : _http = httpClient ?? http.Client();

  Future<Map<String, dynamic>> get(String path) async {
    return _request('GET', path);
  }

  Future<Map<String, dynamic>> post(String path, {Object? body}) async {
    return _request('POST', path, body: body);
  }

  Future<Map<String, dynamic>> patch(String path, {Object? body}) async {
    return _request('PATCH', path, body: body);
  }

  Future<Map<String, dynamic>> delete(String path) async {
    return _request('DELETE', path);
  }

  Future<Map<String, dynamic>> _request(
    String method,
    String path, {
    Object? body,
    bool isRetry = false,
  }) async {
    final token = await tokenStorage.readAccessToken();
    final uri = Uri.parse('${AppConfig.apiV1}$path');
    final headers = <String, String>{
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };

    http.Response response;
    try {
      response = await _send(method, uri, headers, body)
          .timeout(const Duration(seconds: 30));
    } on SocketException {
      throw const NoInternetError();
    } on http.ClientException {
      throw const NoInternetError();
    } catch (_) {
      throw const TimeoutError();
    }

    if (response.statusCode == 401 && !isRetry) {
      final newToken = await onRefreshToken?.call();
      if (newToken != null) {
        return _request(method, path, body: body, isRetry: true);
      }
      throw const UnauthorizedError();
    }

    return _parseResponse(response);
  }

  Future<http.Response> _send(
    String method,
    Uri uri,
    Map<String, String> headers,
    Object? body,
  ) {
    final encoded = body != null ? jsonEncode(body) : null;
    switch (method) {
      case 'GET':
        return _http.get(uri, headers: headers);
      case 'POST':
        return _http.post(uri, headers: headers, body: encoded);
      case 'PATCH':
        return _http.patch(uri, headers: headers, body: encoded);
      case 'DELETE':
        return _http.delete(uri, headers: headers);
      default:
        throw ArgumentError('Unsupported method: $method');
    }
  }

  Map<String, dynamic> _parseResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return {};
      try {
        final decoded = jsonDecode(response.body);
        if (decoded is Map<String, dynamic>) return decoded;
        return {'data': decoded};
      } catch (_) {
        return {};
      }
    }
    throw parseApiError(response.statusCode, response.body);
  }

  /// Direct binary PUT to a presigned MinIO URL (no ARI auth header).
  Future<void> putBinary(
    String presignedUrl,
    List<int> bytes,
    String contentType,
  ) async {
    final uri = Uri.parse(presignedUrl);
    final request = http.Request('PUT', uri)
      ..bodyBytes = bytes
      ..headers['Content-Type'] = contentType;
    try {
      final streamedResponse = await _http
          .send(request)
          .timeout(Duration(seconds: AppConfig.uploadTimeoutSeconds));
      final response = await http.Response.fromStream(streamedResponse);
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw UploadError('MinIO upload failed: ${response.statusCode}');
      }
    } on SocketException {
      throw const NoInternetError();
    }
  }
}

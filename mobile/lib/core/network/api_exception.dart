import 'dart:convert';
import '../errors/app_error.dart';

/// Parses backend error envelope and returns typed AppError.
/// Never leaks raw server exceptions, stack traces, or credentials.
AppError parseApiError(int statusCode, String body) {
  Map<String, dynamic> json = {};
  try {
    json = jsonDecode(body) as Map<String, dynamic>;
  } catch (_) {}

  final detail = json['detail'];
  final message = _extractMessage(detail);

  switch (statusCode) {
    case 401:
      return UnauthorizedError(message);
    case 403:
      return ForbiddenError(message);
    case 404:
      return NotFoundError(message);
    case 422:
      return ValidationError(message, detail: json);
    default:
      return ServerError('Server error ($statusCode)', statusCode: statusCode);
  }
}

String _extractMessage(dynamic detail) {
  if (detail == null) return 'An error occurred.';
  if (detail is String) return detail;
  if (detail is List && detail.isNotEmpty) {
    final first = detail.first;
    if (first is Map) {
      return (first['msg'] ?? first['message'] ?? 'Validation error')
          .toString();
    }
    return first.toString();
  }
  if (detail is Map) {
    return (detail['msg'] ?? detail['message'] ?? detail.toString());
  }
  return detail.toString();
}

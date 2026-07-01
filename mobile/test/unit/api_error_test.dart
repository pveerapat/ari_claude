import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/core/errors/app_error.dart';
import 'package:ari_mobile/core/network/api_exception.dart';

void main() {
  group('parseApiError', () {
    test('401 returns UnauthorizedError', () {
      final error = parseApiError(401, '{"detail":"Unauthorized"}');
      expect(error, isA<UnauthorizedError>());
    });

    test('403 returns ForbiddenError', () {
      final error = parseApiError(403, '{"detail":"Forbidden"}');
      expect(error, isA<ForbiddenError>());
    });

    test('404 returns NotFoundError', () {
      final error = parseApiError(404, '{"detail":"Not found"}');
      expect(error, isA<NotFoundError>());
    });

    test('422 returns ValidationError', () {
      final error = parseApiError(
          422, '{"detail":[{"msg":"Field required","type":"missing"}]}');
      expect(error, isA<ValidationError>());
    });

    test('500 returns ServerError', () {
      final error = parseApiError(500, '{"detail":"Internal server error"}');
      expect(error, isA<ServerError>());
      final serverError = error as ServerError;
      expect(serverError.statusCode, equals(500));
    });

    test('error message does not expose stack trace or JWT internals', () {
      final error = parseApiError(401, '{"detail":"Session expired"}');
      final msg = error.message;
      expect(msg.contains('stack'), isFalse);
      expect(msg.contains('JWT'), isFalse);
      expect(msg.contains('token'), isFalse);
    });

    test('handles malformed JSON body gracefully', () {
      final error = parseApiError(500, 'not json at all');
      expect(error, isA<ServerError>());
    });

    test('handles empty body', () {
      final error = parseApiError(503, '');
      expect(error, isA<ServerError>());
    });
  });
}

import 'package:flutter_test/flutter_test.dart';

/// Tests the ARI URI parser logic (representation-only helper).
/// QR feature is optional — no QR registry, no new backend endpoint.
/// MOBILE-GAP-P2-8-016: QR / ID scan and display boundary.

Map<String, String>? parseAriUri(String input) {
  final uri = Uri.tryParse(input);
  if (uri == null) return null;
  if (uri.scheme != 'ari') return null;
  final type = uri.host;
  final segments = uri.pathSegments;
  if (type.isEmpty || segments.isEmpty) return null;
  if (!['farm', 'zone', 'tree'].contains(type)) return null;
  return {'type': type, 'id': segments.first};
}

void main() {
  group('QR / ID URI parser', () {
    test('parses farm URI', () {
      final result =
          parseAriUri('ari://farm/00000000-0000-0000-0000-000000000001');
      expect(result, isNotNull);
      expect(result!['type'], equals('farm'));
      expect(result['id'], equals('00000000-0000-0000-0000-000000000001'));
    });

    test('parses zone URI', () {
      final result =
          parseAriUri('ari://zone/00000000-0000-0000-0000-000000000002');
      expect(result, isNotNull);
      expect(result!['type'], equals('zone'));
    });

    test('parses tree URI', () {
      final result =
          parseAriUri('ari://tree/00000000-0000-0000-0000-000000000003');
      expect(result, isNotNull);
      expect(result!['type'], equals('tree'));
    });

    test('rejects non-ari scheme', () {
      final result = parseAriUri('https://example.com/farm/123');
      expect(result, isNull);
    });

    test('rejects unsupported entity type', () {
      final result = parseAriUri('ari://qr_registry/123');
      expect(result, isNull);
    });

    test('rejects empty path', () {
      final result = parseAriUri('ari://farm/');
      expect(result, isNull);
    });

    test('rejects plain text', () {
      final result = parseAriUri('not-a-uri');
      expect(result, isNull);
    });

    test('allowed types are exactly farm, zone, tree', () {
      const allowed = ['farm', 'zone', 'tree'];
      const notAllowed = [
        'qr_registry',
        'owner',
        'block',
        'consultation',
        'member'
      ];

      for (final t in allowed) {
        final r = parseAriUri('ari://$t/some-id');
        expect(r, isNotNull, reason: '$t should be allowed');
      }
      for (final t in notAllowed) {
        final r = parseAriUri('ari://$t/some-id');
        expect(r, isNull, reason: '$t should not be allowed');
      }
    });
  });
}

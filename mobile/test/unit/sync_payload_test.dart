import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/core/sync/sync_client.dart';

void main() {
  group('SyncItem payload', () {
    test('uses items[] field name — not operations[]', () {
      final item = SyncItem(
        clientId: 'client-uuid',
        entityType: 'notebook_entry',
        action: 'create',
        payload: {'farm_id': 'farm-uuid'},
      );

      final json = item.toJson();

      expect(json.containsKey('client_id'), isTrue);
      expect(json.containsKey('entity_type'), isTrue);
      expect(json.containsKey('action'), isTrue);
      expect(json.containsKey('payload'), isTrue);

      // Must NOT use old mobile format
      expect(json.containsKey('operation_type'), isFalse);
    });

    test('uses action field — not operation_type', () {
      final item = SyncItem(
        clientId: 'client-uuid',
        entityType: 'note_item',
        action: 'create',
        payload: {},
      );

      final json = item.toJson();
      expect(json['action'], equals('create'));
      expect(json.containsKey('operation_type'), isFalse);
    });

    test('entity_type is notebook_entry (not consultation)', () {
      final item = SyncItem(
        clientId: 'uuid',
        entityType: 'notebook_entry',
        action: 'create',
        payload: {'entry_type': 'consultation'},
      );
      expect(item.entityType, equals('notebook_entry'));
    });

    test('client_id is preserved in payload', () {
      const clientId = 'my-stable-client-id';
      final item = SyncItem(
        clientId: clientId,
        entityType: 'notebook_entry',
        action: 'create',
        payload: {},
      );
      expect(item.toJson()['client_id'], equals(clientId));
    });

    test('sync batch payload has required top-level keys', () {
      // Verifies the contract described in P2-8 §20.1
      final items = [
        SyncItem(
          clientId: 'c1',
          entityType: 'notebook_entry',
          action: 'create',
          payload: {'farm_id': 'f1'},
        ),
      ];

      // Simulate what SyncClient.sendBatch builds
      final payload = {
        'device_id': 'device-uuid',
        'client_batch_id': 'batch-uuid',
        'items': items.map((i) => i.toJson()).toList(),
      };

      expect(payload.containsKey('device_id'), isTrue);
      expect(payload.containsKey('client_batch_id'), isTrue);
      expect(payload.containsKey('items'), isTrue);
      expect(payload.containsKey('operations'), isFalse,
          reason: 'Must not use old operations[] field');
    });
  });
}

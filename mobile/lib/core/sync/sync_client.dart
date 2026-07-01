import '../network/api_client.dart';
import '../utils/device_utils.dart';
import '../config/app_config.dart';

/// Sync batch client aligned to P2-7 canonical payload.
/// Uses items[] / action — NOT operations[] / operation_type.
/// Reference: API-GAP-P2-7-011.
///
/// client_id limitation: backend may lack physical client_id column.
/// Reference: API-GAP-P2-7-017 / MOBILE-GAP-P2-8-015.
class SyncClient {
  final ApiClient apiClient;

  SyncClient({required this.apiClient});

  /// Send a sync batch. Payload follows P2-7 canonical shape.
  Future<Map<String, dynamic>> sendBatch(List<SyncItem> items) async {
    final deviceId = await getOrCreateDeviceId();
    final clientBatchId = newUuid();

    final payload = {
      'device_id': deviceId,
      'client_batch_id': clientBatchId,
      'items': items.map((i) => i.toJson()).toList(),
    };

    AppConfig.log('Sync batch: ${items.length} items, batch=$clientBatchId');
    final resp = await apiClient.post('/sync/batch', body: payload);
    return resp;
  }
}

/// A single sync item in the canonical P2-7 format.
class SyncItem {
  final String clientId;
  final String
      entityType; // notebook_entry | note_item | follow_up | notification | upload_queue
  final String action; // create | update | delete
  final Map<String, dynamic> payload;

  const SyncItem({
    required this.clientId,
    required this.entityType,
    required this.action,
    required this.payload,
  });

  Map<String, dynamic> toJson() => {
        'client_id': clientId,
        'entity_type': entityType,
        'action': action,
        'payload': payload,
      };
}

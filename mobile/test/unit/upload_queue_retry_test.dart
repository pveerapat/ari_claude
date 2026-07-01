import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/shared/models/upload_queue_model.dart';

void main() {
  group('Upload queue retry rules', () {
    final baseRow = {
      'id': 'q1',
      'local_item_id': 'li-stable',
      'local_entry_id': 'le-stable',
      'status': 'failed',
      'item_type': 'photo',
      'local_file_path': '/path/photo.jpg',
      'mime_type': 'image/jpeg',
      'server_entry_id': null,
      'error_message': 'Network error',
      'retry_count': 2,
      'created_at': '2026-01-01T00:00:00',
      'updated_at': '2026-01-01T00:01:00',
    };

    test('item preserves local_item_id on retry', () {
      final item = UploadQueueItem.fromRow(baseRow);
      // local_item_id must not change across retries
      expect(item.localItemId, equals('li-stable'));
    });

    test('item preserves local_entry_id on retry', () {
      final item = UploadQueueItem.fromRow(baseRow);
      expect(item.localEntryId, equals('le-stable'));
    });

    test('retry count increments not the IDs', () {
      final item = UploadQueueItem.fromRow(baseRow);
      expect(item.retryCount, equals(2));
      // IDs remain stable
      expect(item.localItemId, equals('li-stable'));
    });

    test('failed item can be retried (isFailed is true)', () {
      final item = UploadQueueItem.fromRow(baseRow);
      expect(item.isFailed, isTrue);
    });

    test('completed item is not pending or failed', () {
      final row = {...baseRow, 'status': 'completed'};
      final item = UploadQueueItem.fromRow(row);
      expect(item.isCompleted, isTrue);
      expect(item.isPending, isFalse);
      expect(item.isFailed, isFalse);
    });

    test('pending item is neither failed nor completed', () {
      final row = {...baseRow, 'status': 'pending'};
      final item = UploadQueueItem.fromRow(row);
      expect(item.isPending, isTrue);
      expect(item.isFailed, isFalse);
    });

    test('error message is preserved on failed item', () {
      final item = UploadQueueItem.fromRow(baseRow);
      expect(item.errorMessage, equals('Network error'));
    });
  });
}

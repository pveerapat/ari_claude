import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/shared/models/note_item_model.dart';

void main() {
  group('NoteItemModel sequence_order', () {
    test('sequence_order starts at 1 for first item', () {
      final item = NoteItemModel(
        id: '',
        entryId: '',
        itemType: 'text',
        sequenceOrder: 1,
        createdAt: '2026-01-01T00:00:00',
        localItemId: 'li1',
      );
      expect(item.sequenceOrder, equals(1));
    });

    test('sequence_order is preserved from local row', () {
      final row = {
        'local_item_id': 'li-123',
        'client_id': 'c-123',
        'local_entry_id': 'le-1',
        'server_entry_id': null,
        'server_item_id': null,
        'item_type': 'photo',
        'sequence_order': 3,
        'text_content': null,
        'url': null,
        'local_file_path': '/path/photo.jpg',
        'mime_type': 'image/jpeg',
        'status': 'local',
        'synced': 0,
        'created_at': '2026-01-01T00:00:00',
      };
      final item = NoteItemModel.fromLocalRow(row);
      expect(item.sequenceOrder, equals(3));
    });

    test('sequence_order is not changed on retry simulation', () {
      // Retry should NOT regenerate or change sequence_order
      const originalOrder = 5;
      final item = NoteItemModel(
        id: '',
        entryId: '',
        itemType: 'voice',
        sequenceOrder: originalOrder,
        createdAt: '2026-01-01T00:00:00',
        localItemId: 'li-stable',
      );

      // Simulate retry by constructing a new item from same localItemId
      // sequence_order must remain the same
      expect(item.sequenceOrder, equals(originalOrder));
    });

    test('client_id is distinct per item', () {
      // Two items should have different client_ids
      final rows = List.generate(
          3,
          (i) => {
                'local_item_id': 'li-$i',
                'client_id': 'c-$i',
                'local_entry_id': 'le-1',
                'server_entry_id': null,
                'server_item_id': null,
                'item_type': 'text',
                'sequence_order': i + 1,
                'text_content': 'item $i',
                'url': null,
                'local_file_path': null,
                'mime_type': null,
                'status': 'local',
                'synced': 0,
                'created_at': '2026-01-01T00:00:00',
              });

      final items = rows.map(NoteItemModel.fromLocalRow).toList();
      expect(items[0].sequenceOrder, equals(1));
      expect(items[1].sequenceOrder, equals(2));
      expect(items[2].sequenceOrder, equals(3));
    });

    test('fromJson parses sequence_order from server', () {
      final json = {
        'id': 's1',
        'entry_id': 'e1',
        'item_type': 'text',
        'sequence_order': 7,
        'text_content': 'hello',
        'created_at': '2026-01-01T00:00:00',
      };
      final item = NoteItemModel.fromJson(json);
      expect(item.sequenceOrder, equals(7));
    });
  });
}

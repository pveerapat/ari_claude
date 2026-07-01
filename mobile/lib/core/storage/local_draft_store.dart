import 'package:sqflite/sqflite.dart';
import 'local_database.dart';

/// CRUD for local notebook drafts and note items.
/// Preserves client_id, local_id, local_item_id, sequence_order on retry.
class LocalDraftStore {
  Future<void> saveEntry(Map<String, dynamic> entry) async {
    final db = await LocalDatabase.instance;
    await db.insert(
      'local_notebook_entries',
      entry,
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<Map<String, dynamic>>> listEntries({String? farmId}) async {
    final db = await LocalDatabase.instance;
    if (farmId != null) {
      return db.query(
        'local_notebook_entries',
        where: 'farm_id = ?',
        whereArgs: [farmId],
        orderBy: 'created_at DESC',
      );
    }
    return db.query('local_notebook_entries', orderBy: 'created_at DESC');
  }

  Future<Map<String, dynamic>?> getEntry(String localId) async {
    final db = await LocalDatabase.instance;
    final rows = await db.query(
      'local_notebook_entries',
      where: 'local_id = ?',
      whereArgs: [localId],
      limit: 1,
    );
    return rows.isEmpty ? null : rows.first;
  }

  Future<void> updateEntryServerId(String localId, String serverId) async {
    final db = await LocalDatabase.instance;
    await db.update(
      'local_notebook_entries',
      {'server_id': serverId, 'synced': 1, 'status': 'uploaded'},
      where: 'local_id = ?',
      whereArgs: [localId],
    );
    await _saveMapping(localId, serverId, 'notebook_entry');
  }

  Future<void> saveItem(Map<String, dynamic> item) async {
    final db = await LocalDatabase.instance;
    await db.insert(
      'local_note_items',
      item,
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<Map<String, dynamic>>> listItems(String localEntryId) async {
    final db = await LocalDatabase.instance;
    return db.query(
      'local_note_items',
      where: 'local_entry_id = ?',
      whereArgs: [localEntryId],
      orderBy: 'sequence_order ASC',
    );
  }

  Future<int> nextSequenceOrder(String localEntryId) async {
    final items = await listItems(localEntryId);
    if (items.isEmpty) return 1;
    return (items
            .map((e) => e['sequence_order'] as int)
            .reduce((a, b) => a > b ? a : b)) +
        1;
  }

  Future<void> updateItemServerId(
      String localItemId, String serverItemId) async {
    final db = await LocalDatabase.instance;
    await db.update(
      'local_note_items',
      {'server_item_id': serverItemId, 'synced': 1, 'status': 'uploaded'},
      where: 'local_item_id = ?',
      whereArgs: [localItemId],
    );
    await _saveMapping(localItemId, serverItemId, 'note_item');
  }

  Future<void> _saveMapping(
      String localId, String serverId, String entityType) async {
    final db = await LocalDatabase.instance;
    await db.insert(
      'id_mappings',
      {
        'local_id': localId,
        'server_id': serverId,
        'entity_type': entityType,
        'created_at': DateTime.now().toIso8601String(),
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<String?> serverIdFor(String localId, String entityType) async {
    final db = await LocalDatabase.instance;
    final rows = await db.query(
      'id_mappings',
      where: 'local_id = ? AND entity_type = ?',
      whereArgs: [localId, entityType],
      limit: 1,
    );
    return rows.isEmpty ? null : rows.first['server_id'] as String?;
  }
}

import 'local_database.dart';
import 'package:sqflite/sqflite.dart';

enum UploadStatus { pending, uploading, failed, completed }

/// Local upload queue — persists across app restarts.
/// client_id, local_item_id, sequence_order are never changed on retry.
class UploadQueueStore {
  Future<void> enqueue(Map<String, dynamic> item) async {
    final db = await LocalDatabase.instance;
    await db.insert(
      'upload_queue',
      item,
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<Map<String, dynamic>>> listByStatus(UploadStatus status) async {
    final db = await LocalDatabase.instance;
    return db.query(
      'upload_queue',
      where: 'status = ?',
      whereArgs: [status.name],
      orderBy: 'created_at ASC',
    );
  }

  Future<List<Map<String, dynamic>>> listPendingAndFailed() async {
    final db = await LocalDatabase.instance;
    return db.query(
      'upload_queue',
      where: "status IN ('pending', 'failed')",
      orderBy: 'created_at ASC',
    );
  }

  Future<List<Map<String, dynamic>>> listAll() async {
    final db = await LocalDatabase.instance;
    return db.query('upload_queue', orderBy: 'created_at DESC');
  }

  Future<void> markUploading(String id) async {
    await _updateStatus(id, UploadStatus.uploading);
  }

  Future<void> markCompleted(String id) async {
    await _updateStatus(id, UploadStatus.completed);
  }

  Future<void> markFailed(String id, String? error) async {
    final db = await LocalDatabase.instance;
    await db.update(
      'upload_queue',
      {
        'status': UploadStatus.failed.name,
        'error_message': error,
        'updated_at': DateTime.now().toIso8601String(),
      },
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<void> incrementRetry(String id) async {
    final db = await LocalDatabase.instance;
    await db.rawUpdate(
      'UPDATE upload_queue SET retry_count = retry_count + 1, status = ?, updated_at = ? WHERE id = ?',
      [UploadStatus.pending.name, DateTime.now().toIso8601String(), id],
    );
  }

  Future<void> _updateStatus(String id, UploadStatus status) async {
    final db = await LocalDatabase.instance;
    await db.update(
      'upload_queue',
      {'status': status.name, 'updated_at': DateTime.now().toIso8601String()},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<Map<String, dynamic>?> get(String id) async {
    final db = await LocalDatabase.instance;
    final rows = await db.query(
      'upload_queue',
      where: 'id = ?',
      whereArgs: [id],
      limit: 1,
    );
    return rows.isEmpty ? null : rows.first;
  }

  Future<void> updateServerEntryId(String queueId, String serverEntryId) async {
    final db = await LocalDatabase.instance;
    await db.update(
      'upload_queue',
      {
        'server_entry_id': serverEntryId,
        'updated_at': DateTime.now().toIso8601String()
      },
      where: 'id = ?',
      whereArgs: [queueId],
    );
  }
}

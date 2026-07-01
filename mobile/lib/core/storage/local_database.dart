import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

/// Singleton SQLite database for ARI offline storage.
/// Stores: local notebook drafts, note items, upload queue, ID mappings.
class LocalDatabase {
  static Database? _db;

  static Future<Database> get instance async {
    _db ??= await _open();
    return _db!;
  }

  static Future<Database> _open() async {
    final path = join(await getDatabasesPath(), 'ari_mobile.db');
    return openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }

  static Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE local_notebook_entries (
        local_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        server_id TEXT,
        farm_id TEXT,
        zone_id TEXT,
        tree_id TEXT,
        entry_type TEXT NOT NULL DEFAULT 'note',
        title TEXT,
        summary TEXT,
        status TEXT NOT NULL DEFAULT 'local',
        synced INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    ''');

    await db.execute('''
      CREATE TABLE local_note_items (
        local_item_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        server_item_id TEXT,
        local_entry_id TEXT NOT NULL,
        server_entry_id TEXT,
        item_type TEXT NOT NULL,
        sequence_order INTEGER NOT NULL,
        text_content TEXT,
        url TEXT,
        local_file_path TEXT,
        server_file_id TEXT,
        mime_type TEXT,
        status TEXT NOT NULL DEFAULT 'local',
        synced INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (local_entry_id) REFERENCES local_notebook_entries(local_id)
      )
    ''');

    await db.execute('''
      CREATE TABLE upload_queue (
        id TEXT PRIMARY KEY,
        local_item_id TEXT,
        local_entry_id TEXT,
        status TEXT NOT NULL DEFAULT 'pending',
        item_type TEXT,
        local_file_path TEXT,
        mime_type TEXT,
        server_entry_id TEXT,
        error_message TEXT,
        retry_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    ''');

    await db.execute('''
      CREATE TABLE id_mappings (
        local_id TEXT NOT NULL,
        server_id TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY (local_id, entity_type)
      )
    ''');

    await db.execute('''
      CREATE TABLE sync_history (
        batch_id TEXT PRIMARY KEY,
        device_id TEXT NOT NULL,
        status TEXT NOT NULL,
        item_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
      )
    ''');
  }
}

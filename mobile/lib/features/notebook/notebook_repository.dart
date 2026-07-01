import '../../core/network/api_client.dart';
import '../../core/storage/local_draft_store.dart';
import '../../core/storage/upload_queue_store.dart';
import '../../core/utils/device_utils.dart';
import '../../shared/models/notebook_entry_model.dart';
import '../../shared/models/note_item_model.dart';

class NotebookRepository {
  final ApiClient apiClient;
  final LocalDraftStore draftStore;
  final UploadQueueStore uploadQueue;

  NotebookRepository({
    required this.apiClient,
    required this.draftStore,
    required this.uploadQueue,
  });

  // ─── Remote ──────────────────────────────────────────────────────────────

  Future<List<NotebookEntryModel>> listServerEntries({String? farmId}) async {
    final query = farmId != null ? '?farm_id=$farmId' : '';
    final resp = await apiClient.get('/notebook-entries$query');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List) {
      return data
          .map((e) => NotebookEntryModel.fromJson(e as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  Future<NotebookEntryModel> getServerEntry(String entryId) async {
    final resp = await apiClient.get('/notebook-entries/$entryId');
    final data = resp['data'] ?? resp;
    return NotebookEntryModel.fromJson(data as Map<String, dynamic>);
  }

  Future<NotebookEntryModel> createServerEntry(NotebookEntryModel entry) async {
    final resp = await apiClient.post('/notebook-entries',
        body: entry.toCreatePayload());
    final data = resp['data'] ?? resp;
    return NotebookEntryModel.fromJson(data as Map<String, dynamic>);
  }

  Future<List<NoteItemModel>> listServerItems(String entryId) async {
    final resp = await apiClient.get('/notebook-entries/$entryId/items');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List) {
      return data
          .map((e) => NoteItemModel.fromJson(e as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  Future<NoteItemModel> createServerItem(
    String entryId,
    NoteItemModel item,
  ) async {
    final resp = await apiClient.post(
      '/notebook-entries/$entryId/items',
      body: item.toCreatePayload(),
    );
    final data = resp['data'] ?? resp;
    return NoteItemModel.fromJson(data as Map<String, dynamic>);
  }

  // ─── Local draft ─────────────────────────────────────────────────────────

  Future<String> saveLocalDraft({
    required String entryType,
    String? farmId,
    String? zoneId,
    String? treeId,
    String? title,
    String? summary,
  }) async {
    final localId = newUuid();
    final clientId = newUuid();
    final now = DateTime.now().toIso8601String();
    await draftStore.saveEntry({
      'local_id': localId,
      'client_id': clientId,
      'farm_id': farmId,
      'zone_id': zoneId,
      'tree_id': treeId,
      'entry_type': entryType,
      'title': title,
      'summary': summary,
      'status': 'local',
      'synced': 0,
      'created_at': now,
      'updated_at': now,
    });
    return localId;
  }

  Future<String> saveLocalItem({
    required String localEntryId,
    required String itemType,
    String? textContent,
    String? url,
    String? localFilePath,
    String? mimeType,
  }) async {
    final localItemId = newUuid();
    final clientId = newUuid();
    final sequenceOrder = await draftStore.nextSequenceOrder(localEntryId);
    final now = DateTime.now().toIso8601String();

    await draftStore.saveItem({
      'local_item_id': localItemId,
      'client_id': clientId,
      'local_entry_id': localEntryId,
      'item_type': itemType,
      'sequence_order': sequenceOrder,
      'text_content': textContent,
      'url': url,
      'local_file_path': localFilePath,
      'mime_type': mimeType,
      'status': 'local',
      'synced': 0,
      'created_at': now,
    });

    // Enqueue for upload if it has a file
    if (localFilePath != null) {
      final queueId = newUuid();
      final queueNow = DateTime.now().toIso8601String();
      await uploadQueue.enqueue({
        'id': queueId,
        'local_item_id': localItemId,
        'local_entry_id': localEntryId,
        'status': 'pending',
        'item_type': itemType,
        'local_file_path': localFilePath,
        'mime_type': mimeType,
        'retry_count': 0,
        'created_at': queueNow,
        'updated_at': queueNow,
      });
    }

    return localItemId;
  }

  Future<List<NotebookEntryModel>> listLocalDrafts({String? farmId}) async {
    final rows = await draftStore.listEntries(farmId: farmId);
    return rows.map(NotebookEntryModel.fromLocalDraft).toList();
  }

  Future<List<NoteItemModel>> listLocalItems(String localEntryId) async {
    final rows = await draftStore.listItems(localEntryId);
    return rows.map(NoteItemModel.fromLocalRow).toList();
  }
}

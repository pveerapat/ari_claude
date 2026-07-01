import 'dart:io';
import '../../shared/models/upload_queue_model.dart';
import '../network/api_client.dart';
import '../storage/upload_queue_store.dart';

/// Manages file upload flow:
/// 1. Save local file
/// 2. POST /api/v1/files/upload-url
/// 3. PUT binary to MinIO presigned URL
/// 4. POST /api/v1/files/complete
/// 5. Mark queue item completed
/// 6. On failure: POST /api/v1/files/upload-failed if fields available
///
/// MOBILE-GAP-P2-8-003: Object key format and file-to-note-item binding.
/// MOBILE-GAP-P2-8-004: Media read URL for mobile preview.
class UploadManager {
  final ApiClient apiClient;
  final UploadQueueStore queueStore;

  UploadManager({required this.apiClient, required this.queueStore});

  /// Process all pending/failed queue items.
  Future<void> processQueue() async {
    final items = await queueStore.listPendingAndFailed();
    for (final row in items) {
      final item = UploadQueueItem.fromRow(row);
      await _uploadItem(item);
    }
  }

  /// Upload a single queue item.
  Future<bool> _uploadItem(UploadQueueItem item) async {
    if (item.localFilePath == null) return false;
    final file = File(item.localFilePath!);
    if (!await file.exists()) {
      await queueStore.markFailed(item.id, 'Local file not found');
      return false;
    }

    await queueStore.markUploading(item.id);
    try {
      // Step 1: Request presigned URL
      final urlResp = await apiClient.post('/files/upload-url', body: {
        'filename': file.path.split('/').last,
        'content_type': item.mimeType ?? 'application/octet-stream',
        if (item.serverEntryId != null) 'notebook_entry_id': item.serverEntryId,
      });

      final presignedUrl = urlResp['upload_url']?.toString();
      final fileId =
          urlResp['file_id']?.toString() ?? urlResp['id']?.toString();
      final objectKey = urlResp['object_key']?.toString();

      if (presignedUrl == null) {
        await queueStore.markFailed(item.id, 'No presigned URL returned');
        return false;
      }

      // Step 2: Upload binary to MinIO
      final bytes = await file.readAsBytes();
      await apiClient.putBinary(
          presignedUrl, bytes, item.mimeType ?? 'application/octet-stream');

      // Step 3: Complete upload
      await apiClient.post('/files/complete', body: {
        if (fileId != null) 'file_id': fileId,
        if (objectKey != null) 'object_key': objectKey,
        if (item.serverEntryId != null) 'notebook_entry_id': item.serverEntryId,
        if (item.localItemId != null) 'note_item_id': item.localItemId,
      });

      await queueStore.markCompleted(item.id);
      return true;
    } catch (e) {
      await _reportFailure(item, e.toString());
      return false;
    }
  }

  Future<void> _reportFailure(UploadQueueItem item, String error) async {
    await queueStore.markFailed(item.id, error);
    try {
      await apiClient.post('/files/upload-failed', body: {
        if (item.localItemId != null) 'local_item_id': item.localItemId,
        'error_message': error,
      });
    } catch (_) {
      // Best-effort failure reporting
    }
    await queueStore.incrementRetry(item.id);
  }

  /// Retry a specific failed queue item.
  Future<bool> retry(String queueId) async {
    final row = await queueStore.get(queueId);
    if (row == null) return false;
    // Reset to pending so processQueue picks it up
    await queueStore.incrementRetry(queueId);
    final item = UploadQueueItem.fromRow(row);
    return _uploadItem(item);
  }
}

/// Upload queue item — mirrors upload_queue table.
/// Used for displaying pending/failed/retry state in the upload queue UI.
class UploadQueueItem {
  final String id;
  final String? localItemId;
  final String? localEntryId;
  final String status; // pending | uploading | failed | completed
  final String? itemType;
  final String? localFilePath;
  final String? mimeType;
  final String? serverEntryId;
  final String? errorMessage;
  final int retryCount;
  final String createdAt;
  final String updatedAt;

  const UploadQueueItem({
    required this.id,
    this.localItemId,
    this.localEntryId,
    required this.status,
    this.itemType,
    this.localFilePath,
    this.mimeType,
    this.serverEntryId,
    this.errorMessage,
    required this.retryCount,
    required this.createdAt,
    required this.updatedAt,
  });

  factory UploadQueueItem.fromRow(Map<String, dynamic> row) => UploadQueueItem(
        id: row['id']?.toString() ?? '',
        localItemId: row['local_item_id']?.toString(),
        localEntryId: row['local_entry_id']?.toString(),
        status: row['status']?.toString() ?? 'pending',
        itemType: row['item_type']?.toString(),
        localFilePath: row['local_file_path']?.toString(),
        mimeType: row['mime_type']?.toString(),
        serverEntryId: row['server_entry_id']?.toString(),
        errorMessage: row['error_message']?.toString(),
        retryCount: (row['retry_count'] as int?) ?? 0,
        createdAt: row['created_at']?.toString() ?? '',
        updatedAt: row['updated_at']?.toString() ?? '',
      );

  bool get isPending => status == 'pending';
  bool get isFailed => status == 'failed';
  bool get isUploading => status == 'uploading';
  bool get isCompleted => status == 'completed';
}

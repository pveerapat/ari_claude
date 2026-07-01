/// Note Item = Timeline Item (P0 domain rule).
/// Supported types: photo | video | voice | text | file | link.
/// sequence_order must be preserved — never changed on retry.
class NoteItemModel {
  final String id;
  final String entryId;
  final String itemType; // photo | video | voice | text | file | link
  final int sequenceOrder;
  final String? textContent;
  final String? url;
  final String? localFilePath;
  final String? serverFileId;
  final String? mimeType;
  final String createdAt;

  // Local-only fields
  final String? localItemId;
  final String? localEntryId;
  final bool isLocalOnly;
  final String localStatus; // local | uploading | uploaded | failed

  const NoteItemModel({
    required this.id,
    required this.entryId,
    required this.itemType,
    required this.sequenceOrder,
    this.textContent,
    this.url,
    this.localFilePath,
    this.serverFileId,
    this.mimeType,
    required this.createdAt,
    this.localItemId,
    this.localEntryId,
    this.isLocalOnly = false,
    this.localStatus = 'uploaded',
  });

  factory NoteItemModel.fromJson(Map<String, dynamic> json) => NoteItemModel(
        id: json['id']?.toString() ?? '',
        entryId: json['entry_id']?.toString() ?? '',
        itemType: json['item_type']?.toString() ?? 'text',
        sequenceOrder: (json['sequence_order'] as num?)?.toInt() ?? 1,
        textContent: json['text_content']?.toString(),
        url: json['url']?.toString(),
        mimeType: json['mime_type']?.toString(),
        createdAt:
            json['created_at']?.toString() ?? DateTime.now().toIso8601String(),
      );

  factory NoteItemModel.fromLocalRow(Map<String, dynamic> row) => NoteItemModel(
        id: row['server_item_id']?.toString() ?? '',
        entryId: row['server_entry_id']?.toString() ?? '',
        itemType: row['item_type']?.toString() ?? 'text',
        sequenceOrder: (row['sequence_order'] as int?) ?? 1,
        textContent: row['text_content']?.toString(),
        url: row['url']?.toString(),
        localFilePath: row['local_file_path']?.toString(),
        mimeType: row['mime_type']?.toString(),
        createdAt: row['created_at']?.toString() ?? '',
        localItemId: row['local_item_id']?.toString(),
        localEntryId: row['local_entry_id']?.toString(),
        isLocalOnly: (row['synced'] as int? ?? 0) == 0,
        localStatus: row['status']?.toString() ?? 'local',
      );

  Map<String, dynamic> toCreatePayload() => {
        'item_type': itemType,
        'sequence_order': sequenceOrder,
        if (textContent != null) 'text_content': textContent,
        if (url != null) 'url': url,
        if (mimeType != null) 'mime_type': mimeType,
      };
}

/// Notebook Entry = Note Session (P0 domain rule).
/// Supported types: note | consultation.
class NotebookEntryModel {
  final String id;
  final String entryType; // note | consultation
  final String? farmId;
  final String? zoneId;
  final String? treeId;
  final String? title;
  final String? summary;
  final String? analysisStatus;
  final String createdAt;
  final String? updatedAt;

  // Local-only fields (not from server)
  final String? localId;
  final bool isLocalOnly;
  final String localStatus; // local | uploading | uploaded | failed

  const NotebookEntryModel({
    required this.id,
    required this.entryType,
    this.farmId,
    this.zoneId,
    this.treeId,
    this.title,
    this.summary,
    this.analysisStatus,
    required this.createdAt,
    this.updatedAt,
    this.localId,
    this.isLocalOnly = false,
    this.localStatus = 'uploaded',
  });

  factory NotebookEntryModel.fromJson(Map<String, dynamic> json) =>
      NotebookEntryModel(
        id: json['id']?.toString() ?? '',
        entryType: json['entry_type']?.toString() ?? 'note',
        farmId: json['farm_id']?.toString(),
        zoneId: json['zone_id']?.toString(),
        treeId: json['tree_id']?.toString(),
        title: json['title']?.toString(),
        summary: json['summary']?.toString(),
        analysisStatus: json['analysis_status']?.toString(),
        createdAt:
            json['created_at']?.toString() ?? DateTime.now().toIso8601String(),
        updatedAt: json['updated_at']?.toString(),
      );

  factory NotebookEntryModel.fromLocalDraft(Map<String, dynamic> row) =>
      NotebookEntryModel(
        id: row['server_id']?.toString() ?? '',
        entryType: row['entry_type']?.toString() ?? 'note',
        farmId: row['farm_id']?.toString(),
        zoneId: row['zone_id']?.toString(),
        treeId: row['tree_id']?.toString(),
        title: row['title']?.toString(),
        summary: row['summary']?.toString(),
        createdAt: row['created_at']?.toString() ?? '',
        localId: row['local_id']?.toString(),
        isLocalOnly: (row['synced'] as int? ?? 0) == 0,
        localStatus: row['status']?.toString() ?? 'local',
      );

  Map<String, dynamic> toCreatePayload() => {
        'entry_type': entryType,
        if (farmId != null) 'farm_id': farmId,
        if (zoneId != null) 'zone_id': zoneId,
        if (treeId != null) 'tree_id': treeId,
        if (title != null) 'title': title,
        if (summary != null) 'summary': summary,
      };
}

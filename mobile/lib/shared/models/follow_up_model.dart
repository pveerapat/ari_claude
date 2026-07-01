/// Follow-Up model — 3 / 7 / 14 day periods.
/// Outcome values follow frozen domain: improved | same | worse | unknown.
class FollowUpModel {
  final String id;
  final String? notebookEntryId;
  final int? followUpDay; // 3 | 7 | 14
  final String? outcome; // improved | same | worse | unknown
  final String? notes;
  final String? status;
  final String? dueDate;
  final String createdAt;

  const FollowUpModel({
    required this.id,
    this.notebookEntryId,
    this.followUpDay,
    this.outcome,
    this.notes,
    this.status,
    this.dueDate,
    required this.createdAt,
  });

  factory FollowUpModel.fromJson(Map<String, dynamic> json) => FollowUpModel(
        id: json['id']?.toString() ?? '',
        notebookEntryId: json['notebook_entry_id']?.toString(),
        followUpDay: (json['follow_up_day'] as num?)?.toInt(),
        outcome: json['outcome']?.toString(),
        notes: json['notes']?.toString(),
        status: json['status']?.toString(),
        dueDate: json['due_date']?.toString(),
        createdAt:
            json['created_at']?.toString() ?? DateTime.now().toIso8601String(),
      );

  static const List<String> outcomeValues = [
    'improved',
    'same',
    'worse',
    'unknown'
  ];
  static const List<int> followUpDays = [3, 7, 14];
}

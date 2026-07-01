class NotificationModel {
  final String id;
  final String? message;
  final bool isRead;
  final String? notificationType;
  final String createdAt;

  const NotificationModel({
    required this.id,
    this.message,
    required this.isRead,
    this.notificationType,
    required this.createdAt,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) =>
      NotificationModel(
        id: json['id']?.toString() ?? '',
        message: json['message']?.toString(),
        isRead: json['is_read'] == true || json['is_read'] == 1,
        notificationType: json['notification_type']?.toString(),
        createdAt:
            json['created_at']?.toString() ?? DateTime.now().toIso8601String(),
      );
}

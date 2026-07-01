import '../../core/network/api_client.dart';
import '../../shared/models/notification_model.dart';

class NotificationRepository {
  final ApiClient apiClient;
  NotificationRepository({required this.apiClient});

  Future<List<NotificationModel>> listNotifications() async {
    final resp = await apiClient.get('/notifications');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List) {
      return data
          .map((e) => NotificationModel.fromJson(e as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  Future<NotificationModel> getNotification(String id) async {
    final resp = await apiClient.get('/notifications/$id');
    final data = resp['data'] ?? resp;
    return NotificationModel.fromJson(data as Map<String, dynamic>);
  }

  Future<void> markRead(String id) async {
    await apiClient.patch('/notifications/$id/read');
  }

  Future<void> markAllRead() async {
    await apiClient.post('/notifications/mark-all-read');
  }
}

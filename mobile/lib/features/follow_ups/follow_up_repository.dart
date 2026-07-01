import '../../core/network/api_client.dart';
import '../../shared/models/follow_up_model.dart';

class FollowUpRepository {
  final ApiClient apiClient;
  FollowUpRepository({required this.apiClient});

  Future<List<FollowUpModel>> listFollowUps() async {
    final resp = await apiClient.get('/follow-ups');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List) {
      return data
          .map((e) => FollowUpModel.fromJson(e as Map<String, dynamic>))
          .toList();
    }
    return [];
  }

  Future<FollowUpModel> getFollowUp(String followUpId) async {
    final resp = await apiClient.get('/follow-ups/$followUpId');
    final data = resp['data'] ?? resp;
    return FollowUpModel.fromJson(data as Map<String, dynamic>);
  }

  Future<FollowUpModel> updateOutcome(String followUpId, String outcome) async {
    final resp = await apiClient.patch('/follow-ups/$followUpId', body: {
      'outcome': outcome,
    });
    final data = resp['data'] ?? resp;
    return FollowUpModel.fromJson(data as Map<String, dynamic>);
  }
}

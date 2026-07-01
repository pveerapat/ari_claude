import '../../core/network/api_client.dart';
import '../../shared/models/farm_model.dart';

class FarmRepository {
  final ApiClient apiClient;
  FarmRepository({required this.apiClient});

  Future<List<FarmModel>> listFarms() async {
    final resp = await apiClient.get('/farms');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List)
      return data
          .map((e) => FarmModel.fromJson(e as Map<String, dynamic>))
          .toList();
    return [];
  }

  Future<FarmModel> getFarm(String farmId) async {
    final resp = await apiClient.get('/farms/$farmId');
    final data = resp['data'] ?? resp;
    return FarmModel.fromJson(data as Map<String, dynamic>);
  }

  Future<FarmModel> createFarm({
    required String name,
    String? description,
    String? location,
  }) async {
    final resp = await apiClient.post('/farms', body: {
      'farm_name': name,
      if (description != null) 'description': description,
      if (location != null) 'location': {'address': location},
    });
    final data = resp['data'] ?? resp;
    return FarmModel.fromJson(data as Map<String, dynamic>);
  }

  Future<List<ZoneModel>> listZones(String farmId) async {
    final resp = await apiClient.get('/zones?farm_id=$farmId');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List)
      return data
          .map((e) => ZoneModel.fromJson(e as Map<String, dynamic>))
          .toList();
    return [];
  }

  Future<ZoneModel> createZone({
    required String farmId,
    required String name,
    String? description,
    String? zoneType,
  }) async {
    final resp = await apiClient.post('/zones', body: {
      'farm_id': farmId,
      'name': name,
      if (description != null) 'description': description,
      if (zoneType != null) 'zone_type': zoneType,
    });
    final data = resp['data'] ?? resp;
    return ZoneModel.fromJson(data as Map<String, dynamic>);
  }

  Future<List<TreeModel>> listTrees({String? farmId, String? zoneId}) async {
    final params = <String>[];
    if (farmId != null) params.add('farm_id=$farmId');
    if (zoneId != null) params.add('zone_id=$zoneId');
    final query = params.isNotEmpty ? '?${params.join('&')}' : '';
    final resp = await apiClient.get('/trees$query');
    final data = resp['data'] ?? resp['items'] ?? resp;
    if (data is List)
      return data
          .map((e) => TreeModel.fromJson(e as Map<String, dynamic>))
          .toList();
    return [];
  }

  Future<TreeModel> createTree({
    required String zoneId,
    required String farmId,
    String? label,
    String? species,
  }) async {
    final resp = await apiClient.post('/trees', body: {
      'zone_id': zoneId,
      'farm_id': farmId,
      if (label != null) 'label': label,
      if (species != null) 'species': species,
    });
    final data = resp['data'] ?? resp;
    return TreeModel.fromJson(data as Map<String, dynamic>);
  }
}

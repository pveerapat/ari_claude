import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/farm_model.dart';

const _kActiveFarmKey = 'ari_active_farm_id';

/// Manages the currently selected farm context.
/// Farm Selector behavior per P2-8 §14.1:
/// - Uses primary_farm_id as default if available.
/// - Falls back to first accessible farm only if safe.
///
/// MOBILE-GAP-P2-8-002: Default farm behavior when primary_farm_id is null
/// and multiple farms exist. Current behavior: use first farm from list.
class FarmContextProvider extends ChangeNotifier {
  FarmModel? _activeFarm;
  List<FarmModel> _farms = [];
  bool _loading = false;

  FarmModel? get activeFarm => _activeFarm;
  List<FarmModel> get farms => _farms;
  bool get loading => _loading;
  bool get hasFarm => _activeFarm != null;

  Future<void> init(List<FarmModel> farms, String? primaryFarmId) async {
    _loading = true;
    notifyListeners();

    _farms = farms;
    final prefs = await SharedPreferences.getInstance();
    final savedId = prefs.getString(_kActiveFarmKey);

    // Priority: saved context → primary_farm_id → first in list
    FarmModel? selected;
    if (savedId != null) {
      selected = farms.where((f) => f.id == savedId).firstOrNull;
    }
    selected ??= farms.where((f) => f.id == primaryFarmId).firstOrNull;
    selected ??= farms.firstOrNull;

    _activeFarm = selected;
    _loading = false;
    notifyListeners();
  }

  Future<void> setActiveFarm(FarmModel farm) async {
    _activeFarm = farm;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kActiveFarmKey, farm.id);
    notifyListeners();
  }

  void updateFarms(List<FarmModel> farms) {
    _farms = farms;
    if (_activeFarm != null && !farms.any((f) => f.id == _activeFarm!.id)) {
      _activeFarm = farms.firstOrNull;
    }
    notifyListeners();
  }

  void clear() {
    _activeFarm = null;
    _farms = [];
    notifyListeners();
  }
}

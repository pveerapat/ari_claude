import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

const _kDeviceIdKey = 'ari_device_id';

/// Returns a stable UUID for this device installation.
/// Generated once, persisted in SharedPreferences.
Future<String> getOrCreateDeviceId() async {
  final prefs = await SharedPreferences.getInstance();
  var id = prefs.getString(_kDeviceIdKey);
  if (id == null) {
    id = const Uuid().v4();
    await prefs.setString(_kDeviceIdKey, id);
  }
  return id;
}

/// Generate a new random UUID.
String newUuid() => const Uuid().v4();

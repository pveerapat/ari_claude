import 'package:permission_handler/permission_handler.dart';

enum AriPermission { camera, microphone, location, photos, notifications }

/// Thin wrapper over permission_handler.
/// Mobile must not treat OS permission as backend authorization.
class PermissionService {
  Future<bool> request(AriPermission permission) async {
    final status = await _permissionFor(permission).request();
    return status.isGranted;
  }

  Future<bool> isGranted(AriPermission permission) async {
    return (await _permissionFor(permission).status).isGranted;
  }

  Future<void> openSettings() => openAppSettings();

  Permission _permissionFor(AriPermission p) {
    switch (p) {
      case AriPermission.camera:
        return Permission.camera;
      case AriPermission.microphone:
        return Permission.microphone;
      case AriPermission.location:
        return Permission.locationWhenInUse;
      case AriPermission.photos:
        return Permission.photos;
      case AriPermission.notifications:
        return Permission.notification;
    }
  }
}

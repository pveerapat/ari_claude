import 'package:flutter/material.dart';
import '../../core/permissions/permission_service.dart';

/// Permission onboarding screen — requests camera, microphone, location,
/// photos, notifications after registration.
/// If denied, app continues with feature-level fallbacks.
/// Mobile permission ≠ backend authorization.
class PermissionOnboardingScreen extends StatefulWidget {
  final VoidCallback onComplete;
  const PermissionOnboardingScreen({super.key, required this.onComplete});

  @override
  State<PermissionOnboardingScreen> createState() =>
      _PermissionOnboardingScreenState();
}

class _PermissionOnboardingScreenState
    extends State<PermissionOnboardingScreen> {
  final _permService = PermissionService();
  final Map<AriPermission, bool?> _results = {};
  bool _requesting = false;

  static const _permissions = [
    _PermDef(
      perm: AriPermission.camera,
      icon: Icons.camera_alt,
      title: 'Camera',
      description: 'Capture photos and videos for farm notebook entries.',
    ),
    _PermDef(
      perm: AriPermission.microphone,
      icon: Icons.mic,
      title: 'Microphone',
      description: 'Record voice notes for farm entries.',
    ),
    _PermDef(
      perm: AriPermission.location,
      icon: Icons.location_on,
      title: 'Location',
      description: 'Auto-fill farm GPS coordinates when creating a farm.',
    ),
    _PermDef(
      perm: AriPermission.photos,
      icon: Icons.photo_library,
      title: 'Photos & Files',
      description: 'Attach existing media files to notebook entries.',
    ),
    _PermDef(
      perm: AriPermission.notifications,
      icon: Icons.notifications,
      title: 'Notifications',
      description:
          'Receive local upload reminders. Backend notifications always work.',
    ),
  ];

  Future<void> _requestAll() async {
    setState(() => _requesting = true);
    for (final def in _permissions) {
      final granted = await _permService.request(def.perm);
      setState(() => _results[def.perm] = granted);
    }
    setState(() => _requesting = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 24),
              const Icon(Icons.security, size: 48, color: Colors.green),
              const SizedBox(height: 16),
              const Text(
                'App Permissions',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              const Text(
                'ARI needs the following permissions to capture farm evidence. '
                'You can deny any permission — core features will still work with alternatives.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 24),
              Expanded(
                child: ListView(
                  children: _permissions.map((def) {
                    final result = _results[def.perm];
                    return ListTile(
                      leading: Icon(def.icon),
                      title: Text(def.title),
                      subtitle: Text(def.description),
                      trailing: result == null
                          ? const SizedBox.shrink()
                          : Icon(
                              result ? Icons.check_circle : Icons.cancel,
                              color: result ? Colors.green : Colors.grey,
                            ),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 16),
              if (_results.isEmpty)
                ElevatedButton(
                  onPressed: _requesting ? null : _requestAll,
                  child: _requesting
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2))
                      : const Text('Grant Permissions'),
                )
              else
                ElevatedButton(
                  onPressed: widget.onComplete,
                  child: const Text('Continue to App'),
                ),
              const SizedBox(height: 8),
              TextButton(
                onPressed: _requesting ? null : widget.onComplete,
                child: const Text('Skip for now'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PermDef {
  final AriPermission perm;
  final IconData icon;
  final String title;
  final String description;
  const _PermDef({
    required this.perm,
    required this.icon,
    required this.title,
    required this.description,
  });
}

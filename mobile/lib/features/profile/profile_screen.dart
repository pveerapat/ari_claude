import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/providers/auth_provider.dart';
import '../../shared/providers/farm_context_provider.dart';
import '../../shared/widgets/ari_widgets.dart';
import '../upload_queue/upload_queue_screen.dart';
import '../follow_ups/follow_up_screens.dart';
import '../farm_structure/farm_structure_screens.dart';

/// Profile screen — shows user fields from backend, logout.
/// Does not show RBAC role editing.
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final farmCtx = context.watch<FarmContextProvider>();
    final user = auth.user;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Logout',
            onPressed: () => _confirmLogout(context),
          ),
        ],
      ),
      body: user == null
          ? const AriLoadingIndicator()
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // User info card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _InfoRow(label: 'Name', value: user.name),
                        _InfoRow(label: 'Phone', value: user.phone),
                        _InfoRow(
                            label: 'Role',
                            value: _roleLabel(user.farmerStatus)),
                        _InfoRow(
                            label: 'Membership', value: user.membershipStatus),
                        _InfoRow(label: 'Account', value: user.accountStatus),
                        if (farmCtx.activeFarm != null)
                          _InfoRow(
                              label: 'Active Farm',
                              value: farmCtx.activeFarm!.name),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                // Quick links
                if (user.canUseProtectedFeatures) ...[
                  ListTile(
                    leading: const Icon(Icons.upload),
                    title: const Text('Upload Queue'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => const UploadQueueScreen())),
                  ),
                  ListTile(
                    leading: const Icon(Icons.follow_the_signs),
                    title: const Text('Follow-Ups'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => const FollowUpListScreen())),
                  ),
                  if (farmCtx.activeFarm != null)
                    ListTile(
                      leading: const Icon(Icons.crop_square),
                      title: const Text('Zones'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) =>
                                ZoneListScreen(farmId: farmCtx.activeFarm!.id),
                          )),
                    ),
                ],
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    onPressed: () => _confirmLogout(context),
                    icon: const Icon(Icons.logout, color: Colors.red),
                    label: const Text('Logout',
                        style: TextStyle(color: Colors.red)),
                  ),
                ),
              ],
            ),
    );
  }

  Future<void> _confirmLogout(BuildContext context) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Logout'),
        content: const Text(
          'Logging out will clear your session. '
          'Unsynced local drafts will be preserved.',
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancel')),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Logout', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
    if (confirmed == true && context.mounted) {
      await context.read<AuthProvider>().logout();
    }
  }

  String _roleLabel(String s) {
    switch (s) {
      case 'owner':
        return 'Farm Owner';
      case 'owner_family':
        return 'Owner Family';
      case 'farm_staff':
        return 'Farm Staff';
      default:
        return s;
    }
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;
  const _InfoRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Row(
          children: [
            SizedBox(
                width: 100,
                child: Text('$label:',
                    style: const TextStyle(color: Colors.grey))),
            Expanded(
                child: Text(value,
                    style: const TextStyle(fontWeight: FontWeight.w500))),
          ],
        ),
      );
}

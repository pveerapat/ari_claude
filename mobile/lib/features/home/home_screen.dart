import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/providers/auth_provider.dart';
import '../../shared/providers/farm_context_provider.dart';
import '../../shared/providers/network_provider.dart';
import '../../shared/widgets/ari_widgets.dart';
import '../notebook/add_note_screen.dart';
import '../notebook/notebook_list_screen.dart';
import '../notifications/notification_list_screen.dart';
import '../ask_ai/ask_ai_screen.dart';
import '../farm_context/farm_selector_screen.dart';
import '../profile/profile_screen.dart';

/// Home screen — exactly four primary buttons per P2-8 §14.
/// Fixed buttons: Ask AI Now | Add Note | Farm Notebook | Notifications
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final farmCtx = context.watch<FarmContextProvider>();
    final network = context.watch<NetworkProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('ARI'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () => Navigator.push(context,
                MaterialPageRoute(builder: (_) => const ProfileScreen())),
          ),
        ],
      ),
      body: Column(
        children: [
          if (network.isOffline) const NoInternetBanner(),
          // Farm selector bar
          _FarmSelectorBar(farmCtx: farmCtx, user: auth.user),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  const SizedBox(height: 16),
                  Text(
                    'Hello, ${auth.user?.name ?? ''}',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 32),
                  // Exactly four primary buttons — shrinkWrap so all build eagerly
                  GridView.count(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisCount: 2,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 16,
                    children: [
                      _HomeButton(
                        icon: Icons.psychology,
                        label: 'Ask AI Now',
                        onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (_) => const AskAiScreen())),
                      ),
                      _HomeButton(
                        icon: Icons.add_circle_outline,
                        label: 'Add Note',
                        onTap: farmCtx.hasFarm
                            ? () => Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (_) => const AddNoteScreen()))
                            : () => _showNoFarm(context),
                      ),
                      _HomeButton(
                        icon: Icons.book,
                        label: 'Farm Notebook',
                        onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (_) => const NotebookListScreen())),
                      ),
                      _HomeButton(
                        icon: Icons.notifications_outlined,
                        label: 'Notifications',
                        onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (_) =>
                                    const NotificationListScreen())),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showNoFarm(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Please select or create a farm first.')),
    );
  }
}

class _FarmSelectorBar extends StatelessWidget {
  final FarmContextProvider farmCtx;
  final dynamic user;

  const _FarmSelectorBar({required this.farmCtx, required this.user});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => Navigator.push(context,
          MaterialPageRoute(builder: (_) => const FarmSelectorScreen())),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          border: Border(bottom: BorderSide(color: Colors.grey[300]!)),
        ),
        child: Row(
          children: [
            const Icon(Icons.agriculture, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                farmCtx.activeFarm?.name ?? 'Select Farm',
                style: const TextStyle(fontWeight: FontWeight.w500),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const Icon(Icons.chevron_right, size: 18, color: Colors.grey),
          ],
        ),
      ),
    );
  }
}

class _HomeButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _HomeButton(
      {required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon,
                  size: 40, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 12),
              Text(label,
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }
}

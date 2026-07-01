import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/providers/auth_provider.dart';

/// Shown when membership_status = pending_farm_approval.
/// Blocks all protected farm-scoped features.
/// Only allows: Profile, Logout, Session restore.
class PendingApprovalScreen extends StatelessWidget {
  const PendingApprovalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final user = auth.user;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Pending Approval'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Logout',
            onPressed: () async {
              await context.read<AuthProvider>().logout();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: 32),
            const Icon(Icons.hourglass_empty, size: 72, color: Colors.orange),
            const SizedBox(height: 24),
            const Text(
              'Waiting for Farm Approval',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            const Text(
              'Your account has been created and is waiting for the farm owner to approve your membership.\n\n'
              'Once approved, you will have access to all farm features.',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 32),
            if (user != null) ...[
              _InfoRow(label: 'Name', value: user.name),
              _InfoRow(label: 'Phone', value: user.phone),
              _InfoRow(label: 'Role', value: _roleLabel(user.farmerStatus)),
              _InfoRow(label: 'Status', value: 'Pending approval'),
            ],
            const SizedBox(height: 32),
            const Text(
              'Blocked until approval:',
              style: TextStyle(fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            ...[
              'Add Note',
              'Farm Notebook',
              'Upload Queue',
              'Sync',
              'Create Farm / Zone / Tree',
            ].map((feature) => Row(
                  children: [
                    const Icon(Icons.block, size: 16, color: Colors.red),
                    const SizedBox(width: 8),
                    Text(feature, style: const TextStyle(color: Colors.red)),
                  ],
                )),
            const SizedBox(height: 32),
            OutlinedButton.icon(
              onPressed: () async {
                await context.read<AuthProvider>().restoreSession();
              },
              icon: const Icon(Icons.refresh),
              label: const Text('Check approval status'),
            ),
          ],
        ),
      ),
    );
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
                width: 80,
                child: Text('$label:',
                    style: const TextStyle(color: Colors.grey))),
            Expanded(
                child: Text(value,
                    style: const TextStyle(fontWeight: FontWeight.w500))),
          ],
        ),
      );
}

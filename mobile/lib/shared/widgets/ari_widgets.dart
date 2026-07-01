import 'package:flutter/material.dart';

/// Common reusable widgets for ARI mobile.

class AriLoadingIndicator extends StatelessWidget {
  final String? message;
  const AriLoadingIndicator({super.key, this.message});

  @override
  Widget build(BuildContext context) => Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const CircularProgressIndicator(),
            if (message != null) ...[
              const SizedBox(height: 12),
              Text(message!, style: Theme.of(context).textTheme.bodyMedium),
            ],
          ],
        ),
      );
}

class AriEmptyState extends StatelessWidget {
  final String message;
  final IconData? icon;
  final VoidCallback? onRefresh;

  const AriEmptyState({
    super.key,
    required this.message,
    this.icon,
    this.onRefresh,
  });

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon ?? Icons.inbox_outlined,
                  size: 64, color: Colors.grey[400]),
              const SizedBox(height: 16),
              Text(message,
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.grey[600])),
              if (onRefresh != null) ...[
                const SizedBox(height: 16),
                OutlinedButton.icon(
                  onPressed: onRefresh,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Refresh'),
                ),
              ],
            ],
          ),
        ),
      );
}

class AriErrorDisplay extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const AriErrorDisplay({super.key, required this.message, this.onRetry});

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.error_outline,
                  size: 48, color: Theme.of(context).colorScheme.error),
              const SizedBox(height: 12),
              Text(message, textAlign: TextAlign.center),
              if (onRetry != null) ...[
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  onPressed: onRetry,
                  icon: const Icon(Icons.refresh),
                  label: const Text('Retry'),
                ),
              ],
            ],
          ),
        ),
      );
}

class NoInternetBanner extends StatelessWidget {
  const NoInternetBanner({super.key});

  @override
  Widget build(BuildContext context) => Container(
        width: double.infinity,
        color: Colors.orange[700],
        padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 16),
        child: const Row(
          children: [
            Icon(Icons.wifi_off, size: 16, color: Colors.white),
            SizedBox(width: 8),
            Text('No internet connection',
                style: TextStyle(color: Colors.white, fontSize: 13)),
          ],
        ),
      );
}

class PermissionDeniedWidget extends StatelessWidget {
  final String permissionName;
  final VoidCallback? onOpenSettings;

  const PermissionDeniedWidget({
    super.key,
    required this.permissionName,
    this.onOpenSettings,
  });

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.block, size: 48, color: Colors.orange),
              const SizedBox(height: 12),
              Text(
                '$permissionName permission is required for this feature.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              if (onOpenSettings != null)
                ElevatedButton(
                  onPressed: onOpenSettings,
                  child: const Text('Open Settings'),
                ),
            ],
          ),
        ),
      );
}

class StatusChip extends StatelessWidget {
  final String label;
  final Color? color;

  const StatusChip({super.key, required this.label, this.color});

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
        decoration: BoxDecoration(
          color: (color ?? Colors.grey).withOpacity(0.15),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color ?? Colors.grey, width: 1),
        ),
        child: Text(
          label,
          style: TextStyle(fontSize: 11, color: color ?? Colors.grey[700]),
        ),
      );
}

Color uploadStatusColor(String status) {
  switch (status) {
    case 'pending':
      return Colors.blue;
    case 'uploading':
      return Colors.orange;
    case 'failed':
      return Colors.red;
    case 'completed':
      return Colors.green;
    default:
      return Colors.grey;
  }
}

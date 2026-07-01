import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../core/storage/upload_queue_store.dart';
import '../../core/upload/upload_manager.dart';
import '../../shared/models/upload_queue_model.dart';
import '../../shared/providers/network_provider.dart';
import '../../shared/widgets/ari_widgets.dart';

/// Upload queue UI — shows pending/uploading/failed/completed.
/// Manual upload/retry always available.
/// Preserves client_id/local_id on retry.
class UploadQueueScreen extends StatefulWidget {
  const UploadQueueScreen({super.key});

  @override
  State<UploadQueueScreen> createState() => _UploadQueueScreenState();
}

class _UploadQueueScreenState extends State<UploadQueueScreen> {
  List<UploadQueueItem> _items = [];
  bool _loading = false;
  bool _processing = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final store = context.read<UploadQueueStore>();
      final rows = await store.listAll();
      _items = rows.map(UploadQueueItem.fromRow).toList();
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _processAll() async {
    final network = context.read<NetworkProvider>();
    if (network.isOffline) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No internet. Connect and try again.')),
      );
      return;
    }
    setState(() => _processing = true);
    try {
      final mgr = context.read<UploadManager>();
      await mgr.processQueue();
      await _load();
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _processing = false);
    }
  }

  Future<void> _retryItem(String queueId) async {
    final network = context.read<NetworkProvider>();
    if (network.isOffline) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No internet connection.')),
      );
      return;
    }
    final mgr = context.read<UploadManager>();
    await mgr.retry(queueId);
    await _load();
  }

  @override
  Widget build(BuildContext context) {
    final pending = _items.where((i) => i.isPending || i.isFailed).length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Upload Queue'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      body: Column(
        children: [
          if (pending > 0)
            Padding(
              padding: const EdgeInsets.all(16),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: _processing ? null : _processAll,
                  icon: _processing
                      ? const SizedBox(
                          height: 16,
                          width: 16,
                          child: CircularProgressIndicator(strokeWidth: 2))
                      : const Icon(Icons.upload),
                  label: Text(_processing
                      ? 'Uploading...'
                      : 'Upload All ($pending pending)'),
                ),
              ),
            ),
          if (_error != null)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(_error!, style: const TextStyle(color: Colors.red)),
            ),
          Expanded(
            child: _loading
                ? const AriLoadingIndicator()
                : _items.isEmpty
                    ? const AriEmptyState(message: 'No items in upload queue.')
                    : ListView.builder(
                        itemCount: _items.length,
                        itemBuilder: (ctx, i) => _QueueItemTile(
                          item: _items[i],
                          onRetry: () => _retryItem(_items[i].id),
                        ),
                      ),
          ),
        ],
      ),
    );
  }
}

class _QueueItemTile extends StatelessWidget {
  final UploadQueueItem item;
  final VoidCallback onRetry;

  const _QueueItemTile({required this.item, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(_typeIcon(item.itemType), size: 28),
      title: Text(item.itemType ?? 'Unknown type'),
      subtitle: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (item.errorMessage != null)
            Text(item.errorMessage!,
                style: const TextStyle(color: Colors.red, fontSize: 12)),
          Text('Retries: ${item.retryCount}',
              style: const TextStyle(fontSize: 11, color: Colors.grey)),
        ],
      ),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          StatusChip(label: item.status, color: uploadStatusColor(item.status)),
          if (item.isFailed) ...[
            const SizedBox(width: 8),
            IconButton(
                icon: const Icon(Icons.replay, color: Colors.blue),
                onPressed: onRetry),
          ],
        ],
      ),
    );
  }

  IconData _typeIcon(String? type) {
    switch (type) {
      case 'photo':
        return Icons.image;
      case 'video':
        return Icons.videocam;
      case 'voice':
        return Icons.mic;
      case 'file':
        return Icons.attach_file;
      default:
        return Icons.upload_file;
    }
  }
}

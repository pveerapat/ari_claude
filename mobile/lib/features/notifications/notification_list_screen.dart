import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/models/notification_model.dart';
import '../../shared/widgets/ari_widgets.dart';
import 'notification_repository.dart';

class NotificationListScreen extends StatefulWidget {
  const NotificationListScreen({super.key});

  @override
  State<NotificationListScreen> createState() => _NotificationListScreenState();
}

class _NotificationListScreenState extends State<NotificationListScreen> {
  List<NotificationModel> _items = [];
  bool _loading = false;
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
      final repo = context.read<NotificationRepository>();
      _items = await repo.listNotifications();
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _markAllRead() async {
    try {
      final repo = context.read<NotificationRepository>();
      await repo.markAllRead();
      await _load();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  @override
  Widget build(BuildContext context) {
    final unread = _items.where((n) => !n.isRead).length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
        actions: [
          if (unread > 0)
            TextButton(
              onPressed: _markAllRead,
              child: const Text('Mark all read',
                  style: TextStyle(color: Colors.white)),
            ),
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      body: _loading
          ? const AriLoadingIndicator()
          : _error != null
              ? AriErrorDisplay(message: _error!, onRetry: _load)
              : _items.isEmpty
                  ? const AriEmptyState(message: 'No notifications.')
                  : RefreshIndicator(
                      onRefresh: _load,
                      child: ListView.builder(
                        itemCount: _items.length,
                        itemBuilder: (ctx, i) => _NotificationTile(
                          item: _items[i],
                          onTap: () async {
                            await Navigator.push(
                                ctx,
                                MaterialPageRoute(
                                  builder: (_) => NotificationDetailScreen(
                                      notification: _items[i]),
                                ));
                            _load();
                          },
                        ),
                      ),
                    ),
    );
  }
}

class _NotificationTile extends StatelessWidget {
  final NotificationModel item;
  final VoidCallback onTap;
  const _NotificationTile({required this.item, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(
        Icons.notifications,
        color:
            item.isRead ? Colors.grey : Theme.of(context).colorScheme.primary,
      ),
      title: Text(
        item.message ?? 'Notification',
        style: TextStyle(
            fontWeight: item.isRead ? FontWeight.normal : FontWeight.bold),
        maxLines: 2,
        overflow: TextOverflow.ellipsis,
      ),
      subtitle: Text(item.createdAt.split('T').first),
      trailing: !item.isRead
          ? Container(
              width: 8,
              height: 8,
              decoration: const BoxDecoration(
                  color: Colors.blue, shape: BoxShape.circle))
          : null,
      onTap: onTap,
    );
  }
}

// ─── Notification Detail ──────────────────────────────────────────────────

class NotificationDetailScreen extends StatefulWidget {
  final NotificationModel notification;
  const NotificationDetailScreen({super.key, required this.notification});

  @override
  State<NotificationDetailScreen> createState() =>
      _NotificationDetailScreenState();
}

class _NotificationDetailScreenState extends State<NotificationDetailScreen> {
  late NotificationModel _notification;

  @override
  void initState() {
    super.initState();
    _notification = widget.notification;
    if (!_notification.isRead) {
      _markRead();
    }
  }

  Future<void> _markRead() async {
    try {
      final repo = context.read<NotificationRepository>();
      await repo.markRead(_notification.id);
      setState(() {
        _notification = NotificationModel(
          id: _notification.id,
          message: _notification.message,
          isRead: true,
          notificationType: _notification.notificationType,
          createdAt: _notification.createdAt,
        );
      });
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notification')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (_notification.notificationType != null)
              StatusChip(
                  label: _notification.notificationType!, color: Colors.blue),
            const SizedBox(height: 12),
            Text(_notification.message ?? 'No message',
                style: Theme.of(context).textTheme.bodyLarge),
            const SizedBox(height: 8),
            Text(_notification.createdAt.split('T').first,
                style: const TextStyle(color: Colors.grey, fontSize: 12)),
          ],
        ),
      ),
    );
  }
}

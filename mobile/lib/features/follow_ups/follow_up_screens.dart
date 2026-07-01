import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/models/follow_up_model.dart';
import '../../shared/widgets/ari_widgets.dart';
import 'follow_up_repository.dart';

// ─── Follow-Up List ───────────────────────────────────────────────────────

class FollowUpListScreen extends StatefulWidget {
  const FollowUpListScreen({super.key});

  @override
  State<FollowUpListScreen> createState() => _FollowUpListScreenState();
}

class _FollowUpListScreenState extends State<FollowUpListScreen> {
  List<FollowUpModel> _items = [];
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
      final repo = context.read<FollowUpRepository>();
      _items = await repo.listFollowUps();
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Follow-Ups'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load)
        ],
      ),
      body: _loading
          ? const AriLoadingIndicator()
          : _error != null
              ? AriErrorDisplay(message: _error!, onRetry: _load)
              : _items.isEmpty
                  ? const AriEmptyState(message: 'No follow-ups found.')
                  : RefreshIndicator(
                      onRefresh: _load,
                      child: ListView.builder(
                        itemCount: _items.length,
                        itemBuilder: (ctx, i) => _FollowUpTile(
                          item: _items[i],
                          onTap: () async {
                            await Navigator.push(
                                ctx,
                                MaterialPageRoute(
                                  builder: (_) => FollowUpDetailScreen(
                                      followUpId: _items[i].id),
                                ));
                            _load();
                          },
                        ),
                      ),
                    ),
    );
  }
}

class _FollowUpTile extends StatelessWidget {
  final FollowUpModel item;
  final VoidCallback onTap;
  const _FollowUpTile({required this.item, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: Colors.green[100],
        child: Text('${item.followUpDay ?? '?'}d',
            style: const TextStyle(fontSize: 12)),
      ),
      title: Text('Follow-Up — Day ${item.followUpDay ?? 'N/A'}'),
      subtitle: Text(item.dueDate ?? item.createdAt.split('T').first),
      trailing: item.outcome != null
          ? StatusChip(
              label: item.outcome!, color: _outcomeColor(item.outcome!))
          : const StatusChip(label: 'pending', color: Colors.orange),
      onTap: onTap,
    );
  }

  Color _outcomeColor(String o) {
    switch (o) {
      case 'improved':
        return Colors.green;
      case 'same':
        return Colors.blue;
      case 'worse':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }
}

// ─── Follow-Up Detail ─────────────────────────────────────────────────────

class FollowUpDetailScreen extends StatefulWidget {
  final String followUpId;
  const FollowUpDetailScreen({super.key, required this.followUpId});

  @override
  State<FollowUpDetailScreen> createState() => _FollowUpDetailScreenState();
}

class _FollowUpDetailScreenState extends State<FollowUpDetailScreen> {
  FollowUpModel? _item;
  bool _loading = false;
  bool _updating = false;
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
      final repo = context.read<FollowUpRepository>();
      _item = await repo.getFollowUp(widget.followUpId);
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _updateOutcome(String outcome) async {
    setState(() => _updating = true);
    try {
      final repo = context.read<FollowUpRepository>();
      _item = await repo.updateOutcome(widget.followUpId, outcome);
      if (mounted)
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Outcome updated: $outcome')),
        );
    } catch (e) {
      if (mounted)
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString())),
        );
    } finally {
      if (mounted) setState(() => _updating = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Follow-Up Detail')),
      body: _loading
          ? const AriLoadingIndicator()
          : _error != null
              ? AriErrorDisplay(message: _error!, onRetry: _load)
              : _item == null
                  ? const AriEmptyState(message: 'Not found.')
                  : SingleChildScrollView(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _row('Day', '${_item!.followUpDay ?? 'N/A'} days'),
                          _row('Due', _item!.dueDate ?? 'N/A'),
                          _row('Status', _item!.status ?? 'N/A'),
                          _row('Outcome', _item!.outcome ?? 'Not set'),
                          if (_item!.notes != null)
                            _row('Notes', _item!.notes!),
                          const SizedBox(height: 24),
                          const Text('Update Outcome:',
                              style: TextStyle(fontWeight: FontWeight.w600)),
                          const SizedBox(height: 12),
                          Wrap(
                            spacing: 8,
                            children: FollowUpModel.outcomeValues
                                .map((o) => ChoiceChip(
                                      label: Text(o),
                                      selected: _item!.outcome == o,
                                      onSelected: _updating
                                          ? null
                                          : (_) => _updateOutcome(o),
                                    ))
                                .toList(),
                          ),
                          if (_updating)
                            const Padding(
                              padding: EdgeInsets.only(top: 16),
                              child: LinearProgressIndicator(),
                            ),
                          const SizedBox(height: 16),
                          const Text(
                            'Follow-up periods: 3 / 7 / 14 days',
                            style: TextStyle(color: Colors.grey, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
    );
  }

  Widget _row(String label, String value) => Padding(
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

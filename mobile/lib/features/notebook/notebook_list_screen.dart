import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/models/notebook_entry_model.dart';
import '../../shared/providers/farm_context_provider.dart';
import '../../shared/providers/network_provider.dart';
import '../../shared/widgets/ari_widgets.dart';
import 'notebook_repository.dart';
import 'notebook_detail_screen.dart';
import 'add_note_screen.dart';

/// Notebook list — shows both server entries (online) and local drafts.
/// Clearly labels: local-only / pending upload / uploaded / failed.
class NotebookListScreen extends StatefulWidget {
  const NotebookListScreen({super.key});

  @override
  State<NotebookListScreen> createState() => _NotebookListScreenState();
}

class _NotebookListScreenState extends State<NotebookListScreen> {
  List<NotebookEntryModel> _serverEntries = [];
  List<NotebookEntryModel> _localDrafts = [];
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
    final network = context.read<NetworkProvider>();
    try {
      final repo = context.read<NotebookRepository>();
      final farmCtx = context.read<FarmContextProvider>();

      _localDrafts = await repo.listLocalDrafts(farmId: farmCtx.activeFarm?.id);

      if (network.isOnline) {
        _serverEntries =
            await repo.listServerEntries(farmId: farmCtx.activeFarm?.id);
      }
    } catch (e) {
      if (network.isOnline) {
        _error = e.toString();
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final network = context.watch<NetworkProvider>();

    final allEntries = [
      ..._localDrafts,
      ..._serverEntries.where((s) => !_localDrafts.any((l) => l.id == s.id)),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Farm Notebook'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(context,
              MaterialPageRoute(builder: (_) => const AddNoteScreen()));
          _load();
        },
        icon: const Icon(Icons.add),
        label: const Text('Add Note'),
      ),
      body: Column(
        children: [
          if (network.isOffline) const NoInternetBanner(),
          Expanded(
            child: _loading
                ? const AriLoadingIndicator()
                : _error != null
                    ? AriErrorDisplay(message: _error!, onRetry: _load)
                    : allEntries.isEmpty
                        ? AriEmptyState(
                            message: 'No notebook entries yet.',
                            onRefresh: _load)
                        : RefreshIndicator(
                            onRefresh: _load,
                            child: ListView.builder(
                              itemCount: allEntries.length,
                              itemBuilder: (ctx, i) =>
                                  _EntryTile(entry: allEntries[i]),
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

class _EntryTile extends StatelessWidget {
  final NotebookEntryModel entry;
  const _EntryTile({required this.entry});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(
        entry.entryType == 'consultation' ? Icons.psychology : Icons.book,
        color: entry.isLocalOnly ? Colors.orange : Colors.green,
      ),
      title: Text(entry.title ?? 'Untitled ${entry.entryType}'),
      subtitle: Text(_statusLabel()),
      trailing: StatusChip(
        label: entry.isLocalOnly ? entry.localStatus : 'uploaded',
        color: entry.isLocalOnly ? Colors.orange : Colors.green,
      ),
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => NotebookDetailScreen(entry: entry)),
      ),
    );
  }

  String _statusLabel() {
    if (entry.isLocalOnly) {
      switch (entry.localStatus) {
        case 'local':
          return 'Saved locally — not uploaded';
        case 'uploading':
          return 'Uploading...';
        case 'failed':
          return 'Upload failed';
        default:
          return entry.localStatus;
      }
    }
    return entry.createdAt.split('T').first;
  }
}

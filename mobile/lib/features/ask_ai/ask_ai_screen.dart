import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/models/notebook_entry_model.dart';
import '../../shared/providers/farm_context_provider.dart';
import '../../shared/providers/network_provider.dart';
import '../../shared/widgets/ari_widgets.dart';
import '../notebook/add_note_screen.dart';
import '../notebook/notebook_detail_screen.dart';
import '../notebook/notebook_repository.dart';

/// Ask AI Now — safe UI boundary only for P2-8.
/// No internal AI engine, no RAG, no LLM calls.
/// Shows existing consultation notes; allows creating new ones.
///
/// MOBILE-GAP-P2-8-005: Ask AI Now backend/API boundary.
/// Internal ARI AI is not implemented in P2-8.
class AskAiScreen extends StatefulWidget {
  const AskAiScreen({super.key});

  @override
  State<AskAiScreen> createState() => _AskAiScreenState();
}

class _AskAiScreenState extends State<AskAiScreen> {
  List<NotebookEntryModel> _consultations = [];
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

      final localDrafts = await repo.listLocalDrafts(farmId: farmCtx.activeFarm?.id);
      final localConsult = localDrafts.where((e) => e.entryType == 'consultation').toList();

      List<NotebookEntryModel> serverConsult = [];
      if (network.isOnline) {
        final all = await repo.listServerEntries(farmId: farmCtx.activeFarm?.id);
        serverConsult = all.where((e) => e.entryType == 'consultation').toList();
      }

      // merge: local drafts first, then server entries not already in local
      final merged = [
        ...localConsult,
        ...serverConsult.where((s) => !localConsult.any((l) => l.id == s.id)),
      ];

      if (mounted) setState(() => _consultations = merged);
    } catch (e) {
      if (mounted) setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final network = context.watch<NetworkProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ask AI Now'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(
            context,
            MaterialPageRoute(
                builder: (_) => const AddNoteScreen(entryType: 'consultation')),
          );
          _load();
        },
        icon: const Icon(Icons.note_add),
        label: const Text('New Consultation'),
      ),
      body: Column(
        children: [
          if (network.isOffline) const NoInternetBanner(),
          // Placeholder banner
          Container(
            width: double.infinity,
            margin: const EdgeInsets.all(16),
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.grey[100],
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.grey[300]!),
            ),
            child: Column(children: [
              Icon(Icons.psychology_outlined, size: 48, color: Colors.grey[500]),
              const SizedBox(height: 12),
              const Text('ARI AI Analysis',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              const Text(
                'AI-powered analysis is not available in this version (P2-8).\n'
                'Capture observations as Consultation notes — they will be ready for AI review in a future version.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey, fontSize: 13),
              ),
            ]),
          ),
          // Consultation list
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
            child: Row(children: [
              const Text('Consultation Notes',
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 15)),
              const SizedBox(width: 8),
              if (_consultations.isNotEmpty)
                StatusChip(
                    label: '${_consultations.length}',
                    color: Colors.purple),
            ]),
          ),
          Expanded(
            child: _loading
                ? const AriLoadingIndicator()
                : _error != null
                    ? AriErrorDisplay(message: _error!, onRetry: _load)
                    : _consultations.isEmpty
                        ? AriEmptyState(
                            message: 'No consultation notes yet.\nTap + to start one.',
                            icon: Icons.psychology_outlined,
                            onRefresh: _load,
                          )
                        : RefreshIndicator(
                            onRefresh: _load,
                            child: ListView.builder(
                              itemCount: _consultations.length,
                              itemBuilder: (ctx, i) =>
                                  _ConsultationTile(entry: _consultations[i]),
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

class _ConsultationTile extends StatelessWidget {
  final NotebookEntryModel entry;
  const _ConsultationTile({required this.entry});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(
        Icons.psychology,
        color: entry.isLocalOnly ? Colors.orange : Colors.purple,
      ),
      title: Text(entry.title ?? 'Untitled Consultation'),
      subtitle: Text(_statusLabel()),
      trailing: StatusChip(
        label: entry.isLocalOnly ? entry.localStatus : 'uploaded',
        color: entry.isLocalOnly ? Colors.orange : Colors.purple,
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

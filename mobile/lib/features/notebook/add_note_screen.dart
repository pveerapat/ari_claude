import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../../shared/providers/farm_context_provider.dart';
import 'notebook_repository.dart';
import 'notebook_detail_screen.dart';
import '../../shared/models/notebook_entry_model.dart';

/// Add Note — creates a local draft notebook entry.
/// entry_type defaults to 'note'; 'consultation' is set via Ask AI flow.
/// Save Local ≠ Upload ≠ Analyze.
class AddNoteScreen extends StatefulWidget {
  final String entryType;
  const AddNoteScreen({super.key, this.entryType = 'note'});

  @override
  State<AddNoteScreen> createState() => _AddNoteScreenState();
}

class _AddNoteScreenState extends State<AddNoteScreen> {
  final _titleCtrl = TextEditingController();
  final _summaryCtrl = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _titleCtrl.dispose();
    _summaryCtrl.dispose();
    super.dispose();
  }

  Future<void> _saveLocal() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final farmCtx = context.read<FarmContextProvider>();
      final repo = context.read<NotebookRepository>();

      final localId = await repo.saveLocalDraft(
        entryType: widget.entryType,
        farmId: farmCtx.activeFarm?.id,
        title: _titleCtrl.text.trim().isEmpty ? null : _titleCtrl.text.trim(),
        summary:
            _summaryCtrl.text.trim().isEmpty ? null : _summaryCtrl.text.trim(),
      );

      if (mounted) {
        final draftEntry = NotebookEntryModel(
          id: '',
          entryType: widget.entryType,
          farmId: farmCtx.activeFarm?.id,
          title: _titleCtrl.text.trim().isEmpty ? null : _titleCtrl.text.trim(),
          summary: _summaryCtrl.text.trim().isEmpty
              ? null
              : _summaryCtrl.text.trim(),
          createdAt: DateTime.now().toIso8601String(),
          localId: localId,
          isLocalOnly: true,
          localStatus: 'local',
        );
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
              builder: (_) => NotebookDetailScreen(entry: draftEntry)),
        );
      }
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final farmCtx = context.watch<FarmContextProvider>();

    return Scaffold(
      appBar: AppBar(
          title: Text(widget.entryType == 'consultation'
              ? 'New Consultation'
              : 'Add Note')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (farmCtx.activeFarm != null)
              ListTile(
                leading: const Icon(Icons.agriculture),
                title: Text(farmCtx.activeFarm!.name),
                subtitle: const Text('Active farm'),
                contentPadding: EdgeInsets.zero,
              ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _titleCtrl,
              keyboardType: TextInputType.visiblePassword,
              onTap: () {
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  Future.delayed(const Duration(milliseconds: 200), () {
                    SystemChannels.textInput.invokeMethod('TextInput.show');
                  });
                });
              },
              decoration: const InputDecoration(
                labelText: 'Title (optional)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _summaryCtrl,
              maxLines: 3,
              keyboardType: TextInputType.visiblePassword,
              onTap: () {
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  Future.delayed(const Duration(milliseconds: 200), () {
                    SystemChannels.textInput.invokeMethod('TextInput.show');
                  });
                });
              },
              decoration: const InputDecoration(
                labelText: 'Summary (optional)',
                border: OutlineInputBorder(),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 12),
              Text(_error!, style: const TextStyle(color: Colors.red)),
            ],
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _loading ? null : _saveLocal,
              icon: const Icon(Icons.save_alt),
              label: _loading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2))
                  : const Text('Save Local Draft'),
            ),
            const SizedBox(height: 8),
            const Text(
              'The note will be saved locally. '
              'Upload separately when ready — Save ≠ Upload ≠ Analyze.',
              style: TextStyle(color: Colors.grey, fontSize: 12),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

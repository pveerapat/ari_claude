import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import '../../core/permissions/permission_service.dart';
import 'notebook_repository.dart';

/// Bottom sheet for capturing note items: photo/video/voice/text/file/link.
/// sequence_order is assigned automatically.
/// Local file is saved first; upload is separate (Save ≠ Upload).
class AddNoteItemSheet extends StatefulWidget {
  final String localEntryId;
  const AddNoteItemSheet({super.key, required this.localEntryId});

  @override
  State<AddNoteItemSheet> createState() => _AddNoteItemSheetState();
}

class _AddNoteItemSheetState extends State<AddNoteItemSheet> {
  final _textCtrl = TextEditingController();
  final _urlCtrl = TextEditingController();
  final _permService = PermissionService();
  final _imagePicker = ImagePicker();
  bool _saving = false;
  String? _error;

  @override
  void dispose() {
    _textCtrl.dispose();
    _urlCtrl.dispose();
    super.dispose();
  }

  Future<void> _capturePhoto() async {
    final granted = await _permService.request(AriPermission.camera);
    if (!granted) {
      _showPermDenied('Camera');
      return;
    }
    final xFile = await _imagePicker.pickImage(source: ImageSource.camera);
    if (xFile == null) return;
    await _saveFileItem('photo', xFile.path, 'image/jpeg');
  }

  Future<void> _captureVideo() async {
    final camGranted = await _permService.request(AriPermission.camera);
    final micGranted = await _permService.request(AriPermission.microphone);
    if (!camGranted || !micGranted) {
      _showPermDenied('Camera/Microphone');
      return;
    }
    final xFile = await _imagePicker.pickVideo(source: ImageSource.camera);
    if (xFile == null) return;
    await _saveFileItem('video', xFile.path, 'video/mp4');
  }

  Future<void> _pickFromGallery() async {
    final granted = await _permService.request(AriPermission.photos);
    if (!granted) {
      _showPermDenied('Photos');
      return;
    }
    final xFile = await _imagePicker.pickImage(source: ImageSource.gallery);
    if (xFile == null) return;
    await _saveFileItem('photo', xFile.path, 'image/jpeg');
  }

  Future<void> _recordVoice() async {
    final granted = await _permService.request(AriPermission.microphone);
    if (!granted) {
      _showPermDenied('Microphone');
      return;
    }
    final dir = await getTemporaryDirectory();
    final path =
        '${dir.path}/voice_${DateTime.now().millisecondsSinceEpoch}.m4a';
    final recorder = AudioRecorder();

    if (!await recorder.hasPermission()) {
      _showPermDenied('Microphone');
      return;
    }

    await recorder.start(const RecordConfig(), path: path);
    if (!mounted) return;

    final confirmed = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Recording...'),
        content: const Text('Tap Stop to finish recording.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Stop'),
          ),
        ],
      ),
    );

    await recorder.stop();
    if (confirmed == true && File(path).existsSync()) {
      await _saveFileItem('voice', path, 'audio/m4a');
    }
  }

  Future<void> _saveTextItem() async {
    final text = _textCtrl.text.trim();
    if (text.isEmpty) return;
    _setSaving(true);
    try {
      final repo = context.read<NotebookRepository>();
      await repo.saveLocalItem(
        localEntryId: widget.localEntryId,
        itemType: 'text',
        textContent: text,
      );
      if (mounted) Navigator.pop(context);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      _setSaving(false);
    }
  }

  Future<void> _saveLinkItem() async {
    final url = _urlCtrl.text.trim();
    if (url.isEmpty) return;
    _setSaving(true);
    try {
      final repo = context.read<NotebookRepository>();
      await repo.saveLocalItem(
        localEntryId: widget.localEntryId,
        itemType: 'link',
        url: url,
      );
      if (mounted) Navigator.pop(context);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      _setSaving(false);
    }
  }

  Future<void> _saveFileItem(String type, String path, String mime) async {
    _setSaving(true);
    try {
      final repo = context.read<NotebookRepository>();
      await repo.saveLocalItem(
        localEntryId: widget.localEntryId,
        itemType: type,
        localFilePath: path,
        mimeType: mime,
      );
      if (mounted) Navigator.pop(context);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      _setSaving(false);
    }
  }

  void _showPermDenied(String name) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
          content: Text('$name permission denied. Go to Settings to enable.')),
    );
  }

  void _setSaving(bool v) {
    if (mounted) setState(() => _saving = v);
  }

  @override
  Widget build(BuildContext context) {
    return DraggableScrollableSheet(
      initialChildSize: 0.65,
      maxChildSize: 0.95,
      minChildSize: 0.4,
      expand: false,
      builder: (_, scrollController) => Padding(
        padding: EdgeInsets.only(
          left: 16,
          right: 16,
          top: 16,
          bottom: MediaQuery.of(context).viewInsets.bottom + 16,
        ),
        child: SingleChildScrollView(
          controller: scrollController,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text('Add Note Item',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              // Media buttons
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: [
                  _MediaButton(
                      icon: Icons.camera_alt,
                      label: 'Photo',
                      onTap: _saving ? null : _capturePhoto),
                  _MediaButton(
                      icon: Icons.videocam,
                      label: 'Video',
                      onTap: _saving ? null : _captureVideo),
                  _MediaButton(
                      icon: Icons.mic,
                      label: 'Voice',
                      onTap: _saving ? null : _recordVoice),
                  _MediaButton(
                      icon: Icons.photo_library,
                      label: 'Gallery',
                      onTap: _saving ? null : _pickFromGallery),
                ],
              ),
              const SizedBox(height: 20),
              // Text item
              TextFormField(
                controller: _textCtrl,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'Text Note',
                  border: OutlineInputBorder(),
                  hintText: 'Enter text observation...',
                ),
              ),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: _saving ? null : _saveTextItem,
                child: const Text('Add Text Note'),
              ),
              const SizedBox(height: 16),
              // Link item
              TextFormField(
                controller: _urlCtrl,
                keyboardType: TextInputType.url,
                decoration: const InputDecoration(
                  labelText: 'Link URL',
                  border: OutlineInputBorder(),
                  hintText: 'https://...',
                ),
              ),
              const SizedBox(height: 8),
              OutlinedButton(
                onPressed: _saving ? null : _saveLinkItem,
                child: const Text('Add Link'),
              ),
              if (_error != null) ...[
                const SizedBox(height: 8),
                Text(_error!, style: const TextStyle(color: Colors.red)),
              ],
              if (_saving) const SizedBox(height: 8),
              if (_saving) const LinearProgressIndicator(),
            ],
          ),
        ),
      ),
    );
  }
}

class _MediaButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback? onTap;
  const _MediaButton({required this.icon, required this.label, this.onTap});

  @override
  Widget build(BuildContext context) => ElevatedButton.icon(
        onPressed: onTap,
        icon: Icon(icon),
        label: Text(label),
        style: ElevatedButton.styleFrom(
          backgroundColor:
              Theme.of(context).colorScheme.surfaceContainerHighest,
          foregroundColor: Theme.of(context).colorScheme.onSurface,
        ),
      );
}

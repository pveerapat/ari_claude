import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:video_player/video_player.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../shared/models/notebook_entry_model.dart';
import '../../shared/models/note_item_model.dart';
import '../../shared/widgets/ari_widgets.dart';
import 'notebook_repository.dart';
import 'add_note_item_sheet.dart';

/// Notebook detail — shows entry info + note item timeline in sequence_order.
class NotebookDetailScreen extends StatefulWidget {
  final NotebookEntryModel entry;
  const NotebookDetailScreen({super.key, required this.entry});

  @override
  State<NotebookDetailScreen> createState() => _NotebookDetailScreenState();
}

class _NotebookDetailScreenState extends State<NotebookDetailScreen> {
  List<NoteItemModel> _items = [];
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
      final repo = context.read<NotebookRepository>();
      if (widget.entry.isLocalOnly && widget.entry.localId != null) {
        _items = await repo.listLocalItems(widget.entry.localId!);
      } else if (widget.entry.id.isNotEmpty) {
        _items = await repo.listServerItems(widget.entry.id);
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.entry.title ?? 'Notebook Entry')),
      floatingActionButton: widget.entry.localId != null
          ? FloatingActionButton(
              onPressed: () async {
                await showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  builder: (_) =>
                      AddNoteItemSheet(localEntryId: widget.entry.localId!),
                );
                _load();
              },
              child: const Icon(Icons.add),
            )
          : null,
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Entry header
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(children: [
                  StatusChip(
                    label: widget.entry.entryType,
                    color: widget.entry.entryType == 'consultation'
                        ? Colors.purple
                        : Colors.blue,
                  ),
                  const SizedBox(width: 8),
                  StatusChip(
                    label: widget.entry.isLocalOnly
                        ? widget.entry.localStatus
                        : 'uploaded',
                    color:
                        widget.entry.isLocalOnly ? Colors.orange : Colors.green,
                  ),
                ]),
                if (widget.entry.title != null) ...[
                  const SizedBox(height: 8),
                  Text(widget.entry.title!,
                      style: Theme.of(context).textTheme.titleMedium),
                ],
                if (widget.entry.summary != null) ...[
                  const SizedBox(height: 4),
                  Text(widget.entry.summary!,
                      style: TextStyle(color: Colors.grey[600])),
                ],
                const SizedBox(height: 4),
                Text(widget.entry.createdAt.split('T').first,
                    style: const TextStyle(color: Colors.grey, fontSize: 12)),
              ],
            ),
          ),
          const Divider(),
          // Note item timeline (sequence_order preserved)
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: const Text('Timeline',
                style: TextStyle(fontWeight: FontWeight.w600)),
          ),
          Expanded(
            child: _loading
                ? const AriLoadingIndicator()
                : _error != null
                    ? AriErrorDisplay(message: _error!, onRetry: _load)
                    : _items.isEmpty
                        ? const AriEmptyState(
                            message: 'No items yet. Tap + to add.')
                        : ListView.builder(
                            itemCount: _items.length,
                            itemBuilder: (ctx, i) =>
                                _NoteItemTile(item: _items[i]),
                          ),
          ),
        ],
      ),
    );
  }
}

class _NoteItemTile extends StatelessWidget {
  final NoteItemModel item;
  const _NoteItemTile({required this.item});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: CircleAvatar(
        backgroundColor: Colors.grey[200],
        child: Text('${item.sequenceOrder}',
            style: const TextStyle(fontSize: 12, color: Colors.black87)),
      ),
      title: Row(children: [
        Icon(_typeIcon(item.itemType), size: 16, color: Colors.grey),
        const SizedBox(width: 4),
        Text(item.itemType.toUpperCase(),
            style: const TextStyle(
                fontSize: 12, fontWeight: FontWeight.w600, color: Colors.grey)),
      ]),
      subtitle: _subtitle(item),
      trailing: item.isLocalOnly
          ? StatusChip(
              label: item.localStatus,
              color: item.localStatus == 'failed' ? Colors.red : Colors.orange,
            )
          : null,
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => NoteItemDetailScreen(item: item)),
      ),
    );
  }

  Widget? _subtitle(NoteItemModel item) {
    switch (item.itemType) {
      case 'text':
        return item.textContent != null
            ? Text(item.textContent!,
                maxLines: 2, overflow: TextOverflow.ellipsis)
            : null;
      case 'link':
        return item.url != null
            ? Text(item.url!, style: const TextStyle(color: Colors.blue))
            : null;
      case 'photo':
        return item.localFilePath != null
            ? const Text('Photo — saved locally')
            : const Text('Photo');
      case 'video':
        return item.localFilePath != null
            ? const Text('Video — saved locally')
            : const Text('Video');
      case 'voice':
        return item.localFilePath != null
            ? const Text('Voice recording — saved locally')
            : const Text('Voice');
      case 'file':
        return item.localFilePath != null
            ? Text(item.localFilePath!.split('/').last)
            : const Text('File');
      default:
        return null;
    }
  }

  IconData _typeIcon(String type) {
    switch (type) {
      case 'photo':
        return Icons.photo;
      case 'video':
        return Icons.videocam;
      case 'voice':
        return Icons.mic;
      case 'text':
        return Icons.text_fields;
      case 'file':
        return Icons.attach_file;
      case 'link':
        return Icons.link;
      default:
        return Icons.note;
    }
  }
}

// ─── Note Item Detail ─────────────────────────────────────────────────────────

class NoteItemDetailScreen extends StatelessWidget {
  final NoteItemModel item;
  const NoteItemDetailScreen({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${item.itemType.toUpperCase()} #${item.sequenceOrder}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: _buildContent(),
      ),
    );
  }

  Widget _buildContent() {
    switch (item.itemType) {
      case 'photo':
        return _PhotoDetail(item: item);
      case 'video':
        return _VideoDetail(item: item);
      case 'voice':
        return _VoiceDetail(item: item);
      case 'text':
        return _TextDetail(item: item);
      case 'link':
        return _LinkDetail(item: item);
      case 'file':
        return _GenericFileDetail(item: item);
      default:
        return const _NoPreview();
    }
  }
}

// ─── Photo ────────────────────────────────────────────────────────────────────

class _PhotoDetail extends StatelessWidget {
  final NoteItemModel item;
  const _PhotoDetail({required this.item});

  @override
  Widget build(BuildContext context) {
    final path = item.localFilePath;
    if (path != null && File(path).existsSync()) {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.file(File(path), fit: BoxFit.contain),
          ),
          const SizedBox(height: 12),
          _InfoRow(label: 'File', value: path.split('/').last),
          _InfoRow(label: 'Status', value: item.isLocalOnly ? item.localStatus : 'uploaded'),
        ],
      );
    }
    return const _NoPreview();
  }
}

// ─── Video ────────────────────────────────────────────────────────────────────

class _VideoDetail extends StatefulWidget {
  final NoteItemModel item;
  const _VideoDetail({required this.item});

  @override
  State<_VideoDetail> createState() => _VideoDetailState();
}

class _VideoDetailState extends State<_VideoDetail> {
  VideoPlayerController? _controller;
  bool _initialized = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    final path = widget.item.localFilePath;
    if (path != null && File(path).existsSync()) {
      _controller = VideoPlayerController.file(File(path))
        ..initialize().then((_) {
          if (mounted) setState(() => _initialized = true);
        }).catchError((e) {
          if (mounted) setState(() => _error = e.toString());
        });
    } else {
      _error = 'Video file not found on device.';
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return _ErrorCard(message: _error!);
    }
    if (!_initialized) {
      return const Center(child: CircularProgressIndicator());
    }
    final ctrl = _controller!;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: AspectRatio(
            aspectRatio: ctrl.value.aspectRatio,
            child: VideoPlayer(ctrl),
          ),
        ),
        VideoProgressIndicator(ctrl, allowScrubbing: true,
            padding: const EdgeInsets.symmetric(vertical: 8)),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          IconButton(
            iconSize: 36,
            icon: Icon(ctrl.value.isPlaying ? Icons.pause_circle : Icons.play_circle),
            onPressed: () => setState(() =>
                ctrl.value.isPlaying ? ctrl.pause() : ctrl.play()),
          ),
          IconButton(
            icon: const Icon(Icons.replay),
            onPressed: () => ctrl.seekTo(Duration.zero),
          ),
        ]),
        const SizedBox(height: 8),
        _InfoRow(label: 'File', value: widget.item.localFilePath!.split('/').last),
        _InfoRow(label: 'Status', value: widget.item.isLocalOnly ? widget.item.localStatus : 'uploaded'),
      ],
    );
  }
}

// ─── Voice ────────────────────────────────────────────────────────────────────

class _VoiceDetail extends StatefulWidget {
  final NoteItemModel item;
  const _VoiceDetail({required this.item});

  @override
  State<_VoiceDetail> createState() => _VoiceDetailState();
}

class _VoiceDetailState extends State<_VoiceDetail> {
  final _player = AudioPlayer();
  PlayerState _state = PlayerState.stopped;
  Duration _position = Duration.zero;
  Duration _duration = Duration.zero;
  String? _error;

  @override
  void initState() {
    super.initState();
    final path = widget.item.localFilePath;
    if (path == null || !File(path).existsSync()) {
      _error = 'Audio file not found on device.';
      return;
    }
    _player.onPlayerStateChanged.listen((s) {
      if (mounted) setState(() => _state = s);
    });
    _player.onDurationChanged.listen((d) {
      if (mounted) setState(() => _duration = d);
    });
    _player.onPositionChanged.listen((p) {
      if (mounted) setState(() => _position = p);
    });
    _player.setSourceDeviceFile(path).catchError((e) {
      if (mounted) setState(() => _error = e.toString());
    });
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  String _fmt(Duration d) =>
      '${d.inMinutes.toString().padLeft(2, '0')}:${(d.inSeconds % 60).toString().padLeft(2, '0')}';

  @override
  Widget build(BuildContext context) {
    if (_error != null) return _ErrorCard(message: _error!);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.grey[100],
            borderRadius: BorderRadius.circular(8),
          ),
          child: Column(children: [
            Icon(Icons.mic, size: 48, color: Theme.of(context).colorScheme.primary),
            const SizedBox(height: 8),
            Text(_fmt(_position), style: Theme.of(context).textTheme.headlineSmall),
            Text('/ ${_fmt(_duration)}', style: const TextStyle(color: Colors.grey)),
          ]),
        ),
        Slider(
          value: _duration.inMilliseconds == 0
              ? 0
              : _position.inMilliseconds / _duration.inMilliseconds,
          onChanged: (v) {
            _player.seek(Duration(milliseconds: (v * _duration.inMilliseconds).round()));
          },
        ),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          IconButton(
            iconSize: 48,
            icon: Icon(_state == PlayerState.playing
                ? Icons.pause_circle
                : Icons.play_circle),
            onPressed: () async {
              if (_state == PlayerState.playing) {
                await _player.pause();
              } else {
                await _player.resume();
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.replay),
            onPressed: () async {
              await _player.seek(Duration.zero);
              await _player.resume();
            },
          ),
        ]),
        const SizedBox(height: 8),
        _InfoRow(label: 'File', value: widget.item.localFilePath!.split('/').last),
        _InfoRow(label: 'Status', value: widget.item.isLocalOnly ? widget.item.localStatus : 'uploaded'),
      ],
    );
  }
}

// ─── Text ─────────────────────────────────────────────────────────────────────

class _TextDetail extends StatelessWidget {
  final NoteItemModel item;
  const _TextDetail({required this.item});

  @override
  Widget build(BuildContext context) {
    final text = item.textContent ?? '(empty)';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.grey[100],
            borderRadius: BorderRadius.circular(8),
          ),
          child: SelectableText(text, style: Theme.of(context).textTheme.bodyLarge),
        ),
        const SizedBox(height: 12),
        _InfoRow(label: 'Status', value: item.isLocalOnly ? item.localStatus : 'uploaded'),
      ],
    );
  }
}

// ─── Link ─────────────────────────────────────────────────────────────────────

class _LinkDetail extends StatelessWidget {
  final NoteItemModel item;
  const _LinkDetail({required this.item});

  @override
  Widget build(BuildContext context) {
    final url = item.url ?? '';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.blue[50],
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.blue[200]!),
          ),
          child: SelectableText(url.isEmpty ? '(no URL)' : url,
              style: const TextStyle(color: Colors.blue)),
        ),
        const SizedBox(height: 12),
        if (url.isNotEmpty) ...[
          ElevatedButton.icon(
            icon: const Icon(Icons.open_in_browser),
            label: const Text('Open in Browser'),
            onPressed: () async {
              final uri = Uri.tryParse(url);
              if (uri == null) return;
              if (await canLaunchUrl(uri)) {
                await launchUrl(uri, mode: LaunchMode.externalApplication);
              } else if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Cannot open: $url')),
                );
              }
            },
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            icon: const Icon(Icons.copy, size: 16),
            label: const Text('Copy URL'),
            onPressed: () {
              Clipboard.setData(ClipboardData(text: url));
              ScaffoldMessenger.of(context)
                  .showSnackBar(const SnackBar(content: Text('URL copied')));
            },
          ),
        ],
        const SizedBox(height: 12),
        _InfoRow(label: 'Status', value: item.isLocalOnly ? item.localStatus : 'uploaded'),
      ],
    );
  }
}

// ─── Generic file ─────────────────────────────────────────────────────────────

class _GenericFileDetail extends StatelessWidget {
  final NoteItemModel item;
  const _GenericFileDetail({required this.item});

  @override
  Widget build(BuildContext context) {
    final path = item.localFilePath;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
              color: Colors.grey[100], borderRadius: BorderRadius.circular(8)),
          child: Column(children: [
            const Icon(Icons.attach_file, size: 48, color: Colors.grey),
            const SizedBox(height: 8),
            if (path != null)
              Text(path.split('/').last,
                  style: const TextStyle(fontSize: 13, color: Colors.grey),
                  textAlign: TextAlign.center),
          ]),
        ),
        const SizedBox(height: 12),
        if (path != null)
          _InfoRow(label: 'Exists', value: File(path).existsSync() ? 'Yes' : 'Not found'),
        if (item.mimeType != null) _InfoRow(label: 'Type', value: item.mimeType!),
        _InfoRow(label: 'Status', value: item.isLocalOnly ? item.localStatus : 'uploaded'),
      ],
    );
  }
}

// ─── Shared helpers ───────────────────────────────────────────────────────────

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;
  const _InfoRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(children: [
        Text('$label: ', style: const TextStyle(color: Colors.grey, fontSize: 13)),
        Expanded(child: Text(value, style: const TextStyle(fontSize: 13))),
      ]),
    );
  }
}

class _ErrorCard extends StatelessWidget {
  final String message;
  const _ErrorCard({required this.message});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
          color: Colors.red[50], borderRadius: BorderRadius.circular(8)),
      child: Column(children: [
        const Icon(Icons.error_outline, size: 48, color: Colors.red),
        const SizedBox(height: 8),
        Text(message, style: const TextStyle(color: Colors.red), textAlign: TextAlign.center),
      ]),
    );
  }
}

class _NoPreview extends StatelessWidget {
  const _NoPreview();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
          color: Colors.grey[100], borderRadius: BorderRadius.circular(8)),
      child: const Column(children: [
        Icon(Icons.image_not_supported, size: 48, color: Colors.grey),
        SizedBox(height: 8),
        Text('No preview available', style: TextStyle(color: Colors.grey)),
      ]),
    );
  }
}

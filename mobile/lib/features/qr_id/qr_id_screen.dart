import 'package:flutter/material.dart';

/// QR / ID optional helper — representation only.
/// Allowed: parse ari://farm/{id}, ari://zone/{id}, ari://tree/{id}.
/// NOT allowed: QR registry, QR API, QR service, new backend endpoint.
/// Mobile MVP works without QR.
///
/// MOBILE-GAP-P2-8-016: QR / ID scan and display boundary.
/// Mobile-only QR scanner package not included in P2-8 base dependencies.
/// Add qr_code_scanner or mobile_scanner when Owner approves QR package.
class QrIdScreen extends StatefulWidget {
  const QrIdScreen({super.key});

  @override
  State<QrIdScreen> createState() => _QrIdScreenState();
}

class _QrIdScreenState extends State<QrIdScreen> {
  final _idCtrl = TextEditingController();
  String? _parsedType;
  String? _parsedId;
  String? _error;

  @override
  void dispose() {
    _idCtrl.dispose();
    super.dispose();
  }

  void _parseManual() {
    final input = _idCtrl.text.trim();
    final result = _parseAriUri(input);
    if (result != null) {
      setState(() {
        _parsedType = result['type'];
        _parsedId = result['id'];
        _error = null;
      });
    } else {
      setState(() {
        _parsedType = null;
        _parsedId = null;
        _error =
            'Invalid ARI ID format. Use ari://farm/{id} or ari://zone/{id} or ari://tree/{id}';
      });
    }
  }

  Map<String, String>? _parseAriUri(String input) {
    final uri = Uri.tryParse(input);
    if (uri == null) return null;
    if (uri.scheme != 'ari') return null;
    final type = uri.host;
    final segments = uri.pathSegments;
    if (type.isEmpty || segments.isEmpty) return null;
    if (!['farm', 'zone', 'tree'].contains(type)) return null;
    return {'type': type, 'id': segments.first};
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('QR / ID Lookup')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Icon(Icons.qr_code, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            const Text(
              'QR Scanner',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            const Text(
              'Camera-based QR scanning requires an additional package.\n'
              'See MOBILE-GAP-P2-8-016 for package selection.\n\n'
              'You can enter an ARI ID manually below:',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey, fontSize: 13),
            ),
            const SizedBox(height: 24),
            TextField(
              controller: _idCtrl,
              decoration: const InputDecoration(
                labelText: 'ARI ID (e.g. ari://farm/uuid)',
                border: OutlineInputBorder(),
                hintText: 'ari://farm/00000000-0000-0000-0000-000000000000',
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _parseManual,
              child: const Text('Parse ID'),
            ),
            if (_error != null) ...[
              const SizedBox(height: 12),
              Text(_error!, style: const TextStyle(color: Colors.red)),
            ],
            if (_parsedType != null && _parsedId != null) ...[
              const SizedBox(height: 16),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Type: ${_parsedType!.toUpperCase()}'),
                      const SizedBox(height: 4),
                      Text('ID: $_parsedId',
                          style: const TextStyle(
                              fontFamily: 'monospace', fontSize: 12)),
                      const SizedBox(height: 12),
                      OutlinedButton(
                        onPressed: () {
                          // Navigate to detail screen using existing IDs
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                                content: Text(
                                    'Navigate to ${_parsedType!} detail: $_parsedId')),
                          );
                        },
                        child: Text('View ${_parsedType!.capitalize()} Detail'),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

extension StringCapitalize on String {
  String capitalize() =>
      isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';
}

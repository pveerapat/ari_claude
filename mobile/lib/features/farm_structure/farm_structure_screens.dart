import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/models/farm_model.dart';
import '../../shared/providers/auth_provider.dart';
import '../../shared/widgets/ari_widgets.dart';
import 'farm_repository.dart';

// ─── Zone List ────────────────────────────────────────────────────────────

class ZoneListScreen extends StatefulWidget {
  final String farmId;
  const ZoneListScreen({super.key, required this.farmId});

  @override
  State<ZoneListScreen> createState() => _ZoneListScreenState();
}

class _ZoneListScreenState extends State<ZoneListScreen> {
  List<ZoneModel> _zones = [];
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
      final repo = context.read<FarmRepository>();
      _zones = await repo.listZones(widget.farmId);
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    return Scaffold(
      appBar: AppBar(
        title: const Text('Zones'),
        actions: [
          if (auth.user?.canCreateFarm == true)
            IconButton(
              icon: const Icon(Icons.add),
              onPressed: () async {
                await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => CreateZoneScreen(farmId: widget.farmId),
                    ));
                _load();
              },
            ),
        ],
      ),
      body: _loading
          ? const AriLoadingIndicator()
          : _error != null
              ? AriErrorDisplay(message: _error!, onRetry: _load)
              : _zones.isEmpty
                  ? AriEmptyState(message: 'No zones yet.', onRefresh: _load)
                  : ListView.builder(
                      itemCount: _zones.length,
                      itemBuilder: (ctx, i) {
                        final z = _zones[i];
                        return ListTile(
                          leading: const Icon(Icons.crop_square),
                          title: Text(z.name),
                          subtitle:
                              z.zoneType != null ? Text(z.zoneType!) : null,
                          onTap: () => Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => TreeListScreen(
                                    zoneId: z.id, farmId: widget.farmId),
                              )),
                        );
                      },
                    ),
    );
  }
}

// ─── Create Zone ─────────────────────────────────────────────────────────

class CreateZoneScreen extends StatefulWidget {
  final String farmId;
  const CreateZoneScreen({super.key, required this.farmId});

  @override
  State<CreateZoneScreen> createState() => _CreateZoneScreenState();
}

class _CreateZoneScreenState extends State<CreateZoneScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _nameCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final repo = context.read<FarmRepository>();
      await repo.createZone(farmId: widget.farmId, name: _nameCtrl.text.trim());
      if (mounted) Navigator.pop(context);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    if (auth.user?.canCreateFarm != true) {
      return Scaffold(
        appBar: AppBar(title: const Text('Create Zone')),
        body: const Center(child: Text('Only farm owners can create zones.')),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Create Zone')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nameCtrl,
                decoration: const InputDecoration(
                    labelText: 'Zone Name *', border: OutlineInputBorder()),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'Required' : null,
              ),
              if (_error != null) ...[
                const SizedBox(height: 12),
                Text(_error!, style: const TextStyle(color: Colors.red))
              ],
              const SizedBox(height: 24),
              SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _loading ? null : _submit,
                    child: _loading
                        ? const CircularProgressIndicator(strokeWidth: 2)
                        : const Text('Create Zone'),
                  )),
            ],
          ),
        ),
      ),
    );
  }
}

// ─── Tree List ────────────────────────────────────────────────────────────

class TreeListScreen extends StatefulWidget {
  final String zoneId;
  final String farmId;
  const TreeListScreen({super.key, required this.zoneId, required this.farmId});

  @override
  State<TreeListScreen> createState() => _TreeListScreenState();
}

class _TreeListScreenState extends State<TreeListScreen> {
  List<TreeModel> _trees = [];
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
      final repo = context.read<FarmRepository>();
      _trees =
          await repo.listTrees(zoneId: widget.zoneId, farmId: widget.farmId);
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    return Scaffold(
      appBar: AppBar(
        title: const Text('Trees'),
        actions: [
          if (auth.user?.canCreateFarm == true)
            IconButton(
              icon: const Icon(Icons.add),
              onPressed: () async {
                await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => CreateTreeScreen(
                          zoneId: widget.zoneId, farmId: widget.farmId),
                    ));
                _load();
              },
            ),
        ],
      ),
      body: _loading
          ? const AriLoadingIndicator()
          : _error != null
              ? AriErrorDisplay(message: _error!, onRetry: _load)
              : _trees.isEmpty
                  ? AriEmptyState(message: 'No trees yet.', onRefresh: _load)
                  : ListView.builder(
                      itemCount: _trees.length,
                      itemBuilder: (ctx, i) {
                        final t = _trees[i];
                        return ListTile(
                          leading: const Icon(Icons.park),
                          title: Text(t.label ?? t.id),
                          subtitle: t.species != null ? Text(t.species!) : null,
                        );
                      },
                    ),
    );
  }
}

// ─── Create Tree ─────────────────────────────────────────────────────────

class CreateTreeScreen extends StatefulWidget {
  final String zoneId;
  final String farmId;
  const CreateTreeScreen(
      {super.key, required this.zoneId, required this.farmId});

  @override
  State<CreateTreeScreen> createState() => _CreateTreeScreenState();
}

class _CreateTreeScreenState extends State<CreateTreeScreen> {
  final _formKey = GlobalKey<FormState>();
  final _labelCtrl = TextEditingController();
  final _speciesCtrl = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _labelCtrl.dispose();
    _speciesCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final repo = context.read<FarmRepository>();
      await repo.createTree(
        zoneId: widget.zoneId,
        farmId: widget.farmId,
        label: _labelCtrl.text.trim().isEmpty ? null : _labelCtrl.text.trim(),
        species:
            _speciesCtrl.text.trim().isEmpty ? null : _speciesCtrl.text.trim(),
      );
      if (mounted) Navigator.pop(context);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    if (auth.user?.canCreateFarm != true) {
      return Scaffold(
        appBar: AppBar(title: const Text('Register Tree')),
        body: const Center(child: Text('Only farm owners can register trees.')),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Register Tree')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _labelCtrl,
                decoration: const InputDecoration(
                    labelText: 'Tree Label (optional)',
                    border: OutlineInputBorder()),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _speciesCtrl,
                decoration: const InputDecoration(
                    labelText: 'Species (optional)',
                    border: OutlineInputBorder()),
              ),
              if (_error != null) ...[
                const SizedBox(height: 12),
                Text(_error!, style: const TextStyle(color: Colors.red))
              ],
              const SizedBox(height: 24),
              SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _loading ? null : _submit,
                    child: _loading
                        ? const CircularProgressIndicator(strokeWidth: 2)
                        : const Text('Register Tree'),
                  )),
            ],
          ),
        ),
      ),
    );
  }
}

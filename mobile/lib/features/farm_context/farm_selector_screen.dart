import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../shared/models/farm_model.dart';
import '../../shared/providers/auth_provider.dart';
import '../../shared/providers/farm_context_provider.dart';
import '../../shared/providers/network_provider.dart';
import '../../shared/widgets/ari_widgets.dart';
import '../farm_structure/farm_repository.dart';
import '../farm_structure/create_farm_screen.dart';

class FarmSelectorScreen extends StatefulWidget {
  const FarmSelectorScreen({super.key});

  @override
  State<FarmSelectorScreen> createState() => _FarmSelectorScreenState();
}

class _FarmSelectorScreenState extends State<FarmSelectorScreen> {
  List<FarmModel> _farms = [];
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
      _farms = await repo.listFarms();
      if (mounted) {
        context.read<FarmContextProvider>().updateFarms(_farms);
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final farmCtx = context.watch<FarmContextProvider>();
    final network = context.watch<NetworkProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Select Farm'),
        actions: [
          if (auth.user?.canCreateFarm == true)
            IconButton(
              icon: const Icon(Icons.add),
              onPressed: () async {
                await Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (_) => const CreateFarmScreen()));
                _load();
              },
            ),
        ],
      ),
      body: Column(
        children: [
          if (network.isOffline) const NoInternetBanner(),
          Expanded(
            child: _loading
                ? const AriLoadingIndicator(message: 'Loading farms...')
                : _error != null
                    ? AriErrorDisplay(message: _error!, onRetry: _load)
                    : _farms.isEmpty
                        ? AriEmptyState(
                            message: auth.user?.canCreateFarm == true
                                ? 'No farms yet. Create your first farm.'
                                : 'No farms accessible. Contact your farm owner.',
                            icon: Icons.agriculture,
                            onRefresh: _load,
                          )
                        : ListView.builder(
                            itemCount: _farms.length,
                            itemBuilder: (ctx, i) {
                              final farm = _farms[i];
                              final isActive =
                                  farmCtx.activeFarm?.id == farm.id;
                              return ListTile(
                                leading: Icon(
                                  Icons.agriculture,
                                  color: isActive
                                      ? Theme.of(context).colorScheme.primary
                                      : null,
                                ),
                                title: Text(farm.name),
                                subtitle: farm.location != null
                                    ? Text(farm.location!)
                                    : null,
                                trailing: isActive
                                    ? const Icon(Icons.check,
                                        color: Colors.green)
                                    : null,
                                onTap: () async {
                                  final navigator = Navigator.of(context);
                                  await context
                                      .read<FarmContextProvider>()
                                      .setActiveFarm(farm);
                                  if (mounted) navigator.pop();
                                },
                              );
                            },
                          ),
          ),
        ],
      ),
    );
  }
}

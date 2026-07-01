import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'shared/providers/auth_provider.dart';
import 'shared/providers/farm_context_provider.dart';
import 'shared/widgets/ari_widgets.dart';
import 'features/auth/login_screen.dart';
import 'features/onboarding/pending_approval_screen.dart';
import 'features/onboarding/permission_onboarding_screen.dart';
import 'features/home/home_screen.dart';
import 'features/farm_structure/farm_repository.dart';

/// Root routing widget — handles session restore and redirects:
/// unknown → splash/loading
/// unauthenticated → LoginScreen
/// pendingApproval → PendingApprovalScreen
/// authenticated → HomeScreen (or PermissionOnboarding on first login)
class AppRouter extends StatefulWidget {
  const AppRouter({super.key});

  @override
  State<AppRouter> createState() => _AppRouterState();
}

class _AppRouterState extends State<AppRouter> {
  bool _permOnboardingShown = false;
  bool _initializing = true;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _init());
  }

  Future<void> _init() async {
    final auth = context.read<AuthProvider>();
    await auth.restoreSession();

    if (auth.state == AuthState.authenticated) {
      await _loadFarms();
    }
    if (mounted) setState(() => _initializing = false);
  }

  Future<void> _loadFarms() async {
    try {
      final repo = context.read<FarmRepository>();
      final auth = context.read<AuthProvider>();
      final farms = await repo.listFarms();
      if (mounted) {
        await context
            .read<FarmContextProvider>()
            .init(farms, auth.user?.primaryFarmId);
      }
    } catch (_) {
      // Offline — farm context will be empty; local drafts still accessible
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_initializing) {
      return const Scaffold(
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 16),
              Text('ARI',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            ],
          ),
        ),
      );
    }

    final auth = context.watch<AuthProvider>();

    switch (auth.state) {
      case AuthState.unknown:
        return const Scaffold(
            body: AriLoadingIndicator(message: 'Starting...'));

      case AuthState.unauthenticated:
        return const LoginScreen();

      case AuthState.pendingApproval:
        return const PendingApprovalScreen();

      case AuthState.authenticated:
        if (!_permOnboardingShown) {
          return PermissionOnboardingScreen(
            onComplete: () {
              setState(() => _permOnboardingShown = true);
            },
          );
        }
        return const HomeScreen();
    }
  }
}

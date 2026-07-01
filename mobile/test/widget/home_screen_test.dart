import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ari_mobile/features/home/home_screen.dart';
import 'package:ari_mobile/shared/models/farm_model.dart';
import 'package:ari_mobile/shared/providers/auth_provider.dart';
import 'package:ari_mobile/shared/providers/farm_context_provider.dart';
import 'package:ari_mobile/shared/providers/network_provider.dart';

import '../helpers/mock_providers.dart';

void main() {
  group('HomeScreen widget', () {
    testWidgets('renders exactly four primary buttons', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Ask AI Now'), findsOneWidget);
      expect(find.text('Add Note'), findsOneWidget);
      expect(find.text('Farm Notebook'), findsOneWidget);
      expect(find.text('Notifications'), findsOneWidget);
    });

    testWidgets('farm selector bar is rendered', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Test Farm'), findsOneWidget);
    });

    testWidgets('does not render a fifth primary button', (tester) async {
      await tester.pumpWidget(_buildSubject());
      // Exactly 4 cards in the grid
      final cards = tester.widgetList(find.byType(Card)).toList();
      expect(cards.length, equals(4));
    });
  });
}

Widget _buildSubject() => MultiProvider(
      providers: [
        ChangeNotifierProvider<AuthProvider>(
            create: (_) => MockAuthProviderOwner()),
        ChangeNotifierProvider<FarmContextProvider>(
          create: (_) => MockFarmContextProvider(
            farm: const FarmModel(id: 'f1', name: 'Test Farm'),
          ),
        ),
        ChangeNotifierProvider<NetworkProvider>(
            create: (_) => MockNetworkProvider()),
      ],
      child: const MaterialApp(home: HomeScreen()),
    );

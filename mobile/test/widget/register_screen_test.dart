import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ari_mobile/features/auth/register_screen.dart';
import 'package:ari_mobile/shared/providers/auth_provider.dart';

import '../helpers/mock_providers.dart';

void main() {
  group('RegisterScreen widget', () {
    testWidgets('renders farmer_status selection options', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Farm Owner'), findsOneWidget);
      expect(find.text('Owner Family Member'), findsOneWidget);
      expect(find.text('Farm Staff'), findsOneWidget);
    });

    testWidgets('Farm ID field not shown for owner', (tester) async {
      await tester.pumpWidget(_buildSubject());
      // owner is default — no Farm ID field
      expect(find.text('Farm ID (ask your farm owner)'), findsNothing);
    });

    testWidgets('Farm ID field appears when owner_family selected',
        (tester) async {
      await tester.pumpWidget(_buildSubject());
      await tester.tap(find.text('Owner Family Member'));
      await tester.pumpAndSettle();
      expect(find.text('Farm ID (ask your farm owner)'), findsOneWidget);
    });

    testWidgets('Farm ID field appears when farm_staff selected',
        (tester) async {
      await tester.pumpWidget(_buildSubject());
      await tester.tap(find.text('Farm Staff'));
      await tester.pumpAndSettle();
      expect(find.text('Farm ID (ask your farm owner)'), findsOneWidget);
    });

    testWidgets('renders Register button', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Register'), findsOneWidget);
    });

    testWidgets('phone field is present', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Phone Number'), findsOneWidget);
    });
  });
}

Widget _buildSubject() => ChangeNotifierProvider<AuthProvider>(
      create: (_) => MockAuthProvider(),
      child: const MaterialApp(home: RegisterScreen()),
    );

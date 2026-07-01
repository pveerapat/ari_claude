import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ari_mobile/features/auth/login_screen.dart';
import 'package:ari_mobile/shared/providers/auth_provider.dart';
import 'package:ari_mobile/shared/providers/network_provider.dart';

import '../helpers/mock_providers.dart';

void main() {
  group('LoginScreen widget', () {
    testWidgets('renders phone and password fields', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.byType(TextFormField), findsNWidgets(2));
      expect(find.text('Phone Number'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
    });

    testWidgets('renders Log In button', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Log In'), findsOneWidget);
    });

    testWidgets('shows register link', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.textContaining('Register'), findsOneWidget);
    });

    testWidgets('empty phone shows validation error', (tester) async {
      await tester.pumpWidget(_buildSubject());
      await tester.tap(find.text('Log In'));
      await tester.pumpAndSettle();
      expect(find.text('Phone is required'), findsOneWidget);
    });

    testWidgets('empty password shows validation error', (tester) async {
      await tester.pumpWidget(_buildSubject());
      await tester.enterText(find.byType(TextFormField).first, '0800000001');
      await tester.tap(find.text('Log In'));
      await tester.pumpAndSettle();
      expect(find.text('Password is required'), findsOneWidget);
    });
  });
}

Widget _buildSubject() => MultiProvider(
      providers: [
        ChangeNotifierProvider<AuthProvider>(create: (_) => MockAuthProvider()),
        ChangeNotifierProvider<NetworkProvider>(
            create: (_) => MockNetworkProvider()),
      ],
      child: const MaterialApp(home: LoginScreen()),
    );

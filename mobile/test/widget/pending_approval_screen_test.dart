import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ari_mobile/features/onboarding/pending_approval_screen.dart';
import 'package:ari_mobile/shared/providers/auth_provider.dart';

import '../helpers/mock_providers.dart';

void main() {
  group('PendingApprovalScreen widget', () {
    testWidgets('shows pending approval message', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Waiting for Farm Approval'), findsOneWidget);
    });

    testWidgets('shows logout button', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.byIcon(Icons.logout), findsOneWidget);
    });

    testWidgets('lists blocked features', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Add Note'), findsOneWidget);
      expect(find.text('Farm Notebook'), findsOneWidget);
      expect(find.text('Upload Queue'), findsOneWidget);
      expect(find.text('Sync'), findsOneWidget);
    });

    testWidgets('shows check approval status button', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Check approval status'), findsOneWidget);
    });

    testWidgets('user name is displayed', (tester) async {
      await tester.pumpWidget(_buildSubject());
      expect(find.text('Pending User'), findsOneWidget);
    });
  });
}

Widget _buildSubject() => ChangeNotifierProvider<AuthProvider>(
      create: (_) => MockAuthProviderPending(),
      child: const MaterialApp(home: PendingApprovalScreen()),
    );

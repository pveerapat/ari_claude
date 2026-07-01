import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/shared/models/follow_up_model.dart';

void main() {
  group('FollowUpModel', () {
    test('outcome values are exactly improved/same/worse/unknown', () {
      expect(FollowUpModel.outcomeValues,
          equals(['improved', 'same', 'worse', 'unknown']));
    });

    test('follow_up days are 3/7/14', () {
      expect(FollowUpModel.followUpDays, equals([3, 7, 14]));
    });

    test('fromJson parses outcome', () {
      final json = {
        'id': 'f1',
        'notebook_entry_id': 'e1',
        'follow_up_day': 7,
        'outcome': 'improved',
        'notes': 'Looking better',
        'status': 'completed',
        'due_date': '2026-02-01',
        'created_at': '2026-01-25T00:00:00',
      };
      final fu = FollowUpModel.fromJson(json);
      expect(fu.followUpDay, equals(7));
      expect(fu.outcome, equals('improved'));
      expect(fu.notes, equals('Looking better'));
    });

    test('fromJson allows null outcome', () {
      final json = {
        'id': 'f2',
        'follow_up_day': 3,
        'outcome': null,
        'created_at': '2026-01-25T00:00:00',
      };
      final fu = FollowUpModel.fromJson(json);
      expect(fu.outcome, isNull);
    });
  });
}

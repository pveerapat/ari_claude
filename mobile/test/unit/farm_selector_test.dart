import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:ari_mobile/shared/models/farm_model.dart';
import 'package:ari_mobile/shared/providers/farm_context_provider.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('FarmContextProvider', () {
    late FarmContextProvider provider;

    setUp(() {
      SharedPreferences.setMockInitialValues({});
      provider = FarmContextProvider();
    });

    test('hasFarm is false when no farm set', () {
      expect(provider.hasFarm, isFalse);
      expect(provider.activeFarm, isNull);
    });

    test('updateFarms sets farms list', () {
      final farms = [
        const FarmModel(id: 'f1', name: 'Farm 1'),
        const FarmModel(id: 'f2', name: 'Farm 2'),
      ];
      provider.updateFarms(farms);
      expect(provider.farms.length, equals(2));
    });

    test('clear resets state', () {
      provider.updateFarms([const FarmModel(id: 'f1', name: 'Farm 1')]);
      provider.clear();
      expect(provider.farms, isEmpty);
      expect(provider.activeFarm, isNull);
    });

    test('updateFarms keeps activeFarm if still in list', () async {
      const farm1 = FarmModel(id: 'f1', name: 'Farm 1');
      const farm2 = FarmModel(id: 'f2', name: 'Farm 2');

      await provider.init([farm1, farm2], 'f1');
      expect(provider.activeFarm?.id, equals('f1'));

      // Update list — farm1 still present
      provider.updateFarms([farm1, farm2]);
      expect(provider.activeFarm?.id, equals('f1'));
    });
  });
}

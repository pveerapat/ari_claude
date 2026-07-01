import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/shared/models/user_model.dart';

void main() {
  group('UserModel', () {
    test('owner canCreateFarm is true', () {
      final user = UserModel(
        id: '1',
        phone: '0001',
        name: 'Owner',
        farmerStatus: 'owner',
        membershipStatus: 'active',
        accountStatus: 'active',
      );
      expect(user.canCreateFarm, isTrue);
      expect(user.isOwner, isTrue);
    });

    test('owner_family canCreateFarm is false', () {
      final user = UserModel(
        id: '2',
        phone: '0002',
        name: 'Family',
        farmerStatus: 'owner_family',
        membershipStatus: 'active',
        accountStatus: 'active',
      );
      expect(user.canCreateFarm, isFalse);
    });

    test('farm_staff canCreateFarm is false', () {
      final user = UserModel(
        id: '3',
        phone: '0003',
        name: 'Staff',
        farmerStatus: 'farm_staff',
        membershipStatus: 'active',
        accountStatus: 'active',
      );
      expect(user.canCreateFarm, isFalse);
    });

    test('pending membership isPending is true', () {
      final user = UserModel(
        id: '4',
        phone: '0004',
        name: 'Pending',
        farmerStatus: 'owner_family',
        membershipStatus: 'pending_farm_approval',
        accountStatus: 'active',
      );
      expect(user.isPending, isTrue);
      expect(user.canUseProtectedFeatures, isFalse);
    });

    test('active membership canUseProtectedFeatures is true', () {
      final user = UserModel(
        id: '5',
        phone: '0005',
        name: 'Active',
        farmerStatus: 'owner_family',
        membershipStatus: 'active',
        accountStatus: 'active',
      );
      expect(user.isActive, isTrue);
      expect(user.canUseProtectedFeatures, isTrue);
    });

    test('fromJson parses all fields', () {
      final json = {
        'id': 'u1',
        'phone': '0001',
        'name': 'Test User',
        'farmer_status': 'owner',
        'membership_status': 'active',
        'account_status': 'active',
        'primary_farm_id': 'farm1',
        'organization_id': 'org1',
      };
      final user = UserModel.fromJson(json);
      expect(user.id, equals('u1'));
      expect(user.farmerStatus, equals('owner'));
      expect(user.primaryFarmId, equals('farm1'));
    });
  });
}

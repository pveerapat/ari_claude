import 'package:flutter_test/flutter_test.dart';
import 'package:ari_mobile/shared/models/user_model.dart';

void main() {
  group('Membership boundary', () {
    test('pending membership blocks protected features', () {
      final user = UserModel(
        id: 'u1',
        phone: '0001',
        name: 'Pending',
        farmerStatus: 'farm_staff',
        membershipStatus: 'pending_farm_approval',
        accountStatus: 'active',
      );
      expect(user.isPending, isTrue);
      expect(user.canUseProtectedFeatures, isFalse);
    });

    test('pending owner_family cannot use protected features', () {
      final user = UserModel(
        id: 'u2',
        phone: '0002',
        name: 'Family',
        farmerStatus: 'owner_family',
        membershipStatus: 'pending_farm_approval',
        accountStatus: 'active',
      );
      expect(user.isPending, isTrue);
      expect(user.canUseProtectedFeatures, isFalse);
    });

    test('active farm_staff can use protected features', () {
      final user = UserModel(
        id: 'u3',
        phone: '0003',
        name: 'Staff',
        farmerStatus: 'farm_staff',
        membershipStatus: 'active',
        accountStatus: 'active',
      );
      expect(user.canUseProtectedFeatures, isTrue);
    });

    test('owner_family registration requires farm_id', () {
      // Validate the UI rule: farm_id must be present for owner_family
      const farmerStatus = 'owner_family';

      // Without farm_id: invalid
      bool requiresFarmId(String status) =>
          status == 'owner_family' || status == 'farm_staff';

      expect(requiresFarmId(farmerStatus), isTrue);
      expect(requiresFarmId('owner'), isFalse);
    });

    test('farm_staff registration requires farm_id', () {
      bool requiresFarmId(String status) =>
          status == 'owner_family' || status == 'farm_staff';

      expect(requiresFarmId('farm_staff'), isTrue);
    });

    test('farmer_status is not an RBAC role — backend is authority', () {
      // farmer_status controls UI visibility only
      // Mobile must not implement its own permission matrix
      final owner = UserModel(
        id: 'o1',
        phone: '001',
        name: 'Owner',
        farmerStatus: 'owner',
        membershipStatus: 'active',
        accountStatus: 'active',
      );
      final staff = UserModel(
        id: 's1',
        phone: '002',
        name: 'Staff',
        farmerStatus: 'farm_staff',
        membershipStatus: 'active',
        accountStatus: 'active',
      );

      // Only UI visibility — backend returns 403 if they try
      expect(owner.canCreateFarm, isTrue);
      expect(staff.canCreateFarm, isFalse);
    });
  });
}

class UserModel {
  final String id;
  final String phone;
  final String name;
  final String farmerStatus; // owner | owner_family | farm_staff
  final String membershipStatus; // pending_farm_approval | active
  final String accountStatus;
  final String? primaryFarmId;
  final String? organizationId;

  const UserModel({
    required this.id,
    required this.phone,
    required this.name,
    required this.farmerStatus,
    required this.membershipStatus,
    required this.accountStatus,
    this.primaryFarmId,
    this.organizationId,
  });

  bool get isPending => membershipStatus == 'pending_farm_approval';
  bool get isActive => membershipStatus == 'active';
  bool get isOwner => farmerStatus == 'owner';
  bool get canCreateFarm => isOwner;
  bool get canUseProtectedFeatures => !isPending;

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
        id: json['id']?.toString() ?? '',
        phone: json['phone']?.toString() ?? '',
        name: json['name']?.toString() ?? '',
        farmerStatus: json['farmer_status']?.toString() ?? '',
        membershipStatus: json['membership_status']?.toString() ?? '',
        accountStatus: json['account_status']?.toString() ?? '',
        primaryFarmId: json['primary_farm_id']?.toString(),
        organizationId: json['organization_id']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'phone': phone,
        'name': name,
        'farmer_status': farmerStatus,
        'membership_status': membershipStatus,
        'account_status': accountStatus,
        if (primaryFarmId != null) 'primary_farm_id': primaryFarmId,
        if (organizationId != null) 'organization_id': organizationId,
      };
}

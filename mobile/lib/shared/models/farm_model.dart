class FarmModel {
  final String id;
  final String name;
  final String? description;
  final String? location;
  final String? status;
  final String? organizationId;

  const FarmModel({
    required this.id,
    required this.name,
    this.description,
    this.location,
    this.status,
    this.organizationId,
  });

  factory FarmModel.fromJson(Map<String, dynamic> json) {
    final loc = json['location'];
    String? locationStr;
    if (loc is Map) {
      locationStr = (loc['address'] ?? loc['province'] ?? loc['district'])?.toString();
    } else if (loc is String) {
      locationStr = loc;
    }
    return FarmModel(
      id: (json['farm_id'] ?? json['id'])?.toString() ?? '',
      name: (json['farm_name'] ?? json['name'])?.toString() ?? '',
      description: json['description']?.toString(),
      location: locationStr,
      status: json['status']?.toString(),
      organizationId: json['organization_id']?.toString(),
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        if (description != null) 'description': description,
        if (location != null) 'location': location,
        if (status != null) 'status': status,
        if (organizationId != null) 'organization_id': organizationId,
      };
}

class ZoneModel {
  final String id;
  final String name;
  final String farmId;
  final String? description;
  final String? zoneType;

  const ZoneModel({
    required this.id,
    required this.name,
    required this.farmId,
    this.description,
    this.zoneType,
  });

  factory ZoneModel.fromJson(Map<String, dynamic> json) => ZoneModel(
        id: json['id']?.toString() ?? '',
        name: json['name']?.toString() ?? '',
        farmId: json['farm_id']?.toString() ?? '',
        description: json['description']?.toString(),
        zoneType: json['zone_type']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'farm_id': farmId,
        if (description != null) 'description': description,
        if (zoneType != null) 'zone_type': zoneType,
      };
}

class TreeModel {
  final String id;
  final String? label;
  final String zoneId;
  final String farmId;
  final String? species;
  final String? status;

  const TreeModel({
    required this.id,
    this.label,
    required this.zoneId,
    required this.farmId,
    this.species,
    this.status,
  });

  factory TreeModel.fromJson(Map<String, dynamic> json) => TreeModel(
        id: json['id']?.toString() ?? '',
        label: json['label']?.toString(),
        zoneId: json['zone_id']?.toString() ?? '',
        farmId: json['farm_id']?.toString() ?? '',
        species: json['species']?.toString(),
        status: json['status']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        if (label != null) 'label': label,
        'zone_id': zoneId,
        'farm_id': farmId,
        if (species != null) 'species': species,
        if (status != null) 'status': status,
      };
}

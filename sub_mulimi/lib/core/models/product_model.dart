import 'user_model.dart';

class ProductModel {
  final int id;
  final UserModel seller;
  final String name;
  final String category;
  final String description;
  final double quantity;
  final String unit;
  final double pricePerUnit;
  final DateTime harvestDate;
  final String location;
  final String contactPhone;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;
  final List<ProductImage> images;

  ProductModel({
    required this.id,
    required this.seller,
    required this.name,
    required this.category,
    required this.description,
    required this.quantity,
    required this.unit,
    required this.pricePerUnit,
    required this.harvestDate,
    required this.location,
    required this.contactPhone,
    this.isActive = true,
    required this.createdAt,
    required this.updatedAt,
    this.images = const [],
  });

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'],
      seller: UserModel.fromJson(json['seller']),
      name: json['name'],
      category: json['category'],
      description: json['description'],
      quantity: double.parse(json['quantity'].toString()),
      unit: json['unit'],
      pricePerUnit: double.parse(json['price_per_unit'].toString()),
      harvestDate: DateTime.parse(json['harvest_date']),
      location: json['location'],
      contactPhone: json['contact_phone'],
      isActive: json['is_active'] ?? true,
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      images:
          (json['images'] as List?)
              ?.map((img) => ProductImage.fromJson(img))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'seller': seller.toJson(),
      'name': name,
      'category': category,
      'description': description,
      'quantity': quantity,
      'unit': unit,
      'price_per_unit': pricePerUnit,
      'harvest_date': harvestDate.toIso8601String().split('T')[0],
      'location': location,
      'contact_phone': contactPhone,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'images': images.map((img) => img.toJson()).toList(),
    };
  }

  String get categoryDisplayName {
    switch (category) {
      case 'GRAINS':
        return 'Grains';
      case 'VEGETABLES':
        return 'Vegetables';
      case 'FRUITS':
        return 'Fruits';
      case 'LIVESTOCK':
        return 'Livestock';
      case 'DAIRY':
        return 'Dairy';
      case 'OTHER':
        return 'Other';
      default:
        return category;
    }
  }

  String get statusText {
    return isActive ? 'Available' : 'Sold Out';
  }

  double get totalValue {
    return quantity * pricePerUnit;
  }

  String get formattedPrice {
    return 'MWK ${pricePerUnit.toStringAsFixed(2)}';
  }

  String get formattedTotalValue {
    return 'MWK ${totalValue.toStringAsFixed(2)}';
  }

  bool get hasImages {
    return images.isNotEmpty;
  }

  String? get primaryImageUrl {
    return hasImages ? images.first.imageUrl : null;
  }

  int get daysToHarvest {
    final now = DateTime.now();
    final difference = harvestDate.difference(now);
    return difference.inDays;
  }

  bool get isHarvested {
    return DateTime.now().isAfter(harvestDate);
  }

  ProductModel copyWith({
    int? id,
    UserModel? seller,
    String? name,
    String? category,
    String? description,
    double? quantity,
    String? unit,
    double? pricePerUnit,
    DateTime? harvestDate,
    String? location,
    String? contactPhone,
    bool? isActive,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<ProductImage>? images,
  }) {
    return ProductModel(
      id: id ?? this.id,
      seller: seller ?? this.seller,
      name: name ?? this.name,
      category: category ?? this.category,
      description: description ?? this.description,
      quantity: quantity ?? this.quantity,
      unit: unit ?? this.unit,
      pricePerUnit: pricePerUnit ?? this.pricePerUnit,
      harvestDate: harvestDate ?? this.harvestDate,
      location: location ?? this.location,
      contactPhone: contactPhone ?? this.contactPhone,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      images: images ?? this.images,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is ProductModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'ProductModel(id: $id, name: $name, category: $category, seller: ${seller.username})';
  }
}

class ProductImage {
  final int id;
  final String image;
  final DateTime uploadedAt;

  ProductImage({
    required this.id,
    required this.image,
    required this.uploadedAt,
  });

  factory ProductImage.fromJson(Map<String, dynamic> json) {
    return ProductImage(
      id: json['id'],
      image: json['image'],
      uploadedAt: DateTime.parse(json['uploaded_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'image': image,
      'uploaded_at': uploadedAt.toIso8601String(),
    };
  }

  String get imageUrl {
    // If image is already a full URL, return as is
    if (image.startsWith('http')) {
      return image;
    }
    // Otherwise, construct full URL with base URL
    return 'http://10.0.2.2:8000$image';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is ProductImage && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'ProductImage(id: $id, image: $image)';
  }
}

// Product creation/update request model
class ProductCreateRequest {
  final String name;
  final String category;
  final String description;
  final double quantity;
  final String unit;
  final double pricePerUnit;
  final DateTime harvestDate;
  final String location;
  final String contactPhone;

  ProductCreateRequest({
    required this.name,
    required this.category,
    required this.description,
    required this.quantity,
    required this.unit,
    required this.pricePerUnit,
    required this.harvestDate,
    required this.location,
    required this.contactPhone,
  });

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'category': category,
      'description': description,
      'quantity': quantity,
      'unit': unit,
      'price_per_unit': pricePerUnit,
      'harvest_date': harvestDate.toIso8601String().split('T')[0],
      'location': location,
      'contact_phone': contactPhone,
    };
  }
}

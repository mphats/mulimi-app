class UserModel {
  final int id;
  final String username;
  final String email;
  final String role;
  final String? firstName;
  final String? lastName;
  final bool isActive;
  final DateTime? dateJoined;

  UserModel({
    required this.id,
    required this.username,
    required this.email,
    required this.role,
    this.firstName,
    this.lastName,
    this.isActive = true,
    this.dateJoined,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      role: json['role'] ?? 'FARMER',
      firstName: json['first_name'],
      lastName: json['last_name'],
      isActive: json['is_active'] ?? true,
      dateJoined: json['date_joined'] != null
          ? DateTime.parse(json['date_joined'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'role': role,
      'first_name': firstName,
      'last_name': lastName,
      'is_active': isActive,
      'date_joined': dateJoined?.toIso8601String(),
    };
  }

  String get displayName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    }
    return username;
  }

  String get initials {
    if (firstName != null && lastName != null) {
      return '${firstName![0]}${lastName![0]}'.toUpperCase();
    }
    return username.length >= 2
        ? username.substring(0, 2).toUpperCase()
        : username.toUpperCase();
  }

  String get roleDisplayName {
    switch (role) {
      case 'FARMER':
        return 'Farmer';
      case 'TRADER':
        return 'Trader';
      case 'AGRONOMIST':
        return 'Agronomist';
      case 'ADMIN':
        return 'Admin';
      default:
        return role;
    }
  }

  UserModel copyWith({
    int? id,
    String? username,
    String? email,
    String? role,
    String? firstName,
    String? lastName,
    bool? isActive,
    DateTime? dateJoined,
  }) {
    return UserModel(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      role: role ?? this.role,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      isActive: isActive ?? this.isActive,
      dateJoined: dateJoined ?? this.dateJoined,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is UserModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'UserModel(id: $id, username: $username, email: $email, role: $role)';
  }
}

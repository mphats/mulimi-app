import 'user_model.dart';

class PestDiagnosisModel {
  final int id;
  final UserModel user;
  final String cropType;
  final String symptoms;
  final String image;
  final String diagnosis;
  final double confidenceScore;
  final String treatmentAdvice;
  final DateTime createdAt;

  PestDiagnosisModel({
    required this.id,
    required this.user,
    required this.cropType,
    required this.symptoms,
    required this.image,
    required this.diagnosis,
    required this.confidenceScore,
    required this.treatmentAdvice,
    required this.createdAt,
  });

  factory PestDiagnosisModel.fromJson(Map<String, dynamic> json) {
    return PestDiagnosisModel(
      id: json['id'],
      user: UserModel.fromJson(json['user']),
      cropType: json['crop_type'],
      symptoms: json['symptoms'],
      image: json['image'],
      diagnosis: json['diagnosis'],
      confidenceScore: double.parse(json['confidence_score'].toString()),
      treatmentAdvice: json['treatment_advice'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user': user.toJson(),
      'crop_type': cropType,
      'symptoms': symptoms,
      'image': image,
      'diagnosis': diagnosis,
      'confidence_score': confidenceScore,
      'treatment_advice': treatmentAdvice,
      'created_at': createdAt.toIso8601String(),
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

  String get confidencePercentage {
    return '${(confidenceScore * 100).toStringAsFixed(1)}%';
  }

  String get confidenceLevel {
    if (confidenceScore >= 0.8) {
      return 'High';
    } else if (confidenceScore >= 0.6) {
      return 'Medium';
    } else {
      return 'Low';
    }
  }

  String get timeAgo {
    final now = DateTime.now();
    final difference = now.difference(createdAt);

    if (difference.inDays > 0) {
      return '${difference.inDays} days ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hours ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minutes ago';
    } else {
      return 'Just now';
    }
  }

  bool get isReliable {
    return confidenceScore >= 0.7;
  }

  String get cropTypeDisplay {
    return cropType
        .split(' ')
        .map((word) => word[0].toUpperCase() + word.substring(1).toLowerCase())
        .join(' ');
  }

  PestDiagnosisModel copyWith({
    int? id,
    UserModel? user,
    String? cropType,
    String? symptoms,
    String? image,
    String? diagnosis,
    double? confidenceScore,
    String? treatmentAdvice,
    DateTime? createdAt,
  }) {
    return PestDiagnosisModel(
      id: id ?? this.id,
      user: user ?? this.user,
      cropType: cropType ?? this.cropType,
      symptoms: symptoms ?? this.symptoms,
      image: image ?? this.image,
      diagnosis: diagnosis ?? this.diagnosis,
      confidenceScore: confidenceScore ?? this.confidenceScore,
      treatmentAdvice: treatmentAdvice ?? this.treatmentAdvice,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is PestDiagnosisModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'PestDiagnosisModel(id: $id, cropType: $cropType, diagnosis: $diagnosis, confidence: $confidenceScore)';
  }
}

// Pest diagnosis request model
class PestDiagnosisRequest {
  final String cropType;
  final String symptoms;

  PestDiagnosisRequest({required this.cropType, required this.symptoms});

  Map<String, dynamic> toJson() {
    return {'crop_type': cropType, 'symptoms': symptoms};
  }
}

// AI diagnosis result model (for real-time responses)
class DiagnosisResult {
  final String diagnosis;
  final String treatment;
  final double confidence;
  final String? taskId; // For async processing
  final DiagnosisStatus status;

  DiagnosisResult({
    required this.diagnosis,
    required this.treatment,
    required this.confidence,
    this.taskId,
    this.status = DiagnosisStatus.completed,
  });

  factory DiagnosisResult.fromJson(Map<String, dynamic> json) {
    return DiagnosisResult(
      diagnosis: json['diagnosis'] ?? '',
      treatment: json['treatment'] ?? '',
      confidence: double.tryParse(json['confidence'].toString()) ?? 0.0,
      taskId: json['task_id'],
      status: _parseStatus(json['status']),
    );
  }

  static DiagnosisStatus _parseStatus(dynamic status) {
    if (status == null) return DiagnosisStatus.completed;

    switch (status.toString().toLowerCase()) {
      case 'pending':
        return DiagnosisStatus.pending;
      case 'processing':
        return DiagnosisStatus.processing;
      case 'completed':
        return DiagnosisStatus.completed;
      case 'failed':
        return DiagnosisStatus.failed;
      default:
        return DiagnosisStatus.completed;
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'diagnosis': diagnosis,
      'treatment': treatment,
      'confidence': confidence,
      'task_id': taskId,
      'status': status.name,
    };
  }

  String get confidencePercentage {
    return '${(confidence * 100).toStringAsFixed(1)}%';
  }

  String get confidenceLevel {
    if (confidence >= 0.8) {
      return 'High';
    } else if (confidence >= 0.6) {
      return 'Medium';
    } else {
      return 'Low';
    }
  }

  bool get isReliable {
    return confidence >= 0.7;
  }

  bool get isProcessing {
    return status == DiagnosisStatus.pending ||
        status == DiagnosisStatus.processing;
  }

  bool get isCompleted {
    return status == DiagnosisStatus.completed;
  }

  bool get hasFailed {
    return status == DiagnosisStatus.failed;
  }

  DiagnosisResult copyWith({
    String? diagnosis,
    String? treatment,
    double? confidence,
    String? taskId,
    DiagnosisStatus? status,
  }) {
    return DiagnosisResult(
      diagnosis: diagnosis ?? this.diagnosis,
      treatment: treatment ?? this.treatment,
      confidence: confidence ?? this.confidence,
      taskId: taskId ?? this.taskId,
      status: status ?? this.status,
    );
  }

  @override
  String toString() {
    return 'DiagnosisResult(diagnosis: $diagnosis, confidence: $confidence, status: $status)';
  }
}

enum DiagnosisStatus { pending, processing, completed, failed }

extension DiagnosisStatusExtension on DiagnosisStatus {
  String get displayName {
    switch (this) {
      case DiagnosisStatus.pending:
        return 'Pending';
      case DiagnosisStatus.processing:
        return 'Processing';
      case DiagnosisStatus.completed:
        return 'Completed';
      case DiagnosisStatus.failed:
        return 'Failed';
    }
  }

  String get icon {
    switch (this) {
      case DiagnosisStatus.pending:
        return '⏳';
      case DiagnosisStatus.processing:
        return '🔄';
      case DiagnosisStatus.completed:
        return '✅';
      case DiagnosisStatus.failed:
        return '❌';
    }
  }
}

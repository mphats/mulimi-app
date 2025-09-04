import 'dart:io';
import 'package:dio/dio.dart';
import '../constants/app_constants.dart';
import '../models/product_model.dart';
import 'api_service.dart';

class ProductService {
  final ApiService _apiService = ApiService();

  // Get products with filtering and pagination
  Future<ProductResult> getProducts({
    String? category,
    String? location,
    String? search,
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final queryParameters = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
      };

      if (category != null && category.isNotEmpty) {
        queryParameters['category'] = category;
      }
      if (location != null && location.isNotEmpty) {
        queryParameters['location'] = location;
      }
      if (search != null && search.isNotEmpty) {
        queryParameters['search'] = search;
      }

      final response = await _apiService.get(
        AppConstants.products,
        queryParameters: queryParameters,
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final products = (data['results'] as List)
            .map((json) => ProductModel.fromJson(json))
            .toList();

        return ProductResult.success(
          products: products,
          totalCount: data['count'] ?? products.length,
          hasNext: data['next'] != null,
          hasPrevious: data['previous'] != null,
        );
      }

      return ProductResult.failure('Failed to fetch products');
    } on ApiException catch (e) {
      return ProductResult.failure('Failed to fetch products: ${e.message}');
    } catch (e) {
      return ProductResult.failure('Failed to fetch products: ${e.toString()}');
    }
  }

  // Get product by ID
  Future<ProductResult> getProduct(int productId) async {
    try {
      final response = await _apiService.get(
        '${AppConstants.products}/$productId',
      );

      if (response.statusCode == 200) {
        final product = ProductModel.fromJson(response.data);
        return ProductResult.success(products: [product]);
      }

      return ProductResult.failure('Product not found');
    } on ApiException catch (e) {
      return ProductResult.failure('Failed to fetch product: ${e.message}');
    } catch (e) {
      return ProductResult.failure('Failed to fetch product: ${e.toString()}');
    }
  }

  // Create new product
  Future<ProductResult> createProduct(ProductCreateRequest request) async {
    try {
      final response = await _apiService.post(
        AppConstants.products,
        data: request.toJson(),
      );

      if (response.statusCode == 201) {
        final product = ProductModel.fromJson(response.data);
        return ProductResult.success(
          products: [product],
          message: 'Product created successfully',
        );
      }

      return ProductResult.failure('Failed to create product');
    } on ValidationException catch (e) {
      return ProductResult.failure('Validation error: ${e.message}');
    } on ApiException catch (e) {
      return ProductResult.failure('Failed to create product: ${e.message}');
    } catch (e) {
      return ProductResult.failure('Failed to create product: ${e.toString()}');
    }
  }

  // Update product
  Future<ProductResult> updateProduct(
    int productId,
    ProductCreateRequest request,
  ) async {
    try {
      final response = await _apiService.put(
        '${AppConstants.products}/$productId',
        data: request.toJson(),
      );

      if (response.statusCode == 200) {
        final product = ProductModel.fromJson(response.data);
        return ProductResult.success(
          products: [product],
          message: 'Product updated successfully',
        );
      }

      return ProductResult.failure('Failed to update product');
    } on ValidationException catch (e) {
      return ProductResult.failure('Validation error: ${e.message}');
    } on ApiException catch (e) {
      return ProductResult.failure('Failed to update product: ${e.message}');
    } catch (e) {
      return ProductResult.failure('Failed to update product: ${e.toString()}');
    }
  }

  // Delete product
  Future<ProductResult> deleteProduct(int productId) async {
    try {
      final response = await _apiService.delete(
        '${AppConstants.products}/$productId',
      );

      if (response.statusCode == 204) {
        return ProductResult.success(
          products: [],
          message: 'Product deleted successfully',
        );
      }

      return ProductResult.failure('Failed to delete product');
    } on ApiException catch (e) {
      return ProductResult.failure('Failed to delete product: ${e.message}');
    } catch (e) {
      return ProductResult.failure('Failed to delete product: ${e.toString()}');
    }
  }

  // Upload product images
  Future<ProductResult> uploadProductImages(
    int productId,
    List<File> images,
  ) async {
    try {
      final formData = FormData();

      for (int i = 0; i < images.length; i++) {
        formData.files.add(
          MapEntry(
            'images',
            await MultipartFile.fromFile(
              images[i].path,
              filename: 'product_image_$i.jpg',
            ),
          ),
        );
      }

      final endpoint = AppConstants.productImages.replaceAll(
        '{id}',
        productId.toString(),
      );
      final response = await _apiService.postMultipart(endpoint, formData);

      if (response.statusCode == 201) {
        return ProductResult.success(
          products: [],
          message: 'Images uploaded successfully',
        );
      }

      return ProductResult.failure('Failed to upload images');
    } on ApiException catch (e) {
      return ProductResult.failure('Failed to upload images: ${e.message}');
    } catch (e) {
      return ProductResult.failure('Failed to upload images: ${e.toString()}');
    }
  }

  // Get user's products
  Future<ProductResult> getUserProducts({
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final queryParameters = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
        'user_products': true, // Filter for current user's products
      };

      final response = await _apiService.get(
        AppConstants.products,
        queryParameters: queryParameters,
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final products = (data['results'] as List)
            .map((json) => ProductModel.fromJson(json))
            .toList();

        return ProductResult.success(
          products: products,
          totalCount: data['count'] ?? products.length,
          hasNext: data['next'] != null,
          hasPrevious: data['previous'] != null,
        );
      }

      return ProductResult.failure('Failed to fetch user products');
    } on ApiException catch (e) {
      return ProductResult.failure(
        'Failed to fetch user products: ${e.message}',
      );
    } catch (e) {
      return ProductResult.failure(
        'Failed to fetch user products: ${e.toString()}',
      );
    }
  }

  // Toggle product active status
  Future<ProductResult> toggleProductStatus(
    int productId,
    bool isActive,
  ) async {
    try {
      final response = await _apiService.patch(
        '${AppConstants.products}/$productId',
        data: {'is_active': isActive},
      );

      if (response.statusCode == 200) {
        final product = ProductModel.fromJson(response.data);
        return ProductResult.success(
          products: [product],
          message: isActive ? 'Product activated' : 'Product deactivated',
        );
      }

      return ProductResult.failure('Failed to update product status');
    } on ApiException catch (e) {
      return ProductResult.failure(
        'Failed to update product status: ${e.message}',
      );
    } catch (e) {
      return ProductResult.failure(
        'Failed to update product status: ${e.toString()}',
      );
    }
  }
}

// Product service result wrapper
class ProductResult {
  final bool isSuccess;
  final String message;
  final List<ProductModel> products;
  final int totalCount;
  final bool hasNext;
  final bool hasPrevious;

  ProductResult._({
    required this.isSuccess,
    required this.message,
    required this.products,
    this.totalCount = 0,
    this.hasNext = false,
    this.hasPrevious = false,
  });

  factory ProductResult.success({
    required List<ProductModel> products,
    String message = 'Success',
    int totalCount = 0,
    bool hasNext = false,
    bool hasPrevious = false,
  }) {
    return ProductResult._(
      isSuccess: true,
      message: message,
      products: products,
      totalCount: totalCount,
      hasNext: hasNext,
      hasPrevious: hasPrevious,
    );
  }

  factory ProductResult.failure(String message) {
    return ProductResult._(isSuccess: false, message: message, products: []);
  }

  bool get isFailure => !isSuccess;
  bool get hasProducts => products.isNotEmpty;
  ProductModel? get firstProduct => products.isNotEmpty ? products.first : null;

  @override
  String toString() {
    return 'ProductResult(isSuccess: $isSuccess, message: $message, productCount: ${products.length})';
  }
}

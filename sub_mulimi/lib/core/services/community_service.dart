import '../constants/app_constants.dart';
import '../models/community_model.dart';
import 'api_service.dart';

class CommunityService {
  final ApiService _apiService = ApiService();

  // Get community posts with filtering and pagination
  Future<CommunityResult> getPosts({
    String? category,
    String? search,
    bool? isQuestion,
    bool? isResolved,
    int page = 1,
    int pageSize = 20,
    String orderBy = '-created_at',
  }) async {
    try {
      final queryParameters = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
        'ordering': orderBy,
      };

      if (category != null && category.isNotEmpty) {
        queryParameters['category'] = category;
      }
      if (search != null && search.isNotEmpty) {
        queryParameters['search'] = search;
      }
      if (isQuestion != null) {
        queryParameters['is_question'] = isQuestion;
      }
      if (isResolved != null) {
        queryParameters['is_resolved'] = isResolved;
      }

      final response = await _apiService.get(
        AppConstants.communityPosts,
        queryParameters: queryParameters,
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final posts = (data['results'] as List)
            .map((json) => CommunityPostModel.fromJson(json))
            .toList();

        return CommunityResult.success(
          posts: posts,
          totalCount: data['count'] ?? posts.length,
          hasNext: data['next'] != null,
          hasPrevious: data['previous'] != null,
        );
      }

      return CommunityResult.failure('Failed to fetch posts');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to fetch posts: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to fetch posts: ${e.toString()}');
    }
  }

  // Get post by ID with replies
  Future<CommunityResult> getPost(int postId) async {
    try {
      final response = await _apiService.get(
        '${AppConstants.communityPosts}/$postId',
      );

      if (response.statusCode == 200) {
        final post = CommunityPostModel.fromJson(response.data);
        return CommunityResult.success(posts: [post]);
      }

      return CommunityResult.failure('Post not found');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to fetch post: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to fetch post: ${e.toString()}');
    }
  }

  // Create new post
  Future<CommunityResult> createPost(CommunityPostCreateRequest request) async {
    try {
      final response = await _apiService.post(
        AppConstants.communityPosts,
        data: request.toJson(),
      );

      if (response.statusCode == 201) {
        final post = CommunityPostModel.fromJson(response.data);
        return CommunityResult.success(
          posts: [post],
          message: 'Post created successfully',
        );
      }

      return CommunityResult.failure('Failed to create post');
    } on ValidationException catch (e) {
      return CommunityResult.failure('Validation error: ${e.message}');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to create post: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to create post: ${e.toString()}');
    }
  }

  // Update post
  Future<CommunityResult> updatePost(
    int postId,
    CommunityPostCreateRequest request,
  ) async {
    try {
      final response = await _apiService.put(
        '${AppConstants.communityPosts}/$postId',
        data: request.toJson(),
      );

      if (response.statusCode == 200) {
        final post = CommunityPostModel.fromJson(response.data);
        return CommunityResult.success(
          posts: [post],
          message: 'Post updated successfully',
        );
      }

      return CommunityResult.failure('Failed to update post');
    } on ValidationException catch (e) {
      return CommunityResult.failure('Validation error: ${e.message}');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to update post: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to update post: ${e.toString()}');
    }
  }

  // Delete post
  Future<CommunityResult> deletePost(int postId) async {
    try {
      final response = await _apiService.delete(
        '${AppConstants.communityPosts}/$postId',
      );

      if (response.statusCode == 204) {
        return CommunityResult.success(
          posts: [],
          message: 'Post deleted successfully',
        );
      }

      return CommunityResult.failure('Failed to delete post');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to delete post: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to delete post: ${e.toString()}');
    }
  }

  // Add reply to post
  Future<CommunityResult> addReply(
    int postId,
    CommunityReplyCreateRequest request,
  ) async {
    try {
      final endpoint = AppConstants.communityReplies.replaceAll(
        '{id}',
        postId.toString(),
      );
      final response = await _apiService.post(endpoint, data: request.toJson());

      if (response.statusCode == 201) {
        final reply = CommunityReplyModel.fromJson(response.data);
        return CommunityResult.success(
          replies: [reply],
          message: 'Reply added successfully',
        );
      }

      return CommunityResult.failure('Failed to add reply');
    } on ValidationException catch (e) {
      return CommunityResult.failure('Validation error: ${e.message}');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to add reply: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to add reply: ${e.toString()}');
    }
  }

  // Like/unlike post
  Future<CommunityResult> togglePostLike(int postId) async {
    try {
      final endpoint = AppConstants.postLike.replaceAll(
        '{id}',
        postId.toString(),
      );
      final response = await _apiService.post(endpoint);

      if (response.statusCode == 200) {
        final data = response.data;
        final isLiked = data['liked'] ?? false;
        final likeCount = data['like_count'] ?? 0;

        return CommunityResult.success(
          posts: [],
          message: isLiked ? 'Post liked' : 'Post unliked',
          extraData: {'is_liked': isLiked, 'like_count': likeCount},
        );
      }

      return CommunityResult.failure('Failed to toggle like');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to toggle like: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to toggle like: ${e.toString()}');
    }
  }

  // Like/unlike reply
  Future<CommunityResult> toggleReplyLike(int replyId) async {
    try {
      final endpoint = AppConstants.replyLike.replaceAll(
        '{id}',
        replyId.toString(),
      );
      final response = await _apiService.post(endpoint);

      if (response.statusCode == 200) {
        final data = response.data;
        final isLiked = data['liked'] ?? false;
        final likeCount = data['like_count'] ?? 0;

        return CommunityResult.success(
          replies: [],
          message: isLiked ? 'Reply liked' : 'Reply unliked',
          extraData: {'is_liked': isLiked, 'like_count': likeCount},
        );
      }

      return CommunityResult.failure('Failed to toggle reply like');
    } on ApiException catch (e) {
      return CommunityResult.failure(
        'Failed to toggle reply like: ${e.message}',
      );
    } catch (e) {
      return CommunityResult.failure(
        'Failed to toggle reply like: ${e.toString()}',
      );
    }
  }

  // Share post
  Future<CommunityResult> sharePost(int postId, String method) async {
    try {
      final endpoint = AppConstants.postShare.replaceAll(
        '{id}',
        postId.toString(),
      );
      final response = await _apiService.post(
        endpoint,
        data: {'method': method},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final shareCount = data['share_count'] ?? 0;

        return CommunityResult.success(
          posts: [],
          message: 'Post shared successfully',
          extraData: {'share_count': shareCount},
        );
      }

      return CommunityResult.failure('Failed to share post');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to share post: ${e.message}');
    } catch (e) {
      return CommunityResult.failure('Failed to share post: ${e.toString()}');
    }
  }

  // Track post view
  Future<CommunityResult> trackPostView(int postId) async {
    try {
      final endpoint = AppConstants.postView.replaceAll(
        '{id}',
        postId.toString(),
      );
      final response = await _apiService.post(endpoint);

      if (response.statusCode == 200) {
        final data = response.data;
        final viewCount = data['view_count'] ?? 0;

        return CommunityResult.success(
          posts: [],
          message: 'Post view tracked',
          extraData: {'view_count': viewCount},
        );
      }

      return CommunityResult.failure('Failed to track post view');
    } on ApiException catch (e) {
      return CommunityResult.failure('Failed to track post view: ${e.message}');
    } catch (e) {
      return CommunityResult.failure(
        'Failed to track post view: ${e.toString()}',
      );
    }
  }

  // Mark reply as solution
  Future<CommunityResult> markReplyAsSolution(int replyId) async {
    try {
      final endpoint = AppConstants.markSolution.replaceAll(
        '{id}',
        replyId.toString(),
      );
      final response = await _apiService.post(endpoint);

      if (response.statusCode == 200) {
        final reply = CommunityReplyModel.fromJson(response.data);
        return CommunityResult.success(
          replies: [reply],
          message: 'Reply marked as solution',
        );
      }

      return CommunityResult.failure('Failed to mark reply as solution');
    } on ApiException catch (e) {
      return CommunityResult.failure(
        'Failed to mark reply as solution: ${e.message}',
      );
    } catch (e) {
      return CommunityResult.failure(
        'Failed to mark reply as solution: ${e.toString()}',
      );
    }
  }

  // Get user's posts
  Future<CommunityResult> getUserPosts({
    int page = 1,
    int pageSize = 20,
  }) async {
    try {
      final queryParameters = <String, dynamic>{
        'page': page,
        'page_size': pageSize,
        'user_posts': true, // Filter for current user's posts
        'ordering': '-created_at',
      };

      final response = await _apiService.get(
        AppConstants.communityPosts,
        queryParameters: queryParameters,
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final posts = (data['results'] as List)
            .map((json) => CommunityPostModel.fromJson(json))
            .toList();

        return CommunityResult.success(
          posts: posts,
          totalCount: data['count'] ?? posts.length,
          hasNext: data['next'] != null,
          hasPrevious: data['previous'] != null,
        );
      }

      return CommunityResult.failure('Failed to fetch user posts');
    } on ApiException catch (e) {
      return CommunityResult.failure(
        'Failed to fetch user posts: ${e.message}',
      );
    } catch (e) {
      return CommunityResult.failure(
        'Failed to fetch user posts: ${e.toString()}',
      );
    }
  }
}

// Community service result wrapper
class CommunityResult {
  final bool isSuccess;
  final String message;
  final List<CommunityPostModel> posts;
  final List<CommunityReplyModel> replies;
  final int totalCount;
  final bool hasNext;
  final bool hasPrevious;
  final Map<String, dynamic>? extraData;

  CommunityResult._({
    required this.isSuccess,
    required this.message,
    required this.posts,
    required this.replies,
    this.totalCount = 0,
    this.hasNext = false,
    this.hasPrevious = false,
    this.extraData,
  });

  factory CommunityResult.success({
    List<CommunityPostModel> posts = const [],
    List<CommunityReplyModel> replies = const [],
    String message = 'Success',
    int totalCount = 0,
    bool hasNext = false,
    bool hasPrevious = false,
    Map<String, dynamic>? extraData,
  }) {
    return CommunityResult._(
      isSuccess: true,
      message: message,
      posts: posts,
      replies: replies,
      totalCount: totalCount,
      hasNext: hasNext,
      hasPrevious: hasPrevious,
      extraData: extraData,
    );
  }

  factory CommunityResult.failure(String message) {
    return CommunityResult._(
      isSuccess: false,
      message: message,
      posts: [],
      replies: [],
    );
  }

  bool get isFailure => !isSuccess;
  bool get hasPosts => posts.isNotEmpty;
  bool get hasReplies => replies.isNotEmpty;
  CommunityPostModel? get firstPost => posts.isNotEmpty ? posts.first : null;
  CommunityReplyModel? get firstReply =>
      replies.isNotEmpty ? replies.first : null;

  @override
  String toString() {
    return 'CommunityResult(isSuccess: $isSuccess, message: $message, postCount: ${posts.length}, replyCount: ${replies.length})';
  }
}

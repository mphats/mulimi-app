import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_strings.dart';
import '../../core/models/community_model.dart';
import '../../core/services/community_service.dart';
import '../../widgets/empty_state.dart';
import '../../widgets/error_state.dart';
import '../../widgets/shimmer_list.dart';
import 'create_post_screen.dart';

class CommunityScreen extends StatefulWidget {
  const CommunityScreen({super.key});

  @override
  State<CommunityScreen> createState() => _CommunityScreenState();
}

class _CommunityScreenState extends State<CommunityScreen> {
  final _service = CommunityService();
  bool _isLoading = true;
  String? _error;
  List<CommunityPostModel> _posts = [];
  String? _category;
  String? _search;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });
    final res = await _service.getPosts(
      category: _category,
      search: _search,
    );
    if (!mounted) return;
    setState(() {
      _isLoading = false;
      if (res.isSuccess) {
        _posts = res.posts;
      } else {
        _error = res.message;
      }
    });
  }

  void _openCreatePost() async {
    await Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => const CreatePostScreen()),
    );
    if (mounted) _fetch();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(AppStrings.community),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        automaticallyImplyLeading: false,
        actions: [
          IconButton(onPressed: _openCreatePost, icon: const Icon(Icons.add_comment_outlined))
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _fetch,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildFilters(),
              const SizedBox(height: 12),
              if (_isLoading) const ShimmerList(height: 100),
              if (!_isLoading && _error != null)
                ErrorState(title: 'Failed to load', message: _error, onRetry: _fetch),
              if (!_isLoading && _error == null && _posts.isEmpty)
                const EmptyState(
                  icon: Icons.forum_outlined,
                  title: 'No posts yet',
                  message: 'Start a discussion or ask a question.',
                ),
              if (!_isLoading && _error == null && _posts.isNotEmpty)
                _buildList(),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openCreatePost,
        child: const Icon(Icons.edit_outlined),
      ),
    );
  }
}

extension on _CommunityScreenState {
  Widget _buildFilters() {
    return Row(
      children: [
        Expanded(
          child: TextField(
            decoration: const InputDecoration(
              hintText: 'Search posts',
              prefixIcon: Icon(Icons.search),
            ),
            onChanged: (v) => _search = v,
            onSubmitted: (_) => _fetch(),
          ),
        ),
        const SizedBox(width: 12),
        SizedBox(
          width: 150,
          child: DropdownButtonFormField<String>(
            value: _category,
            isExpanded: true,
            items: const [
              DropdownMenuItem(value: null, child: Text('All')),
              DropdownMenuItem(value: 'question', child: Text('Question')),
              DropdownMenuItem(value: 'advice', child: Text('Advice')),
              DropdownMenuItem(value: 'discussion', child: Text('Discussion')),
            ],
            onChanged: (v) {
              setState(() => _category = v);
              _fetch();
            },
            decoration: const InputDecoration(labelText: 'Category'),
          ),
        ),
      ],
    );
  }

  Widget _buildList() {
    return ListView.separated(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: _posts.length,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, index) {
        final p = _posts[index];
        return Container(
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.05),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: AppColors.surfaceVariant,
              child: Text(p.author.initials),
            ),
            title: Text(p.title),
            subtitle: Text(p.content, maxLines: 2, overflow: TextOverflow.ellipsis),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.thumb_up_off_alt, size: 16),
                    const SizedBox(width: 4),
                    Text(p.likeCount.toString()),
                  ],
                ),
                const SizedBox(height: 4),
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.comment_outlined, size: 16),
                    const SizedBox(width: 4),
                    Text(p.replyCount.toString()),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

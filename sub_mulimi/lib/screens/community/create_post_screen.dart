import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';
import '../../core/services/community_service.dart';
import '../../core/models/community_model.dart';

class CreatePostScreen extends StatefulWidget {
  const CreatePostScreen({super.key});

  @override
  State<CreatePostScreen> createState() => _CreatePostScreenState();
}

class _CreatePostScreenState extends State<CreatePostScreen> {
  final _formKey = GlobalKey<FormState>();
  final _title = TextEditingController();
  final _content = TextEditingController();
  String _category = 'general';
  bool _isQuestion = false;
  bool _submitting = false;
  final _service = CommunityService();

  @override
  void dispose() {
    _title.dispose();
    _content.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _submitting = true);
    final req = CommunityPostCreateRequest(
      title: _title.text.trim(),
      content: _content.text.trim(),
      category: _category,
      isQuestion: _isQuestion,
    );
    final res = await _service.createPost(req);
    if (!mounted) return;
    setState(() => _submitting = false);
    if (res.isSuccess) {
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Post created')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(res.message)),
      );
    }
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Post'),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _title,
                decoration: const InputDecoration(labelText: 'Title'),
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Required' : null,
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: _category,
                items: const [
                  DropdownMenuItem(value: 'question', child: Text('Question')),
                  DropdownMenuItem(value: 'advice', child: Text('Advice')),
                  DropdownMenuItem(value: 'discussion', child: Text('Discussion')),
                  DropdownMenuItem(value: 'experience', child: Text('Experience')),
                  DropdownMenuItem(value: 'problem', child: Text('Problem')),
                  DropdownMenuItem(value: 'solution', child: Text('Solution')),
                  DropdownMenuItem(value: 'general', child: Text('General')),
                ],
                onChanged: (v) => setState(() => _category = v ?? 'general'),
                decoration: const InputDecoration(labelText: 'Category'),
              ),
              const SizedBox(height: 12),
              SwitchListTile(
                value: _isQuestion,
                onChanged: (v) => setState(() => _isQuestion = v),
                title: const Text('Mark as question'),
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _content,
                decoration: const InputDecoration(labelText: 'Content'),
                maxLines: 6,
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Required' : null,
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _submitting ? null : _submit,
                  child: _submitting
                      ? const SizedBox(
                          height: 18,
                          width: 18,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                        )
                      : const Text('Publish'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

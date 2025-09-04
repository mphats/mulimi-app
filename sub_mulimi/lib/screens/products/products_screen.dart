import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_strings.dart';
import '../../core/models/product_model.dart';
import '../../core/services/product_service.dart';
import '../../widgets/empty_state.dart';
import '../../widgets/error_state.dart';
import '../../widgets/shimmer_list.dart';

class ProductsScreen extends StatefulWidget {
  const ProductsScreen({super.key});

  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  final _service = ProductService();
  final _searchController = TextEditingController();
  String? _selectedCategory;
  String? _selectedLocation;
  bool _isLoading = true;
  String? _error;
  List<ProductModel> _products = [];

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _fetch() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });
    final res = await _service.getProducts(
      category: _selectedCategory,
      location: _selectedLocation,
      search: _searchController.text.trim().isEmpty
          ? null
          : _searchController.text.trim(),
    );
    if (!mounted) return;
    setState(() {
      _isLoading = false;
      if (res.isSuccess) {
        _products = res.products;
      } else {
        _error = res.message;
      }
    });
  }

  void _openAddProduct() async {
    await Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => const AddProductScreen()),
    );
    if (mounted) _fetch();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(AppStrings.products),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        automaticallyImplyLeading: false,
        actions: [
          IconButton(onPressed: _openAddProduct, icon: const Icon(Icons.add))
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
              if (_isLoading) const ShimmerList(),
              if (!_isLoading && _error != null)
                ErrorState(title: 'Failed to load', message: _error, onRetry: _fetch),
              if (!_isLoading && _error == null && _products.isEmpty)
                const EmptyState(
                  icon: Icons.storefront_outlined,
                  title: 'No products found',
                  message: 'Try changing filters or add your first product.',
                ),
              if (!_isLoading && _error == null && _products.isNotEmpty)
                _buildList(),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openAddProduct,
        child: const Icon(Icons.add),
      ),
    );
  }
}

class AddProductScreen extends StatefulWidget {
  const AddProductScreen({super.key});

  @override
  State<AddProductScreen> createState() => _AddProductScreenState();
}

class _AddProductScreenState extends State<AddProductScreen> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _category = ValueNotifier<String>('GRAINS');
  final _description = TextEditingController();
  final _quantity = TextEditingController();
  final _unit = ValueNotifier<String>('kg');
  final _price = TextEditingController();
  final _harvestDate = ValueNotifier<DateTime>(DateTime.now());
  final _location = TextEditingController();
  final _phone = TextEditingController();
  bool _submitting = false;
  final _service = ProductService();

  @override
  void dispose() {
    _name.dispose();
    _description.dispose();
    _quantity.dispose();
    _price.dispose();
    _location.dispose();
    _phone.dispose();
    _category.dispose();
    _unit.dispose();
    _harvestDate.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _submitting = true);
    final req = ProductCreateRequest(
      name: _name.text.trim(),
      category: _category.value,
      description: _description.text.trim(),
      quantity: double.parse(_quantity.text.trim()),
      unit: _unit.value,
      pricePerUnit: double.parse(_price.text.trim()),
      harvestDate: _harvestDate.value,
      location: _location.text.trim(),
      contactPhone: _phone.text.trim(),
    );
    final res = await _service.createProduct(req);
    if (!mounted) return;
    setState(() => _submitting = false);
    if (res.isSuccess) {
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Product created')),
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
        title: const Text('Add Product'),
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
                controller: _name,
                decoration: const InputDecoration(labelText: 'Name'),
                validator: (v) => (v == null || v.trim().isEmpty) ? 'Required' : null,
              ),
              const SizedBox(height: 12),
              ValueListenableBuilder<String>(
                valueListenable: _category,
                builder: (_, value, __) => DropdownButtonFormField<String>(
                  value: value,
                  items: const [
                    DropdownMenuItem(value: 'GRAINS', child: Text('Grains')),
                    DropdownMenuItem(value: 'VEGETABLES', child: Text('Vegetables')),
                    DropdownMenuItem(value: 'FRUITS', child: Text('Fruits')),
                    DropdownMenuItem(value: 'LIVESTOCK', child: Text('Livestock')),
                    DropdownMenuItem(value: 'DAIRY', child: Text('Dairy')),
                    DropdownMenuItem(value: 'OTHER', child: Text('Other')),
                  ],
                  onChanged: (v) => _category.value = v ?? 'GRAINS',
                  decoration: const InputDecoration(labelText: 'Category'),
                ),
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _description,
                decoration: const InputDecoration(labelText: 'Description'),
                maxLines: 3,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _quantity,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'Quantity'),
                validator: (v) => (v == null || double.tryParse(v) == null) ? 'Enter a number' : null,
              ),
              const SizedBox(height: 12),
              ValueListenableBuilder<String>(
                valueListenable: _unit,
                builder: (_, value, __) => DropdownButtonFormField<String>(
                  value: value,
                  items: const [
                    DropdownMenuItem(value: 'kg', child: Text('kg')),
                    DropdownMenuItem(value: 'ton', child: Text('ton')),
                    DropdownMenuItem(value: 'bag', child: Text('bag')),
                  ],
                  onChanged: (v) => _unit.value = v ?? 'kg',
                  decoration: const InputDecoration(labelText: 'Unit'),
                ),
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _price,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'Price per unit'),
                validator: (v) => (v == null || double.tryParse(v) == null) ? 'Enter a number' : null,
              ),
              const SizedBox(height: 12),
              ValueListenableBuilder<DateTime>(
                valueListenable: _harvestDate,
                builder: (_, value, __) => InkWell(
                  onTap: () async {
                    final picked = await showDatePicker(
                      context: context,
                      initialDate: value,
                      firstDate: DateTime.now().subtract(const Duration(days: 365)),
                      lastDate: DateTime.now().add(const Duration(days: 365 * 2)),
                    );
                    if (picked != null) _harvestDate.value = picked;
                  },
                  child: InputDecorator(
                    decoration: const InputDecoration(labelText: 'Harvest date'),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('${value.year}-${value.month.toString().padLeft(2,'0')}-${value.day.toString().padLeft(2,'0')}'),
                        const Icon(Icons.calendar_today, size: 18),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _location,
                decoration: const InputDecoration(labelText: 'Location'),
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _phone,
                decoration: const InputDecoration(labelText: 'Contact phone'),
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
                      : const Text('Create product'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

extension on _ProductsScreenState {
  Widget _buildFilters() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextField(
          controller: _searchController,
          decoration: InputDecoration(
            hintText: 'Search products',
            prefixIcon: const Icon(Icons.search),
            suffixIcon: IconButton(
              icon: const Icon(Icons.clear),
              onPressed: () {
                _searchController.clear();
                _fetch();
              },
            ),
          ),
          onSubmitted: (_) => _fetch(),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: DropdownButtonFormField<String>(
                value: _selectedCategory,
                isExpanded: true,
                items: const [
                  DropdownMenuItem(value: null, child: Text('All categories')),
                  DropdownMenuItem(value: 'GRAINS', child: Text('Grains')),
                  DropdownMenuItem(value: 'VEGETABLES', child: Text('Vegetables')),
                  DropdownMenuItem(value: 'FRUITS', child: Text('Fruits')),
                  DropdownMenuItem(value: 'LIVESTOCK', child: Text('Livestock')),
                  DropdownMenuItem(value: 'DAIRY', child: Text('Dairy')),
                  DropdownMenuItem(value: 'OTHER', child: Text('Other')),
                ],
                onChanged: (v) {
                  setState(() => _selectedCategory = v);
                  _fetch();
                },
                decoration: const InputDecoration(
                  labelText: 'Category',
                ),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: TextFormField(
                initialValue: _selectedLocation,
                decoration: const InputDecoration(
                  labelText: 'Location',
                  prefixIcon: Icon(Icons.place_outlined),
                ),
                onFieldSubmitted: (_) => _fetch(),
                onChanged: (v) => _selectedLocation = v,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildList() {
    return ListView.separated(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: _products.length,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, index) {
        final p = _products[index];
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
              child: Text(p.name.isNotEmpty ? p.name[0].toUpperCase() : '?'),
            ),
            title: Text(p.name),
            subtitle: Text('${p.categoryDisplayName} • ${p.formattedPrice}'),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(p.statusText,
                    style: Theme.of(context)
                        .textTheme
                        .labelMedium
                        ?.copyWith(color: AppColors.textSecondary)),
                Text(p.location, style: Theme.of(context).textTheme.labelSmall),
              ],
            ),
          ),
        );
      },
    );
  }
}

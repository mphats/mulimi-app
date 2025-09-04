import 'package:flutter/material.dart';

import '../core/constants/app_colors.dart';

class ShimmerList extends StatelessWidget {
  final int itemCount;
  final double height;

  const ShimmerList({super.key, this.itemCount = 6, this.height = 80});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      itemCount: itemCount,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, index) {
        return Container(
          height: height,
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(12),
          ),
        );
      },
    );
  }
}


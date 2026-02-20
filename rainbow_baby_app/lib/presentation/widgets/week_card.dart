import 'package:flutter/material.dart';
import '../../../data/models/pregnancy.dart';

class WeekCard extends StatelessWidget {
  final Pregnancy pregnancy;
  final VoidCallback onTap;

  const WeekCard({
    super.key,
    required this.pregnancy,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              const Color(0xFFE91E63).withOpacity(0.8),
              const Color(0xFF9C27B0).withOpacity(0.8),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.purple.withOpacity(0.3),
              blurRadius: 12,
              offset: const Offset(0, 6),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    pregnancy.trimester,
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                      fontSize: 14,
                    ),
                  ),
                ),
                const Icon(
                  Icons.favorite,
                  color: Colors.white70,
                  size: 24,
                ),
              ],
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            '${pregnancy.currentWeek}',
                            style: const TextStyle(
                              fontSize: 56,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                              height: 1,
                            ),
                          ),
                          const SizedBox(width: 8),
                          const Padding(
                            padding: EdgeInsets.only(bottom: 12),
                            child: Text(
                              'WEEKS',
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.white70,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '+ ${pregnancy.currentDay} days',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.white.withOpacity(0.8),
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Text(
                      emojiForSize(pregnancy.babySize),
                      style: const TextStyle(fontSize: 40),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.tips_and_updates,
                    color: Colors.white70,
                    size: 20,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Baby is size of a ${pregnancy.babySize}',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.white.withOpacity(0.9),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                const Icon(
                  Icons.calendar_today,
                  color: Colors.white70,
                  size: 16,
                ),
                const SizedBox(width: 8),
                Text(
                  '${pregnancy.daysRemaining} days until due date',
                  style: TextStyle(
                    fontSize: 13,
                    color: Colors.white.withOpacity(0.8),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  String emojiForSize(String size) {
    Map<String, String> emojis = {
      'Poppy Seed': '🌱',
      'Apple Seed': '🍎',
      'Sweet Pea': '🫛',
      'Blueberry': '🫐',
      'Raspberry': '🍇',
      'Strawberry': '🍓',
      'Kumquat': '🍊',
      'Fig': '🌰',
      'Lime': '🍋',
      'Peach': '🍑',
      'Lemon': '🍋',
      'Apple': '🍎',
      'Avocado': '🥑',
      'Turnip': '🥔',
      'Bell Pepper': '🫑',
      'Heirloom Tomato': '🍅',
      'Banana': '🍌',
      'Carrot': '🥕',
      'Spaghetti Squash': '🎃',
      'Mango': '🥭',
      'Ear of Corn': '🌽',
      'Rutabaga': '🧅',
      'Scallion': '🧅',
      'Cauliflower': '🥦',
      'Eggplant': '🍆',
      'Butternut Squash': '🎃',
      'Cabbage': '🥬',
      'Coconut': '🥥',
      'Jicama': '🥔',
      'Pineapple': '🍍',
      'Cantaloupe': '🍈',
      'Honeydew Melon': '🍈',
      'Romaine Lettuce': '🥬',
      'Swiss Chard': '🥬',
      'Leek': '🧅',
      'Watermelon': '🍉',
      'Pumpkin': '🎃',
    };
    return emojis[size] ?? '👶';
  }
}

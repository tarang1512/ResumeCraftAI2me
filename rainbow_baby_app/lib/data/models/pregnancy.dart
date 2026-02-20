class Pregnancy {
  final DateTime lmpDate; // Last Menstrual Period
  final DateTime? dueDate;
  final int currentWeek;
  final int currentDay;
  final String trimester;
  final String babySize;

  Pregnancy({
    required this.lmpDate,
    this.dueDate,
    required this.currentWeek,
    required this.currentDay,
    required this.trimester,
    required this.babySize,
  });

  factory Pregnancy.fromLMP(DateTime lmp) {
    final now = DateTime.now();
    final difference = now.difference(lmp);
    final totalDays = difference.inDays;
    final currentWeek = (totalDays / 7).floor();
    final currentDay = totalDays % 7;
    final dueDate = lmp.add(Duration(days: 280));

    String trimester;
    if (currentWeek < 13) {
      trimester = 'First';
    } else if (currentWeek < 27) {
      trimester = 'Second';
    } else {
      trimester = 'Third';
    }

    String babySize = getBabySize(currentWeek);

    return Pregnancy(
      lmpDate: lmp,
      dueDate: dueDate,
      currentWeek: currentWeek,
      currentDay: currentDay,
      trimester: trimester,
      babySize: babySize,
    );
  }

  static String getBabySize(int week) {
    final sizes = {
      4: 'Poppy Seed',
      5: 'Apple Seed',
      6: 'Sweet Pea',
      7: 'Blueberry',
      8: 'Raspberry',
      9: 'Strawberry',
      10: 'Kumquat',
      11: 'Fig',
      12: 'Lime',
      13: 'Peach',
      14: 'Lemon',
      15: 'Apple',
      16: 'Avocado',
      17: 'Turnip',
      18: 'Bell Pepper',
      19: 'Heirloom Tomato',
      20: 'Banana',
      21: 'Carrot',
      22: 'Spaghetti Squash',
      23: 'Mango',
      24: 'Ear of Corn',
      25: 'Rutabaga',
      26: 'Scallion',
      27: 'Cauliflower',
      28: 'Eggplant',
      29: 'Butternut Squash',
      30: 'Cabbage',
      31: 'Coconut',
      32: 'Jicama',
      33: 'Pineapple',
      34: 'Cantaloupe',
      35: 'Honeydew Melon',
      36: 'Romaine Lettuce',
      37: 'Swiss Chard',
      38: 'Leek',
      39: 'Watermelon',
      40: 'Pumpkin',
    };
    return sizes[week] ?? 'Growing Baby';
  }

  int get daysRemaining {
    return dueDate?.difference(DateTime.now()).inDays ?? 0;
  }

  double get progressPercent {
    return currentWeek / 40.0;
  }
}

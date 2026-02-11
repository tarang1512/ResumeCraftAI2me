class AppConstants {
  // App Info
  static const String appName = 'RainbowBaby';
  static const String appVersion = '1.0.0';
  static const String appTagline = 'Hope after loss';
  
  // Storage Keys
  static const String userProfileKey = 'user_profile';
  static const String pregnancyDataKey = 'pregnancy_data';
  static const String symptomsKey = 'symptoms';
  static const String appointmentsKey = 'appointments';
  static const String settingsKey = 'settings';
  
  // Hive Boxes
  static const String pregnancyBox = 'pregnancy_box';
  static const String symptomBox = 'symptom_box';
  static const String userBox = 'user_box';
  static const String healthBox = 'health_box';
  
  // HealthKit Types
  static const List<String> healthKitTypes = [
    'HEART_RATE',
    'HEART_RATE_VARIABILITY_SDNN',
    'BLOOD_OXYGEN',
    'SLEEP_ASLEEP',
    'BODY_TEMPERATURE',
    'ACTIVE_ENERGY_BURNED',
    'BASAL_ENERGY_BURNED',
  ];
  
  // Pregnancy Constants
  static const int totalWeeks = 40;
  static const int trimester1End = 12;
  static const int trimester2End = 27;
  static const int trimester3End = 40;
  
  // Risk Levels
  static const String riskLevelNormal = 'Normal';
  static const String riskLevelCaution = 'Contact Doctor';
  static const String riskLevelEmergency = 'Emergency';
  
  // Colors (Rainbow Theme)
  static const int rainbowRed = 0xFFFF6B6B;
  static const int rainbowOrange = 0xFFFF9F43;
  static const int rainbowYellow = 0xFFFFD93D;
  static const int rainbowGreen = 0xFF6BCB77;
  static const int rainbowBlue = 0xFF4D96FF;
  static const int rainbowPurple = 0xFF9B59B6;
  
  // Affirmations
  static const List<String> dailyAffirmations = [
    'Your rainbow baby is growing strong.',
    'Every day brings new hope and healing.',
    'Trust your body, trust the process.',
    'You are strong enough for this journey.',
    'Today is a step forward on your rainbow path.',
    'Your love surrounds your baby.',
    'Breathe in peace, exhale worry.',
    'This pregnancy is different, this baby is safe.',
    'You are creating a miracle.',
    'Hope is stronger than fear.',
  ];
}

class PregnancyMilestones {
  static const Map<int, Map<String, dynamic>> weeklyMilestones = {
    1: {
      'title': 'Conception',
      'babySize': 'Poppy Seed',
      'babyLength': '0.0',
      'babyWeight': '0.00',
      'description': 'Your baby\'s journey begins.',
      'momChanges': 'You may not feel different yet, but amazing things are happening.',
      'tips': [
        'Start taking prenatal vitamins',
        'Avoid alcohol and smoking',
        'Stay hydrated',
      ],
    },
    4: {
      'title': 'Implantation Complete',
      'babySize': 'Poppy Seed',
      'babyLength': '0.2',
      'babyWeight': '0.00',
      'description': 'Your baby is now a blastocyst, implanting in the uterus.',
      'momChanges': 'You may notice light spotting or cramping.',
      'tips': [
        'Rest when you need to',
        'Continue prenatal vitamins',
        'Schedule your first prenatal appointment',
      ],
    },
    8: {
      'title': 'Little Heartbeat',
      'babySize': 'Raspberry',
      'babyLength': '1.6',
      'babyWeight': '0.04',
      'description': 'Your baby\'s heart is beating! All major organs are forming.',
      'momChanges': 'Morning sickness and fatigue are common now.',
      'tips': [
        'Eat small, frequent meals',
        'Get plenty of rest',
        'Stay hydrated',
      ],
    },
    12: {
      'title': 'End of First Trimester',
      'babySize': 'Lime',
      'babyLength': '2.1',
      'babyWeight': '0.49',
      'description': 'Risk of miscarriage drops significantly. Your baby can move!',
      'momChanges': 'You may start showing a small bump.',
      'tips': [
        'Consider announcing if you\'re ready',
        'Notify your employer',
        'Research maternity leave options',
      ],
    },
    16: {
      'title': 'Feeling Movement',
      'babySize': 'Avocado',
      'babyLength': '4.6',
      'babyWeight': '3.53',
      'description': 'You might feel those first fluttering movements!',
      'momChanges': 'Your energy may be returning.',
      'tips': [
        'Start feeling for baby movements',
        'Consider prenatal classes',
        'Update your wardrobe',
      ],
    },
    20: {
      'title': 'Halfway There',
      'babySize': 'Banana',
      'babyLength': '6.5',
      'babyWeight': '10.58',
      'description': 'Anatomy scan time! You might find out the gender.',
      'momChanges': 'Your bump is definitely growing now!',
      'tips': [
        'Schedule your anatomy scan',
        'Start a baby registry',
        'Begin nursery planning',
      ],
    },
    24: {
      'title': 'Viability Milestone',
      'babySize': 'Corn',
      'babyLength': '12.0',
      'babyWeight': '1.32',
      'description': 'Your baby has a chance of survival if born now.',
      'momChanges': 'You may experience Braxton Hicks contractions.',
      'tips': [
        'Count baby kicks daily',
        'Prepare for glucose test',
        'Watch for swelling',
      ],
    },
    28: {
      'title': 'Third Trimester Begins',
      'babySize': 'Eggplant',
      'babyLength': '14.8',
      'babyWeight': '2.22',
      'description': 'Your baby can now open and close their eyes!',
      'momChanges': 'You may experience more discomfort and fatigue.',
      'tips': [
        'Pack your hospital bag',
        'Finalize birth plan',
        'Install car seat',
      ],
    },
    32: {
      'title': 'Breathing Practice',
      'babySize': 'Squash',
      'babyLength': '16.7',
      'babyWeight': '3.75',
      'description': 'Your baby is practicing breathing movements!',
      'momChanges': 'You may need to urinate more frequently.',
      'tips': [
        'Practice relaxation techniques',
        'Monitor baby\'s movement',
        'Rest with feet elevated',
      ],
    },
    36: {
      'title': 'Almost Ready',
      'babySize': 'Honeydew',
      'babyLength': '18.7',
      'babyWeight': '5.78',
      'description': 'Your baby is nearly fully developed!',
      'momChanges': 'You may feel more pressure as baby drops.',
      'tips': [
        'Week 36-37: Prepare for arrival',
        'Know signs of labor',
        'Rest and conserve energy',
      ],
    },
    40: {
      'title': 'Due Date',
      'babySize': 'Watermelon',
      'babyLength': '20.2',
      'babyWeight': '7.63',
      'description': 'Your baby is ready to meet the world!',
      'momChanges': 'The wait continues...',
      'tips': [
        'Stay calm and prepared',
        'Enjoy the final moments',
        'Trust your body',
      ],
    },
  };
  
  static Map<String, dynamic>? getMilestoneForWeek(int week) {
    // Find closest milestone week
    final milestoneWeek = PregnancyMilestones.weeklyMilestones.keys
        .where((w) => w <= week)
        .toList()..sort();
    
    if (milestoneWeek.isEmpty) return weeklyMilestones[1];
    return weeklyMilestones[milestoneWeek.last];
  }
}
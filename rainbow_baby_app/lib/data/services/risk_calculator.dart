import '../models/pregnancy.dart';

class RiskAssessment {
  final String level;
  final String message;
  final String recommendation;
  final int score;

  RiskAssessment({
    required this.level,
    required this.message,
    required this.recommendation,
    required this.score,
  });
}

class RiskCalculator {
  static RiskAssessment calculateRisk({
    required List<Map<String, dynamic>> symptoms,
    required Map<String, dynamic> vitals,
    required Pregnancy pregnancy,
    bool hasHistory = false,
  }) {
    int score = 0;
    List<String> highRiskSymptoms = [];
    
    // Symptom scoring
    for (var symptom in symptoms) {
      String name = symptom['name'].toString().toLowerCase();
      double severity = symptom['severity'] ?? 0;
      
      if (severity > 7) {
        score += (severity * 2).toInt();
        highRiskSymptoms.add(name);
      } else if (severity > 4) {
        score += severity.toInt();
      }
      
      // Critical symptom multipliers
      if (name.contains('spotting') && severity > 3) score += 15;
      if (name.contains('cramping') && severity > 6) score += 20;
      if (name.contains('anxiety') && severity > 6) score += 10;
    }
    
    // Vital signs
    final hr = vitals['heartRate'];
    if (hr != null) {
      if (hr > 110 || hr < 50) score += 20;
      else if (hr > 100) score += 10;
    }
    
    final hrv = vitals['hrv'];
    if (hrv != null && hrv < 40) score += 15;
    
    final sleep = vitals['sleepHours'];
    if (sleep != null && sleep < 5) score += 10;
    
    // History of loss
    if (hasHistory && pregnancy.currentWeek < 14) {
      score += 5; // Slightly elevated baseline in first trimester
    }
    
    // Trimester adjustments
    if (pregnancy.trimester == 'First' && score > 20) score += 5;
    
    // Determine risk level
    String level;
    String message;
    String recommendation;
    
    if (score >= 60) {
      level = 'HIGH';
      message = 'Multiple concerning symptoms detected. Immediate medical attention recommended.';
      recommendation = 'Contact your doctor or visit emergency services now.';
    } else if (score >= 30) {
      level = 'MEDIUM';
      message = 'Some symptoms require attention. Monitor closely.';
      recommendation = 'Call your healthcare provider within 24 hours for guidance.';
    } else {
      level = 'LOW';
      message = 'Symptoms appear within normal range.';
      recommendation = 'Continue monitoring. Reach out if symptoms worsen.';
    }
    
    return RiskAssessment(
      level: level,
      message: message,
      recommendation: recommendation,
      score: score,
    );
  }
}

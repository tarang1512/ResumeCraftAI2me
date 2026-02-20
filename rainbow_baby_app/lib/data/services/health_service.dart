import 'package:health/health.dart';
import 'package:permission_handler/permission_handler.dart';

class HealthService {
  final HealthFactory _health = HealthFactory();
  
  static final List<HealthDataType> _types = [
    HealthDataType.HEART_RATE,
    HealthDataType.HEART_RATE_VARIABILITY_SDNN,
    HealthDataType.BLOOD_OXYGEN,
    HealthDataType.SLEEP_ASLEEP,
    HealthDataType.SLEEP_IN_BED,
    HealthDataType.STEPS,
    HealthDataType.BODY_TEMPERATURE,
  ];

  Future<bool> requestPermissions() async {
    // Request iOS HealthKit permissions
    final permissions = _types.map((t) => HealthDataAccess.READ).toList();
    return await _health.requestAuthorization(_types, permissions: permissions);
  }

  Future<Map<String, dynamic>> getLatestVitals() async {
    final now = DateTime.now();
    final yesterday = now.subtract(const Duration(days: 1));
    
    Map<String, dynamic> vitals = {};
    
    try {
      // Heart rate
      final heartRate = await _health.getHealthDataFromTypes(yesterday, now, [HealthDataType.HEART_RATE]);
      if (heartRate.isNotEmpty) {
        vitals['heartRate'] = heartRate.last.value;
        vitals['heartRateTimestamp'] = heartRate.last.dateFrom;
      }
      
      // HRV
      final hrv = await _health.getHealthDataFromTypes(yesterday, now, [HealthDataType.HEART_RATE_VARIABILITY_SDNN]);
      if (hrv.isNotEmpty) {
        vitals['hrv'] = hrv.last.value;
      }
      
      // Sleep
      final sleep = await _health.getHealthDataFromTypes(yesterday, now, [HealthDataType.SLEEP_ASLEEP]);
      if (sleep.isNotEmpty) {
        double totalSleep = 0;
        for (var s in sleep) {
          totalSleep += (s.dateTo.difference(s.dateFrom).inMinutes / 60);
        }
        vitals['sleepHours'] = totalSleep;
      }
      
      // Steps
      final steps = await _health.getTotalStepsInInterval(yesterday, now);
      vitals['steps'] = steps ?? 0;
      
    } catch (e) {
      print('HealthKit error: $e');
    }
    
    return vitals;
  }

  Future<bool> isAvailable() async {
    return await _health.isHealthDataAvailable();
  }
}

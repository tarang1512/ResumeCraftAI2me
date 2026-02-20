import 'package:flutter/material.dart';
import '../../../data/services/health_service.dart';

class VitalsDashboard extends StatefulWidget {
  const VitalsDashboard({super.key});

  @override
  State<VitalsDashboard> createState() => _VitalsDashboardState();
}

class _VitalsDashboardState extends State<VitalsDashboard> {
  final HealthService _healthService = HealthService();
  Map<String, dynamic> _vitals = {};
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadVitals();
  }

  Future<void> _loadVitals() async {
    setState(() => _loading = true);
    
    final hasPermission = await _healthService.requestPermissions();
    if (hasPermission) {
      final vitals = await _healthService.getLatestVitals();
      setState(() {
        _vitals = vitals;
        _loading = false;
      });
    } else {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F5),
      appBar: AppBar(
        title: const Text('Vitals', style: TextStyle(color: Color(0xFFE91E63), fontWeight: FontWeight.bold)),
        elevation: 0,
        backgroundColor: Colors.white,
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadVitals,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                child: Column(
                  children: [
                    const SizedBox(height: 16),
                    _buildVitalCard('Heart Rate', _vitals['heartRate'] ?? '--', 'bpm', Icons.favorite, Colors.red),
                    _buildVitalCard('HRV', _vitals['hrv'] ?? '--', 'ms', Icons.stacked_line_chart, Colors.purple),
                    _buildVitalCard('Sleep', _vitals['sleepHours'] != null ? '${_vitals['sleepHours'].toStringAsFixed(1)}' : '--', 'hrs', Icons.bedtime, Colors.indigo),
                    _buildVitalCard('Steps', _vitals['steps']?.toString() ?? '--', 'steps', Icons.directions_walk, Colors.green),
                    const SizedBox(height: 20),
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFFF8E1),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Row(
                          children: [
                            Icon(Icons.info_outline, color: Color(0xFFFF8F00)),
                            SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                'Enable Apple Health permissions to see your data here.',
                                style: TextStyle(fontSize: 13, color: Color(0xFFFF8F00)),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildVitalCard(String title, String value, String unit, IconData icon, Color color) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 8, offset: const Offset(0, 2)),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
            child: Icon(icon, color: color, size: 28),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: TextStyle(fontSize: 14, color: Colors.grey.shade600)),
                const SizedBox(height: 4),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(value, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                    const SizedBox(width: 6),
                    Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(unit, style: const TextStyle(fontSize: 14, color: Colors.grey)),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

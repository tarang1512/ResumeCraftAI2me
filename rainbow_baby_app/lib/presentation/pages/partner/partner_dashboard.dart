import 'package:flutter/material.dart';

class PartnerDashboard extends StatelessWidget {
  const PartnerDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Partner Mode'),
        backgroundColor: const Color(0xFF9C27B0),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildHeader(),
            _buildTodaySupportCard(),
            _buildWeeklyChecklist(),
            _buildSymptomSummary(),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: const BoxDecoration(
        color: Color(0xFF9C27B0),
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(20),
          bottomRight: Radius.circular(20),
        ),
      ),
      child: const Column(
        children: [
          CircleAvatar(
            radius: 40,
            backgroundColor: Colors.white,
            child: Icon(Icons.favorite, size: 40, color: Color(0xFF9C27B0)),
          ),
          SizedBox(height: 16),
          Text(
            'Support Mode',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Week 8 • Second Trimester starting soon',
            style: TextStyle(color: Colors.white70),
          ),
        ],
      ),
    );
  }

  Widget _buildTodaySupportCard() {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 8)],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.today, color: Color(0xFF9C27B0)),
              SizedBox(width: 8),
              Text('How to Help Today', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 16),
          _buildTipItem('Prepare healthy snacks', '🥗 She may be feeling nauseous today'),
          _buildTipItem('Gentle back rub', '💆 Relieves tension and shows you care'),
          _buildTipItem('Hydration reminder', '💧 Bring water every hour'),
        ],
      ),
    );
  }

  Widget _buildTipItem(String title, String subtitle) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.check_circle, color: Color(0xFF9C27B0), size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
                Text(subtitle, style: TextStyle(color: Colors.grey.shade600, fontSize: 13)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWeeklyChecklist() {
    final items = [
      'Attend prenatal appointment',
      'Help with household chores',
      'Plan nutritious meals',
      'Emotional check-in daily',
    ];

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFFCE4EC),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Weekly Checklist', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          ...items.map((item) => CheckboxListTile(
            title: Text(item),
            value: false,
            onChanged: (_) {},
            controlAffinity: ListTileControlAffinity.leading,
            contentPadding: EdgeInsets.zero,
          )),
        ],
      ),
    );
  }

  Widget _buildSymptomSummary() {
    return Container(
      margin: const EdgeInsets.all(16),
      child: ElevatedButton.icon(
        onPressed: () {},
        icon: const Icon(Icons.visibility),
        label: const Text('View Her Symptom Log'),
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF9C27B0),
          minimumSize: const Size(double.infinity, 50),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
    );
  }
}

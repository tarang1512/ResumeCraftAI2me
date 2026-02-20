import 'package:flutter/material.dart';

class SymptomLogPage extends StatefulWidget {
  const SymptomLogPage({super.key});

  @override
  State<SymptomLogPage> createState() => _SymptomLogPageState();
}

class _SymptomLogPageState extends State<SymptomLogPage> {
  final List<Map<String, dynamic>> symptoms = [
    {'name': 'Nausea', 'icon': '🤢', 'severity': 0.0},
    {'name': 'Fatigue', 'icon': '😴', 'severity': 0.0},
    {'name': 'Cramping', 'icon': '😣', 'severity': 0.0},
    {'name': 'Spotting', 'icon': '🩸', 'severity': 0.0},
    {'name': 'Mood Swings', 'icon': '🎭', 'severity': 0.0},
    {'name': 'Anxiety', 'icon': '😰', 'severity': 0.0},
    {'name': 'Breast Tenderness', 'icon': '🤱', 'severity': 0.0},
    {'name': 'Headache', 'icon': '🤕', 'severity': 0.0},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Log Symptoms'),
        backgroundColor: const Color(0xFFE91E63),
        actions: [
          TextButton(
            onPressed: () {},
            child: const Text('SAVE', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: symptoms.length,
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${symptoms[index]['icon']} ${symptoms[index]['name']}'),
                  Slider(
                    value: symptoms[index]['severity'],
                    max: 10,
                    divisions: 10,
                    label: symptoms[index]['severity'].round().toString(),
                    onChanged: (value) {
                      setState(() {
                        symptoms[index]['severity'] = value;
                      });
                    },
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'presentation/pages/home/home_page.dart';
import 'presentation/pages/symptoms/symptom_log_page.dart';
import 'presentation/pages/vitals/vitals_dashboard.dart';
import 'presentation/pages/partner/partner_dashboard.dart';
import 'presentation/pages/settings/settings_page.dart';
import 'presentation/pages/calendar/calendar_page.dart';
import 'presentation/pages/journal/journal_page.dart';
import 'presentation/pages/community/community_page.dart';
import 'presentation/pages/notifications/notifications_page.dart';

void main() {
  runApp(const RainbowBabyApp());
}

class RainbowBabyApp extends StatelessWidget {
  const RainbowBabyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rainbow Baby',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.pink,
        scaffoldBackgroundColor: const Color(0xFFF5F5F5),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomePage(),
        '/symptoms': (context) => const SymptomLogPage(),
        '/vitals': (context) => const VitalsDashboard(),
        '/partner': (context) => const PartnerDashboard(),
        '/settings': (context) => const SettingsPage(),
        '/calendar': (context) => const CalendarPage(),
        '/journal': (context) => const JournalPage(),
        '/community': (context) => const CommunityPage(),
        '/notifications': (context) => const NotificationsPage(),
      },
    );
  }
}

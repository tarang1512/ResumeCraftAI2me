import 'package:flutter/material.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F5),
      appBar: AppBar(
        title: const Text(
          'Settings',
          style: TextStyle(
            color: Color(0xFFE91E63),
            fontWeight: FontWeight.bold,
          ),
        ),
        elevation: 0,
        backgroundColor: Colors.white,
        iconTheme: const IconThemeData(color: Color(0xFFE91E63)),
      ),
      body: ListView(
        children: [
          _buildSectionHeader('Pregnancy'),
          _buildSettingTile(
            icon: Icons.calendar_today,
            title: 'Due Date',
            subtitle: 'Calculate from last period',
            onTap: () {},
          ),
          _buildSettingTile(
            icon: Icons.person,
            title: 'My Profile',
            subtitle: 'Update your information',
            onTap: () {},
          ),
          _buildSectionHeader('Notifications'),
          _buildSettingTile(
            icon: Icons.notifications,
            title: 'Push Notifications',
            subtitle: 'Daily tips and reminders',
            trailing: Switch(
              value: true,
              onChanged: (value) {},
              activeColor: const Color(0xFFE91E63),
            ),
          ),
          _buildSettingTile(
            icon: Icons.email,
            title: 'Email Updates',
            subtitle: 'Weekly progress reports',
            trailing: Switch(
              value: false,
              onChanged: (value) {},
              activeColor: const Color(0xFFE91E63),
            ),
          ),
          _buildSectionHeader('Preferences'),
          _buildSettingTile(
            icon: Icons.dark_mode,
            title: 'Dark Mode',
            subtitle: 'Easier on the eyes at night',
            trailing: Switch(
              value: false,
              onChanged: (value) {},
              activeColor: const Color(0xFFE91E63),
            ),
          ),
          _buildSettingTile(
            icon: Icons.lock,
            title: 'Privacy',
            subtitle: 'Manage data sharing',
            onTap: () {},
          ),
          _buildSectionHeader('Support'),
          _buildSettingTile(
            icon: Icons.help,
            title: 'Help Center',
            subtitle: 'FAQs and guides',
            onTap: () {},
          ),
          _buildSettingTile(
            icon: Icons.feedback,
            title: 'Send Feedback',
            subtitle: 'We\'d love to hear from you',
            onTap: () {},
          ),
          const SizedBox(height: 20),
          Center(
            child: Text(
              'Version 1.0.0',
              style: TextStyle(
                color: Colors.grey.shade500,
                fontSize: 12,
              ),
            ),
          ),
          const SizedBox(height: 40),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
      child: Text(
        title,
        style: const TextStyle(
          color: Color(0xFFE91E63),
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }

  Widget _buildSettingTile({
    required IconData icon,
    required String title,
    required String subtitle,
    Widget? trailing,
    VoidCallback? onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
        ),
        child: ListTile(
          leading: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: const Color(0xFFE91E63).withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: const Color(0xFFE91E63)),
          ),
          title: Text(title),
          subtitle: Text(
            subtitle,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey.shade600,
            ),
          ),
          trailing: trailing ?? const Icon(Icons.chevron_right, color: Colors.grey),
        ),
      ),
    );
  }
}

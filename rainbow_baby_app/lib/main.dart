import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/theme/app_theme.dart';
import 'core/constants/app_constants.dart';
import 'data/services/health_service.dart';
import 'data/services/database_service.dart';
import 'presentation/blocs/pregnancy/pregnancy_bloc.dart';
import 'presentation/blocs/symptom/symptom_bloc.dart';
import 'presentation/blocs/health/health_bloc.dart';
import 'presentation/blocs/risk/risk_bloc.dart';
import 'presentation/pages/splash/splash_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp();
  
  // Initialize Hive for local storage
  await Hive.initFlutter();
  await DatabaseService().init();
  
  runApp(const RainbowBabyApp());
}

class RainbowBabyApp extends StatelessWidget {
  const RainbowBabyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: const Size(375, 812),
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (context, child) {
        return MultiBlocProvider(
          providers: [
            BlocProvider(create: (_) => PregnancyBloc()),
            BlocProvider(create: (_) => SymptomBloc()),
            BlocProvider(create: (_) => HealthBloc(HealthService())),
            BlocProvider(create: (_) => RiskBloc()),
          ],
          child: MaterialApp(
            title: AppConstants.appName,
            debugShowCheckedModeBanner: false,
            theme: AppTheme.lightTheme,
            darkTheme: AppTheme.darkTheme,
            themeMode: ThemeMode.system,
            home: const SplashPage(),
          ),
        );
      },
    );
  }
}

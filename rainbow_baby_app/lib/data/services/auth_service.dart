import 'dart:async';

class MockUser {
  final String uid;
  final String email;
  final String displayName;
  final bool isAnonymous;

  MockUser({
    required this.uid,
    required this.email,
    this.displayName = '',
    this.isAnonymous = false,
  });
}

class AuthService {
  MockUser? _currentUser;
  final _authStateController = StreamController<MockUser?>.broadcast();

  // Mock implementation for testing
  // Replace with FirebaseAuth when ready
  
  Stream<MockUser?> get authStateChanges => _authStateController.stream;
  
  MockUser? get currentUser => _currentUser;

  Future<MockUser?> signInWithEmailAndPassword(String email, String password) async {
    // Mock sign in
    await Future.delayed(const Duration(seconds: 1));
    _currentUser = MockUser(
      uid: DateTime.now().millisecondsSinceEpoch.toString(),
      email: email,
      displayName: email.split('@').first,
    );
    _authStateController.add(_currentUser);
    return _currentUser;
  }

  Future<MockUser?> signUp(String email, String password, String name) async {
    await Future.delayed(const Duration(seconds: 1));
    _currentUser = MockUser(
      uid: DateTime.now().millisecondsSinceEpoch.toString(),
      email: email,
      displayName: name,
    );
    _authStateController.add(_currentUser);
    return _currentUser;
  }

  Future<MockUser?> signInAnonymously() async {
    await Future.delayed(const Duration(milliseconds: 500));
    _currentUser = MockUser(
      uid: 'anon_${DateTime.now().millisecondsSinceEpoch}',
      email: '',
      displayName: 'Guest',
      isAnonymous: true,
    );
    _authStateController.add(_currentUser);
    return _currentUser;
  }

  Future<void> signOut() async {
    await Future.delayed(const Duration(milliseconds: 300));
    _currentUser = null;
    _authStateController.add(null);
  }

  void dispose() {
    _authStateController.close();
  }
}

# Rainbow Baby Skill - Setup Requirements

## Flutter Installation

This skill assumes Flutter is already installed. To install Flutter:

```bash
# Option 1: Snap (Ubuntu)
sudo snap install flutter --classic

# Option 2: Manual installation
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.24.9-stable.tar.xz
tar xf flutter_linux_3.24.9-stable.tar.xz -C ~/
echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
source ~/.bashrc
flutter doctor
```

## Dart Installation
Flutter includes Dart. No separate installation needed.

## Environment Variables
Ensure Flutter bin is in your PATH:
```bash
export PATH="$PATH:$HOME/flutter/bin"
```

## Verify Installation
```bash
flutter --version
dart --version
```
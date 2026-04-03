[app]
# (str) Title of your application
title = Willow Block Puzzle

# (str) Package name
package.name = willowpuzzle

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's keep it simple)
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,txt

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Тільки Python 3 та Pygame, щоб не було конфліктів
requirements = python3,pygame

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (int) Android API to use
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version
android.build_tools_version = 31.0.0

# (bool) If True, then skip the license agreement prompts
android.accept_sdk_license = True

# (list) The Android architectures to build for
# ВАЖЛИВО: Залишаємо ТІЛЬКИ arm64-v8a, щоб прибрати помилку 'longintrepr.h'
android.archs = arm64-v8a

# (str) The bootstrap to use for p4a
# Обов'язково для ігор на Pygame
p4a.bootstrap = sdl2

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1


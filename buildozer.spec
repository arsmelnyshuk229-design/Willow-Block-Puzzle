[app]
title = Willow Block Puzzle
package.name = willowpuzzle
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,txt
version = 0.1

# Вимоги саме для твого нового Pygame коду
requirements = python3,pygame,pillow

orientation = portrait

# Android specific
fullscreen = 1
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
android.ndk = 25b
android.accept_sdk_license = True

# Вмикаємо обидві архітектури: для нових (arm64) і старих (v7a) телефонів
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.debug_artifact = apk

# Важливо для Pygame
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1

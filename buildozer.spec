[app]
title = Willow Block Puzzle
package.name = willowpuzzle
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,txt
version = 0.1

# ВАЖЛИВО: для Pygame потрібен спеціальний набір
requirements = python3,pygame

orientation = portrait

# Android specific
fullscreen = 1
android.api = 31
# Знижуємо до 31 — це найбільш стабільна версія для Pygame на GitHub!
android.minapi = 21
android.build_tools_version = 31.0.0
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

# ЦЕ ГОЛОВНЕ ДЛЯ PYGAME:
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1

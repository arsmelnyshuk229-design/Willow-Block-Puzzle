[app]
title = Willow Block Puzzle
package.name = willowpuzzle
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3
version = 0.1
requirements = python3,kivy,kivymd==1.1.1,pillow
orientation = portrait

# Android specific
fullscreen = 1
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
android.debug_artifact = apk

# Python for android (p4a) specific
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

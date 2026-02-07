[app]
title = Gematria
package.name = gematria
package.domain = org.luizzepeda

source.dir = .
source.include_exts = py

version = 0.1

requirements = python3==3.10,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 26
android.build_tools_version = 33.0.2
android.ndk = 25b
requirements = python3,kivy

# NO fijar ndk a menos que sea necesario
# android.ndk = r25c

[buildozer]
log_level = 2
warn_on_root = 1

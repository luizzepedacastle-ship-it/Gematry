[app]
title = Gematría
package.name = gematria
package.domain = org.luiz

source.dir = .
source.include_exts = py

version = 0.1

# 👇 AQUÍ ESTÁ LA CLAVE
requirements = python3,kivy,cython

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 26
android.build_tools_version = 33.0.2
android.ndk = 25b

android.permissions = INTERNET

log_level = 2
warn_on_root = 1

#!/usr/bin/env python3
import sys
import importlib

print("=" * 50)
print("Vérification de l'Installation - Stark Log")
print("=" * 50)

modules = [
    "customtkinter",
    "psutil",
    "PIL",
    "supabase",
    "matplotlib",
    "numpy",
    "requests",
    "dotenv",
]

print("\nVérification des dépendances Python:\n")

missing = []
for module in modules:
    try:
        importlib.import_module(module)
        print(f"✓ {module}")
    except ImportError:
        print(f"✗ {module} - MANQUANT")
        missing.append(module)

print("\nVérification des modules locaux:\n")

local_modules = [
    "config.settings",
    "config.theme",
    "services.supabase_client",
    "services.system_monitor",
    "services.auth_service",
    "services.chat_service",
    "ui.app",
]

for module in local_modules:
    try:
        importlib.import_module(module)
        print(f"✓ {module}")
    except ImportError as e:
        print(f"✗ {module} - {e}")
        missing.append(module)

print("\n" + "=" * 50)

if missing:
    print(f"\n⚠️  {len(missing)} dépendances manquantes!")
    print("\nInstallez-les avec:")
    print(f"pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("\n✅ Toutes les dépendances sont installées!")
    print("\nVous pouvez maintenant lancer l'application avec:")
    print("python3 main.py")
    sys.exit(0)

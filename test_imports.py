#!/usr/bin/env python3

print("Testing Stark Log imports...")
print("-" * 50)

try:
    print("✓ Importing main modules...")
    from main import StarkLogApp
    print("  ✓ main module OK")

    print("\n✓ Importing config modules...")
    from config.settings import settings
    from config.theme import COLORS, FONTS
    from config.constants import APP_NAME, APP_VERSION
    print("  ✓ config modules OK")

    print("\n✓ Importing services...")
    from services.system_monitor import SystemMonitor
    from services.auth_service import AuthService
    from services.chat_service import ChatService
    from services.supabase_client import get_supabase
    print("  ✓ services OK")

    print("\n✓ Importing UI modules...")
    from ui.app import StarkLogApp
    from ui.frames.dashboard import DashboardFrame
    from ui.frames.storage import StorageFrame
    from ui.frames.chat import ChatFrame
    from ui.frames.settings import SettingsFrame
    from ui.frames.auth import AuthFrame
    print("  ✓ frames OK")

    from ui.widgets.ram_monitor import RAMMonitor
    from ui.widgets.cleanup_popup import CleanupPopup
    from ui.widgets.dns_popup import DNSPopup
    from ui.widgets.process_list import ProcessListPopup
    print("  ✓ widgets OK")

    print("\n" + "=" * 50)
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("=" * 50)
    print(f"\nStark Log v{APP_VERSION}")
    print("Ready to run: python3 main.py")

except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    print("\nMake sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    exit(1)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    exit(1)

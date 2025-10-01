#!/usr/bin/env python3
"""
Gmail Brute Force Tool Launcher
Quick launcher for the advanced brute force tool
"""

import sys
import os
from pathlib import Path

def main():
    print("🚀 Gmail Brute Force Tool v2.0 Launcher")
    print("=" * 40)
    
    # Check if required files exist
    required_files = ["BruteForce3.py", "configs/config.ini"]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return
    
    print("✅ All required files found")
    print()
    
    # Show menu
    print("Available tools:")
    print("1. 🎯 Advanced Brute Forcer (BruteForce3.py)")
    print("2. 🌐 Proxy Manager (proxy_manager.py)")
    print("3. 📝 Wordlist Generator (wordlist_generator.py)")
    print("4. 🔍 Check Requirements")
    print("5. 📊 View Logs")
    print("6. ❌ Exit")
    
    choice = input("\nSelect tool (1-6): ").strip()
    
    if choice == "1":
        os.system("python BruteForce3.py")
    elif choice == "2":
        os.system("python proxy_manager.py")
    elif choice == "3":
        os.system("python wordlist_generator.py")
    elif choice == "4":
        check_requirements()
    elif choice == "5":
        view_logs()
    elif choice == "6":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import requests
        import socks
        import fake_useragent
        import colorama
        print("✅ All requirements are installed!")
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Run: pip install -r requirements.txt")

def view_logs():
    """View recent logs"""
    log_file = Path("logs/brute_force.log")
    if log_file.exists():
        print("📋 Recent log entries:")
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-10:]:  # Show last 10 lines
                print(line.strip())
    else:
        print("📋 No log file found")

if __name__ == "__main__":
    main()

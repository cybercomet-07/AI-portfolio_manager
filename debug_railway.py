#!/usr/bin/env python3
"""
DEBUG RAILWAY - Simple script to see what's actually running
"""

import os
import time
from datetime import datetime

print("🔍 DEBUG RAILWAY - WHAT'S ACTUALLY RUNNING?")
print("=" * 50)
print(f"⏰ Time: {datetime.now()}")
print(f"📁 Directory: {os.getcwd()}")
print(f"📋 Files: {os.listdir('.')}")

# Check if this is the new script
print("\n✅ THIS IS THE NEW DEBUG SCRIPT!")
print("🚀 If you see this, Railway is running the new code!")

# Check environment
print(f"\n🔐 ALPACA_API_KEY: {'SET' if os.getenv('ALPACA_API_KEY') else 'NOT SET'}")
print(f"🔐 GEMINI_API_KEY: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")

# Keep running
print("\n⏳ Keeping alive...")
for i in range(60):
    print(f"⏰ Still running: {i+1}/60 seconds")
    time.sleep(1)

print("✅ Debug complete!")

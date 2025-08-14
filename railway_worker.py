#!/usr/bin/env python3
"""
RAILWAY WORKER - Unique script to force Railway to run new code
"""

import os
import time
from datetime import datetime

print("🚂 RAILWAY WORKER - NEW CODE IS RUNNING!")
print("=" * 50)
print(f"⏰ Time: {datetime.now()}")
print(f"📁 Directory: {os.getcwd()}")
print(f"📋 Files: {os.listdir('.')}")

print("\n✅ THIS IS THE NEW RAILWAY WORKER SCRIPT!")
print("🚀 Railway is finally running the new code!")

# Check environment
print(f"\n🔐 ALPACA_API_KEY: {'SET' if os.getenv('ALPACA_API_KEY') else 'NOT SET'}")
print(f"🔐 GEMINI_API_KEY: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")

# Keep running
print("\n⏳ Railway worker is alive and running...")
for i in range(60):
    print(f"⏰ Railway worker: {i+1}/60 seconds")
    time.sleep(1)

print("✅ Railway worker complete!")

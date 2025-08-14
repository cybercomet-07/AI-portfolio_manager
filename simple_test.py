#!/usr/bin/env python3
"""
SIMPLE TEST - Force Railway to run new code
"""

print("🎯 SIMPLE TEST - NEW CODE IS RUNNING!")
print("=" * 40)
print("✅ If you see this, Railway deployed the new code!")
print("🚀 This is NOT the old 'Waiting for market to open...' code!")

import os
print(f"📁 Current directory: {os.getcwd()}")
print(f"📋 Files here: {os.listdir('.')}")

import time
for i in range(30):
    print(f"⏰ Test running: {i+1}/30 seconds")
    time.sleep(1)

print("✅ Simple test complete!")

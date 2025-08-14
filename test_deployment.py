#!/usr/bin/env python3
"""
Test Deployment Script - Verify what's actually running
"""

import os
import time
from datetime import datetime

def test_deployment():
    """Test what's actually running on Railway"""
    print("🧪 TESTING DEPLOYMENT - VERIFYING WHAT'S RUNNING")
    print("=" * 60)
    print(f"⏰ Current time: {datetime.now()}")
    print(f"🔧 Python version: {os.sys.version}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📋 Files in directory: {os.listdir('.')}")
    
    # Test environment variables
    print("\n🔐 Environment Variables:")
    env_vars = ["ALPACA_API_KEY", "GEMINI_API_KEY", "TWILIO_ACCOUNT_SID"]
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * len(value)} (set)")
        else:
            print(f"❌ {var}: NOT SET")
    
    # Test imports
    print("\n📦 Testing imports:")
    try:
        from dotenv import load_dotenv
        print("✅ dotenv imported")
    except Exception as e:
        print(f"❌ dotenv import failed: {e}")
    
    try:
        from ai_trading_bot import AITradingBot
        print("✅ AITradingBot imported")
    except Exception as e:
        print(f"❌ AITradingBot import failed: {e}")
    
    # Test bot initialization
    print("\n🤖 Testing bot initialization:")
    try:
        bot = AITradingBot()
        print("✅ Bot initialized successfully")
        print(f"📈 Tickers: {bot.tickers}")
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
    
    print("\n🎯 DEPLOYMENT TEST COMPLETE")
    print("=" * 60)
    
    # Keep running to see if Railway kills it
    print("⏳ Keeping alive for 5 minutes to test...")
    for i in range(300):
        print(f"⏰ Still alive: {i+1}/300 seconds")
        time.sleep(1)

if __name__ == "__main__":
    test_deployment()

#!/usr/bin/env python3
"""
Test Enhanced Bot - Test all new features
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_enhanced_bot():
    """Test all enhanced features"""
    print("🧪 TESTING ENHANCED AI PORTFOLIO MANAGER")
    print("=" * 50)
    
    # Test environment variables
    print("\n🔐 Checking Environment Variables:")
    
    # Required variables
    required_vars = {
        "ALPACA_API_KEY": "Alpaca API Key",
        "ALPACA_SECRET_KEY": "Alpaca Secret Key", 
        "GEMINI_API_KEY": "Gemini API Key",
        "TWILIO_ACCOUNT_SID": "Twilio Account SID",
        "TWILIO_AUTH_TOKEN": "Twilio Auth Token",
        "TELEGRAM_CHAT_ID": "Telegram Chat ID"
    }
    
    all_good = True
    for var, name in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"✅ {name}: SET")
        else:
            print(f"❌ {name}: NOT SET")
            all_good = False
    
    # Optional variables
    print("\n📧 Optional Email Configuration:")
    email_vars = {
        "EMAIL_ADDRESS": "Email Address",
        "EMAIL_PASSWORD": "Email Password",
        "TO_EMAIL_ADDRESS": "To Email Address"
    }
    
    email_configured = True
    for var, name in email_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"✅ {name}: SET")
        else:
            print(f"⚠️ {name}: NOT SET (Email reports will be skipped)")
            email_configured = False
    
    if not all_good:
        print("\n❌ Missing required environment variables!")
        print("💡 Please update your .env file with the required API keys.")
        return False
    
    print(f"\n✅ All required variables are set!")
    print(f"📧 Email configured: {'Yes' if email_configured else 'No'}")
    
    # Test imports
    print("\n📦 Testing Imports:")
    try:
        from ai_trading_bot import AITradingBot
        print("✅ AITradingBot imported")
    except Exception as e:
        print(f"❌ AITradingBot import failed: {e}")
        return False
    
    try:
        from telegram_notifier import TelegramNotifier
        print("✅ TelegramNotifier imported")
    except Exception as e:
        print(f"❌ TelegramNotifier import failed: {e}")
        return False
    
    try:
        from email_reporter import EmailReporter
        print("✅ EmailReporter imported")
    except Exception as e:
        print(f"❌ EmailReporter import failed: {e}")
        return False
    
    # Test bot initialization
    print("\n🤖 Testing Bot Initialization:")
    try:
        bot = AITradingBot()
        print("✅ Bot initialized successfully")
        print(f"📈 Monitoring: {', '.join(bot.tickers)}")
        print(f"📱 Telegram Chat ID: {bot.telegram.chat_id}")
        print(f"📧 Email configured: {'Yes' if bot.email_reporter.email else 'No'}")
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False
    
    # Test Telegram
    print("\n📱 Testing Telegram:")
    try:
        test_message = "🧪 Testing enhanced AI Portfolio Manager - Telegram integration working!"
        success = bot.telegram.send_message(test_message)
        if success:
            print("✅ Telegram test message sent successfully!")
        else:
            print("⚠️ Telegram test failed (check chat ID)")
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
    
    # Test WhatsApp
    print("\n📲 Testing WhatsApp:")
    try:
        test_message = "🧪 Testing enhanced AI Portfolio Manager - WhatsApp integration working!"
        bot.send_whatsapp_message(test_message)
        print("✅ WhatsApp test message sent!")
    except Exception as e:
        print(f"❌ WhatsApp test failed: {e}")
    
    print("\n🎯 ENHANCED BOT TEST COMPLETE!")
    print("=" * 50)
    print("✅ Your enhanced AI Portfolio Manager is ready!")
    print("📱 You'll receive notifications via WhatsApp and Telegram")
    print("📧 Email reports will work once you add the Gmail app password")
    
    return True

if __name__ == "__main__":
    test_enhanced_bot()

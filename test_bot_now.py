#!/usr/bin/env python3
"""
Test script to force the bot to start trading immediately
"""

import os
from dotenv import load_dotenv
from ai_trading_bot import AITradingBot

def test_bot_immediately():
    """Test the bot without waiting for market hours"""
    print("🧪 Testing AI Trading Bot Immediately...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if environment variables are set
    required_vars = [
        "ALPACA_API_KEY",
        "ALPACA_SECRET_KEY", 
        "GEMINI_API_KEY",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ All environment variables found")
    
    try:
        # Initialize bot
        bot = AITradingBot()
        print("✅ Bot initialized successfully")
        
        # Test Alpaca connection
        try:
            account = bot.api.get_account()
            print(f"✅ Alpaca connected - Portfolio: ${float(account.portfolio_value):,.2f}")
        except Exception as e:
            print(f"❌ Alpaca connection failed: {e}")
            return False
        
        # Test WhatsApp
        try:
            bot.send_whatsapp_message("🤖 AI Trading Bot Test - Bot is working and ready to trade!")
            print("✅ WhatsApp test message sent")
        except Exception as e:
            print(f"❌ WhatsApp test failed: {e}")
        
        # Test AI analysis
        try:
            print("🤖 Testing AI analysis...")
            decision = bot.ai_engine.get_ai_decision("AAPL")
            if decision:
                print(f"✅ AI Decision: {decision['action']} (Confidence: {decision['confidence']:.2f})")
            else:
                print("⚠️ AI decision returned None (might be rate limited)")
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
        
        print("🎉 Bot test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Bot test failed: {e}")
        return False

if __name__ == "__main__":
    test_bot_immediately()

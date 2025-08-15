#!/usr/bin/env python3
"""
Test Notifications - Verify notification fixes
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_notification_setup():
    """Test notification setup and credentials"""
    print("🧪 TESTING NOTIFICATION SETUP")
    print("=" * 50)
    
    # Check Telegram
    print("\n📱 Telegram Configuration:")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if telegram_chat_id:
        print(f"✅ Chat ID: {telegram_chat_id}")
    else:
        print("❌ Chat ID: NOT SET")
    
    # Check WhatsApp/Twilio
    print("\n📲 WhatsApp/Twilio Configuration:")
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    to_whatsapp = os.getenv("TO_WHATSAPP_NUMBER")
    
    if twilio_sid:
        print(f"✅ Account SID: {twilio_sid[:10]}...")
    else:
        print("❌ Account SID: NOT SET")
    
    if twilio_token:
        print(f"✅ Auth Token: {twilio_token[:10]}...")
    else:
        print("❌ Auth Token: NOT SET")
    
    if to_whatsapp:
        print(f"✅ To Number: {to_whatsapp}")
    else:
        print("❌ To Number: NOT SET")
    
    # Test bot import
    print("\n🤖 Testing Bot Import:")
    try:
        from ai_trading_bot import AITradingBot
        print("✅ AITradingBot imported successfully")
        
        # Test bot initialization
        bot = AITradingBot()
        print("✅ Bot initialized successfully")
        
        # Test notification methods
        print("\n📱 Testing Notification Methods:")
        
        # Test WhatsApp
        test_msg = "🧪 Test notification from enhanced bot"
        whatsapp_result = bot.send_whatsapp_message(test_msg)
        print(f"   WhatsApp: {'✅ Success' if whatsapp_result else '❌ Failed'}")
        
        # Test Telegram
        telegram_result = bot.send_telegram_message(test_msg)
        print(f"   Telegram: {'✅ Success' if telegram_result else '❌ Failed'}")
        
    except Exception as e:
        print(f"❌ Bot test failed: {e}")
        return False
    
    print("\n🎯 NOTIFICATION TEST COMPLETE!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_notification_setup()

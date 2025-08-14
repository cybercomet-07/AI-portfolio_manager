#!/usr/bin/env python3
"""
Force Start Script - Bypass all market hours checks
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def force_start():
    """Force start the bot without any market hours checks"""
    print("🚀 FORCE STARTING AI BOT - NO MARKET HOURS CHECK")
    print("=" * 60)
    
    try:
        from ai_trading_bot import AITradingBot
        
        # Initialize bot
        bot = AITradingBot()
        print("✅ Bot initialized")
        
        # Send immediate test message
        try:
            bot.send_whatsapp_message("🚀 FORCE START: AI Bot is running 24/7!")
            print("✅ Force start message sent")
        except Exception as e:
            print(f"⚠️ WhatsApp failed: {e}")
        
        # Run AI analysis immediately
        print("🔍 Running AI analysis cycle...")
        bot.run_ai_analysis_cycle()
        
        # Start continuous loop
        print("🔄 Starting 24/7 continuous loop...")
        cycle_count = 0
        
        while True:
            cycle_count += 1
            print(f"\n🔄 Cycle #{cycle_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            try:
                bot.run_ai_analysis_cycle()
                print(f"✅ Cycle #{cycle_count} completed")
            except Exception as e:
                print(f"❌ Cycle #{cycle_count} failed: {e}")
            
            print("⏸ Sleeping 30 minutes...")
            time.sleep(1800)  # 30 minutes
            
    except Exception as e:
        print(f"❌ Force start failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = force_start()
    exit(0 if success else 1)

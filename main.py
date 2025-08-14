#!/usr/bin/env python3
"""
AI Portfolio Manager - Main Entry Point
A simple AI-powered paper trading bot using Google Gemini AI
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the AI Portfolio Manager"""
    print("🤖 AI Portfolio Manager")
    print("=" * 50)
    
    # Check if required environment variables are set
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
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please set up your .env file with the required API keys.")
        print("   Copy env_example.txt to .env and fill in your credentials.")
        return False
    
    print("✅ Environment variables loaded")
    
    # Import and run the main bot
    try:
        from ai_trading_bot import AITradingBot
        print("✅ AI Trading Bot imported")
        
        # Initialize and run the bot
        bot = AITradingBot()
        print("🚀 Starting AI Portfolio Manager...")
        bot.run_bot()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

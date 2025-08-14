#!/usr/bin/env python3
"""
Test script for AI Trading Bot
Run this to verify all components work before starting the main bot
"""

import sys
import time
import os
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported")
    except ImportError as e:
        print(f"❌ google.generativeai import failed: {e}")
        return False
    
    try:
        import yfinance as yf
        print("✅ yfinance imported")
    except ImportError as e:
        print(f"❌ yfinance import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import ta
        print("✅ ta (technical analysis) imported")
    except ImportError as e:
        print(f"❌ ta import failed: {e}")
        return False
    
    try:
        from alpaca_trade_api.rest import REST
        print("✅ alpaca-trade-api imported")
    except ImportError as e:
        print(f"❌ alpaca-trade-api import failed: {e}")
        return False
    
    try:
        from twilio.rest import Client
        print("✅ twilio imported")
    except ImportError as e:
        print(f"❌ twilio import failed: {e}")
        return False
    
    return True

def test_ai_engine():
    """Test AI Trading Engine"""
    print("\n🤖 Testing AI Trading Engine...")
    
    try:
        from ai_trading_engine import AITradingEngine
        
        # Initialize with your API key
        engine = AITradingEngine(os.getenv("GEMINI_API_KEY", "your_gemini_api_key"))
        print("✅ AI Trading Engine initialized")
        
        # Test technical indicators
        indicators = engine.get_technical_indicators("AAPL")
        if indicators:
            print(f"✅ Technical indicators for AAPL: RSI={indicators['rsi']:.2f}, MACD={indicators['macd']:.4f}")
        else:
            print("❌ Failed to get technical indicators")
            return False
        
        # Test market context
        context = engine.get_market_context("AAPL")
        if context:
            print(f"✅ Market context for AAPL: Sector={context.get('sector', 'Unknown')}")
        else:
            print("❌ Failed to get market context")
            return False
        
        # Test AI decision (this will make an API call)
        print("🤖 Getting AI decision for AAPL (this may take a moment)...")
        decision = engine.get_ai_decision("AAPL")
        if decision:
            print(f"✅ AI Decision: {decision['action']} (Confidence: {decision['confidence']:.2f})")
            print(f"   Reasoning: {decision['reasoning'][:100]}...")
        else:
            print("❌ Failed to get AI decision")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ AI Engine test failed: {e}")
        return False

def test_alpaca_connection():
    """Test Alpaca API connection"""
    print("\n📈 Testing Alpaca API connection...")
    
    try:
        from alpaca_trade_api.rest import REST
        
        # Your Alpaca credentials
        API_KEY = "PKFAV4L15F9NWJBY98VO"
        API_SECRET = "0IOF9cXkck2c0IEps1NbWBjZDqKcOLxaYVacfESY"
        BASE_URL = 'https://paper-api.alpaca.markets'
        
        api = REST(API_KEY, API_SECRET, BASE_URL)
        
        # Test account info
        account = api.get_account()
        print(f"✅ Alpaca connected - Account: {account.id}")
        print(f"   Portfolio Value: ${float(account.portfolio_value):,.2f}")
        print(f"   Cash: ${float(account.cash):,.2f}")
        
        # Test market clock
        clock = api.get_clock()
        print(f"   Market Status: {'Open' if clock.is_open else 'Closed'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Alpaca connection failed: {e}")
        return False

def test_twilio_connection():
    """Test Twilio WhatsApp connection"""
    print("\n📲 Testing Twilio WhatsApp connection...")
    
    try:
        from twilio.rest import Client
        
        # Your Twilio credentials
        TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_account_sid")
        TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_auth_token")
        FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER", "whatsapp:+14155238886")
        TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER", "whatsapp:+your_phone_number")
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Send test message
        message = client.messages.create(
            body=f"🤖 AI Trading Bot Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            from_=FROM_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        
        print(f"✅ Twilio test message sent - SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Twilio connection failed: {e}")
        return False

def test_portfolio_tracker():
    """Test Portfolio Tracker"""
    print("\n📊 Testing Portfolio Tracker...")
    
    try:
        from alpaca_trade_api.rest import REST
        from portfolio_tracker import PortfolioTracker
        
        # Initialize Alpaca API
        API_KEY = "PKFAV4L15F9NWJBY98VO"
        API_SECRET = "0IOF9cXkck2c0IEps1NbWBjZDqKcOLxaYVacfESY"
        BASE_URL = 'https://paper-api.alpaca.markets'
        api = REST(API_KEY, API_SECRET, BASE_URL)
        
        # Initialize Portfolio Tracker
        tracker = PortfolioTracker(api)
        print("✅ Portfolio Tracker initialized")
        
        # Test portfolio data
        portfolio = tracker.get_current_portfolio()
        if portfolio:
            print(f"✅ Portfolio data retrieved - Value: ${portfolio['total_value']:,.2f}")
            print(f"   Positions: {portfolio['position_count']}")
        else:
            print("❌ Failed to get portfolio data")
            return False
        
        # Test portfolio metrics
        metrics = tracker.calculate_portfolio_metrics(portfolio)
        if metrics:
            print(f"✅ Portfolio metrics calculated - Return: {metrics['total_return_pct']:.2f}%")
        else:
            print("❌ Failed to calculate portfolio metrics")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio Tracker test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Trading Bot Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("AI Engine Test", test_ai_engine),
        ("Alpaca Connection Test", test_alpaca_connection),
        ("Twilio Connection Test", test_twilio_connection),
        ("Portfolio Tracker Test", test_portfolio_tracker)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your AI trading bot is ready to run.")
        print("🚀 Run 'python ai_trading_bot.py' to start the bot.")
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the bot.")
        print("💡 Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

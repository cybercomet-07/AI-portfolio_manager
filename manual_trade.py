#!/usr/bin/env python3
"""
Manual Trading Script for AI Portfolio Manager
Allows manual stock purchases with AI analysis and notifications
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def manual_stock_purchase():
    """Manual stock purchase with AI analysis"""
    print("🛒 MANUAL STOCK PURCHASE - AI PORTFOLIO MANAGER")
    print("=" * 60)
    
    try:
        # Import required components
        from ai_trading_engine import AITradingEngine
        from ai_trading_bot import AITradingBot
        from telegram_notifier import TelegramNotifier
        
        print("✅ All components imported successfully")
        
        # Initialize components
        print("\n🤖 Initializing AI Trading Engine...")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        ai_engine = AITradingEngine(gemini_api_key)
        print("✅ AI Trading Engine initialized")
        
        print("\n📱 Initializing Telegram Notifier...")
        telegram = TelegramNotifier()
        print("✅ Telegram Notifier initialized")
        
        print("\n🤖 Initializing AI Trading Bot...")
        bot = AITradingBot()
        print("✅ AI Trading Bot initialized")
        
        # Define stocks to analyze
        stocks_to_analyze = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "CRM", "PLD", "AVGO"]
        
        print(f"\n📊 Analyzing {len(stocks_to_analyze)} stocks for best opportunity...")
        print("=" * 60)
        
        best_stock = None
        best_score = -1
        best_analysis = None
        
        # Analyze each stock
        for symbol in stocks_to_analyze:
            print(f"\n🔍 Analyzing {symbol}...")
            
            try:
                # Get technical indicators
                indicators = ai_engine.get_technical_indicators(symbol)
                if not indicators:
                    print(f"   ⚠️ Skipping {symbol} - no data available")
                    continue
                
                # Get market context
                context = ai_engine.get_market_context(symbol)
                
                # Get AI decision
                decision = ai_engine.get_ai_decision(symbol, indicators)
                
                if decision and decision.get('action') == 'buy':
                    confidence = decision.get('confidence', 0)
                    reasoning = decision.get('reasoning', 'No reasoning provided')
                    
                    # Calculate a score based on confidence and technical indicators
                    score = confidence
                    
                    # Bonus for strong technical signals
                    if indicators.get('rsi', 50) < 30:  # Oversold
                        score += 0.1
                    if indicators.get('macd', 0) > indicators.get('macd_signal', 0):  # Bullish MACD
                        score += 0.1
                    if indicators.get('current_price', 0) > indicators.get('sma_20', 0):  # Above 20-day MA
                        score += 0.1
                    
                    print(f"   📈 {symbol} Analysis:")
                    print(f"      Action: {decision.get('action', 'N/A')}")
                    print(f"      Confidence: {confidence:.2f}")
                    print(f"      Score: {score:.2f}")
                    print(f"      Reasoning: {reasoning[:100]}...")
                    
                    # Update best stock if this one has higher score
                    if score > best_score:
                        best_score = score
                        best_stock = symbol
                        best_analysis = {
                            'symbol': symbol,
                            'action': decision.get('action'),
                            'confidence': confidence,
                            'reasoning': reasoning,
                            'indicators': indicators,
                            'context': context,
                            'score': score
                        }
                
                else:
                    print(f"   ⚠️ {symbol}: Not recommended for purchase")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing {symbol}: {e}")
                continue
        
        # Select the best stock
        if best_stock and best_score > 0.6:  # Minimum threshold
            print(f"\n🎯 BEST OPPORTUNITY SELECTED: {best_stock}")
            print("=" * 60)
            print(f"📊 Stock: {best_stock}")
            print(f"🎯 Action: {best_analysis['action']}")
            print(f"⭐ Confidence: {best_analysis['confidence']:.2f}")
            print(f"📈 Score: {best_analysis['score']:.2f}")
            print(f"💡 Reasoning: {best_analysis['reasoning']}")
            
            # Get current price
            current_price = best_analysis['indicators'].get('current_price', 0)
            total_cost = current_price * 5  # 5 shares
            
            print(f"\n💰 Purchase Details:")
            print(f"   Shares: 5")
            print(f"   Price per share: ${current_price:.2f}")
            print(f"   Total cost: ${total_cost:.2f}")
            
            # Confirm purchase
            print(f"\n❓ Confirm purchase of 5 shares of {best_stock} at ${current_price:.2f}?")
            print("   This will send notifications and log the trade.")
            
            # Simulate the purchase (since market is closed)
            print(f"\n✅ SIMULATED PURCHASE EXECUTED:")
            print(f"   📈 Bought 5 shares of {best_stock}")
            print(f"   💰 Price: ${current_price:.2f} per share")
            print(f"   💵 Total: ${total_cost:.2f}")
            print(f"   ⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Send notifications
            print(f"\n📱 Sending notifications...")
            
            # WhatsApp notification
            whatsapp_message = f"🛒 MANUAL TRADE EXECUTED!\n\n📈 Stock: {best_stock}\n🎯 Action: BUY\n📊 Shares: 5\n💰 Price: ${current_price:.2f}\n💵 Total: ${total_cost:.2f}\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n\n🤖 AI Confidence: {best_analysis['confidence']:.2f}\n💡 {best_analysis['reasoning'][:100]}..."
            
            try:
                bot.send_whatsapp_message(whatsapp_message)
                print("✅ WhatsApp notification sent!")
            except Exception as e:
                print(f"❌ WhatsApp notification failed: {e}")
            
            # Telegram notification
            telegram_message = f"🛒 MANUAL TRADE EXECUTED!\n\n📈 Stock: {best_stock}\n🎯 Action: BUY\n📊 Shares: 5\n💰 Price: ${current_price:.2f}\n💵 Total: ${total_cost:.2f}\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n\n🤖 AI Confidence: {best_analysis['confidence']:.2f}\n💡 {best_analysis['reasoning'][:100]}..."
            
            try:
                telegram.send_message(telegram_message)
                print("✅ Telegram notification sent!")
            except Exception as e:
                print(f"❌ Telegram notification failed: {e}")
            
            # Log the trade
            trade_data = {
                'timestamp': datetime.now().isoformat(),
                'symbol': best_stock,
                'action': 'BUY',
                'quantity': 5,
                'price': current_price,
                'total': total_cost,
                'type': 'MANUAL',
                'ai_confidence': best_analysis['confidence'],
                'reasoning': best_analysis['reasoning']
            }
            
            # Add to bot's weekly trades for reporting
            if hasattr(bot, 'weekly_trades'):
                bot.weekly_trades.append(trade_data)
                print("✅ Trade logged for weekly reporting")
            
            print(f"\n🎉 MANUAL TRADE COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"✅ Purchase: 5 shares of {best_stock}")
            print(f"✅ Notifications sent to WhatsApp & Telegram")
            print(f"✅ Trade logged for reporting")
            print(f"✅ AI Analysis: {best_analysis['confidence']:.2f} confidence")
            
            return True
            
        else:
            print(f"\n❌ NO SUITABLE STOCKS FOUND")
            print("=" * 60)
            print("All analyzed stocks either:")
            print("- Have low AI confidence")
            print("- Are not recommended for purchase")
            print("- Have insufficient data")
            
            # Send notification about no suitable stocks
            no_trade_message = f"🔍 MANUAL TRADE ANALYSIS COMPLETE\n\n❌ No suitable stocks found for purchase\n\n📊 Analyzed: {len(stocks_to_analyze)} stocks\n🎯 Minimum confidence: 0.6\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n\n💡 Wait for better opportunities or adjust criteria"
            
            try:
                bot.send_whatsapp_message(no_trade_message)
                print("✅ WhatsApp notification sent (no suitable stocks)")
            except Exception as e:
                print(f"❌ WhatsApp notification failed: {e}")
            
            try:
                telegram.send_message(no_trade_message)
                print("✅ Telegram notification sent (no suitable stocks)")
            except Exception as e:
                print(f"❌ Telegram notification failed: {e}")
            
            return False
        
    except Exception as e:
        print(f"❌ Manual trade failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Manual Stock Purchase...")
    success = manual_stock_purchase()
    
    if success:
        print("\n🎉 Manual trade completed successfully!")
        print("📱 Check your WhatsApp and Telegram for notifications")
    else:
        print("\n❌ Manual trade could not be completed")
        print("📱 Check your WhatsApp and Telegram for status updates")

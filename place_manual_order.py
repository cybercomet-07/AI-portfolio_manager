#!/usr/bin/env python3
"""
Manual Order Placement Script
Place manual buy orders for specific stocks - REAL TRADING
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def place_manual_order():
    """Place a manual buy order for a specific stock"""
    print("🛒 MANUAL ORDER PLACEMENT - AI PORTFOLIO MANAGER")
    print("=" * 60)
    
    try:
        # Import required components
        from ai_trading_bot import AITradingBot
        from telegram_notifier import TelegramNotifier
        import alpaca_trade_api as tradeapi
        
        print("✅ All components imported successfully")
        
        # Initialize components
        print("\n🤖 Initializing AI Trading Bot...")
        bot = AITradingBot()
        print("✅ AI Trading Bot initialized")
        
        print("\n📱 Initializing Telegram Notifier...")
        telegram = TelegramNotifier()
        print("✅ Telegram Notifier initialized")
        
        # Initialize Alpaca API
        print("\n📊 Initializing Alpaca API...")
        alpaca_api_key = os.getenv("ALPACA_API_KEY")
        alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
        alpaca_api = tradeapi.REST(alpaca_api_key, alpaca_secret_key, 'https://paper-api.alpaca.markets')
        print("✅ Alpaca API initialized")
        
        # Check market status
        print("\n⏰ Checking market status...")
        try:
            clock = alpaca_api.get_clock()
            is_market_open = clock.is_open
            next_open = clock.next_open
            next_close = clock.next_close
            
            print(f"   Market Status: {'🟢 OPEN' if is_market_open else '🔴 CLOSED'}")
            if not is_market_open:
                print(f"   Next Open: {next_open.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Next Close: {next_close.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"   ⚠️ Could not check market status: {e}")
            is_market_open = False
        
        # Get stock information
        print("\n📊 Enter Stock Details:")
        print("-" * 40)
        
        # You can modify these values as needed
        stock_symbol = "NVDA"  # NVIDIA - a different stock
        quantity = 5
        price_per_share = 850.00  # Approximate current price
        
        print(f"📈 Stock Symbol: {stock_symbol}")
        print(f"📊 Quantity: {quantity} shares")
        print(f"💰 Price per share: ${price_per_share:.2f}")
        
        total_cost = quantity * price_per_share
        
        print(f"\n💰 Order Summary:")
        print(f"   Stock: {stock_symbol}")
        print(f"   Action: BUY")
        print(f"   Quantity: {quantity} shares")
        print(f"   Price: ${price_per_share:.2f} per share")
        print(f"   Total Cost: ${total_cost:.2f}")
        
        # Check account balance
        print(f"\n💳 Checking account balance...")
        try:
            account = alpaca_api.get_account()
            buying_power = float(account.buying_power)
            print(f"   Available Buying Power: ${buying_power:,.2f}")
            
            if buying_power < total_cost:
                print(f"   ❌ Insufficient funds! Need ${total_cost:,.2f}, have ${buying_power:,.2f}")
                return False
            else:
                print(f"   ✅ Sufficient funds available")
        except Exception as e:
            print(f"   ⚠️ Could not check account balance: {e}")
        
        # Execute order based on market status
        if is_market_open:
            print(f"\n🚀 Market is OPEN - Placing REAL ORDER...")
            
            try:
                # Place the actual order
                order = alpaca_api.submit_order(
                    symbol=stock_symbol,
                    qty=quantity,
                    side='buy',
                    type='market',
                    time_in_force='day'
                )
                
                print(f"✅ REAL ORDER PLACED SUCCESSFULLY!")
                print(f"   Order ID: {order.id}")
                print(f"   Status: {order.status}")
                print(f"   Stock: {stock_symbol}")
                print(f"   Quantity: {quantity} shares")
                print(f"   Type: Market Order")
                print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Send success notifications
                success_message = f"🚀 REAL ORDER EXECUTED!\n\n📈 Stock: {stock_symbol}\n🎯 Action: BUY\n📊 Shares: {quantity}\n💰 Price: Market Price\n💵 Total: ~${total_cost:.2f}\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n\n🏷️ Order Type: REAL MARKET ORDER\n🆔 Order ID: {order.id}\n✅ Order Status: {order.status}"
                
                # WhatsApp notification
                try:
                    bot.send_whatsapp_message(success_message)
                    print("✅ WhatsApp notification sent!")
                except Exception as e:
                    print(f"❌ WhatsApp notification failed: {e}")
                
                # Telegram notification
                try:
                    telegram.send_message(success_message)
                    print("✅ Telegram notification sent!")
                except Exception as e:
                    print(f"❌ Telegram notification failed: {e}")
                
                # Log the trade
                trade_data = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': stock_symbol,
                    'action': 'BUY',
                    'quantity': quantity,
                    'price': price_per_share,
                    'total': total_cost,
                    'type': 'REAL_MARKET_ORDER',
                    'order_id': order.id,
                    'order_status': order.status,
                    'ai_confidence': 1.0,
                    'reasoning': 'Manual order placed by user - REAL TRADE'
                }
                
                # Add to bot's weekly trades for reporting
                if hasattr(bot, 'weekly_trades'):
                    bot.weekly_trades.append(trade_data)
                    print("✅ Trade logged for weekly reporting")
                
                return True
                
            except Exception as e:
                print(f"❌ Failed to place real order: {e}")
                return False
                
        else:
            print(f"\n⏰ Market is CLOSED - Placing PENDING ORDER with Alpaca...")
            
            try:
                # Submit a pending order that will execute when market opens
                pending_order = alpaca_api.submit_order(
                    symbol=stock_symbol,
                    qty=quantity,
                    side='buy',
                    type='market',
                    time_in_force='day',
                    extended_hours=False  # Only execute during regular market hours
                )
                
                print(f"✅ PENDING ORDER PLACED WITH ALPACA!")
                print(f"   Order ID: {pending_order.id}")
                print(f"   Status: {pending_order.status}")
                print(f"   Stock: {stock_symbol}")
                print(f"   Quantity: {quantity} shares")
                print(f"   Type: Market Order (Pending)")
                print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   ⏰ Will execute when market opens tomorrow")
                
                # Send pending order notification
                pending_message = f"⏰ PENDING ORDER PLACED - Market Closed\n\n📈 Stock: {stock_symbol}\n🎯 Action: BUY\n📊 Shares: {quantity}\n💰 Price: Market Price (when opens)\n💵 Total: ~${total_cost:.2f}\n⏰ Placed: {datetime.now().strftime('%H:%M:%S')}\n\n🏷️ Order Type: PENDING MARKET ORDER\n🆔 Order ID: {pending_order.id}\n📊 Status: {pending_order.status}\n⏰ Will execute when market opens\n📅 Next Open: {next_open.strftime('%Y-%m-%d %H:%M:%S') if 'next_open' in locals() else 'Unknown'}"
                
                # WhatsApp notification
                try:
                    bot.send_whatsapp_message(pending_message)
                    print("✅ WhatsApp notification sent (pending order)")
                except Exception as e:
                    print(f"❌ WhatsApp notification failed: {e}")
                
                # Telegram notification
                try:
                    telegram.send_message(pending_message)
                    print("✅ Telegram notification sent (pending order)")
                except Exception as e:
                    print(f"❌ Telegram notification failed: {e}")
                
                # Log the trade
                trade_data = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': stock_symbol,
                    'action': 'BUY',
                    'quantity': quantity,
                    'price': price_per_share,
                    'total': total_cost,
                    'type': 'PENDING_MARKET_ORDER',
                    'order_id': pending_order.id,
                    'order_status': pending_order.status,
                    'ai_confidence': 1.0,
                    'reasoning': 'Manual order placed by user - PENDING ORDER'
                }
                
                # Add to bot's weekly trades for reporting
                if hasattr(bot, 'weekly_trades'):
                    bot.weekly_trades.append(trade_data)
                    print("✅ Trade logged for weekly reporting")
                
                print(f"\n📋 PENDING ORDER PLACED SUCCESSFULLY!")
                print("=" * 60)
                print(f"✅ Order submitted to Alpaca: {stock_symbol}")
                print(f"✅ Order ID: {pending_order.id}")
                print(f"✅ Status: {pending_order.status}")
                print(f"✅ Will execute automatically when market opens")
                print(f"✅ Check your Alpaca dashboard for pending orders")
                
                return True
                
            except Exception as e:
                print(f"❌ Failed to place pending order: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Manual order failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Manual Order Placement...")
    success = place_manual_order()
    
    if success:
        print("\n🎉 Manual order process completed!")
        print("📱 Check your WhatsApp and Telegram for notifications")
    else:
        print("\n❌ Manual order could not be completed")
        print("📱 Check your WhatsApp and Telegram for status updates")

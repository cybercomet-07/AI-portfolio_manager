#!/usr/bin/env python3
"""
Telegram Notifier - Send daily trade summaries and alerts
"""

import requests
import os
from datetime import datetime
import json

class TelegramNotifier:
    def __init__(self):
        """Initialize Telegram notifier"""
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8242945520:AAHfsijFpaY2oRK95dQGVmD0VpaiOEGChlA")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def send_message(self, message):
        """Send a message via Telegram"""
        try:
            if not self.chat_id:
                print("⚠️ TELEGRAM_CHAT_ID not set - skipping Telegram message")
                return False
                
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"📱 Telegram: Message sent successfully")
                return True
            else:
                print(f"❌ Telegram Error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram Error: {e}")
            return False
    
    def send_daily_summary(self, portfolio_data, trades_today):
        """Send daily trading summary"""
        try:
            # Create daily summary message
            message = f"""
🤖 <b>AI Portfolio Manager - Daily Summary</b>
📅 {datetime.now().strftime('%Y-%m-%d')}

💰 <b>Portfolio Value:</b> ${portfolio_data.get('total_value', 0):,.2f}
📈 <b>Total Return:</b> {portfolio_data.get('total_return', 0):.2f}%
📊 <b>Positions:</b> {portfolio_data.get('position_count', 0)}
💵 <b>Cash:</b> ${portfolio_data.get('cash', 0):,.2f}

🔄 <b>Trades Today:</b> {len(trades_today)}
📋 <b>Recent Trades:</b>
"""
            
            # Add recent trades
            for trade in trades_today[-5:]:  # Last 5 trades
                emoji = "🟢" if trade.get('action') == 'BUY' else "🔴"
                message += f"{emoji} {trade.get('symbol', 'N/A')} {trade.get('action', 'N/A')} @ ${trade.get('price', 0):.2f}\n"
            
            message += f"\n⚡ <i>Powered by AI Portfolio Manager</i>"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"❌ Error sending daily summary: {e}")
            return False
    
    def send_trade_alert(self, trade_data):
        """Send individual trade alert"""
        try:
            emoji = "🟢" if trade_data.get('action') == 'BUY' else "🔴"
            confidence = trade_data.get('confidence', 0)
            
            message = f"""
{emoji} <b>AI Trade Alert</b>

📈 <b>Symbol:</b> {trade_data.get('symbol', 'N/A')}
🔄 <b>Action:</b> {trade_data.get('action', 'N/A')}
💰 <b>Price:</b> ${trade_data.get('price', 0):.2f}
📊 <b>Shares:</b> {trade_data.get('shares', 0)}
🎯 <b>Confidence:</b> {confidence:.1f}%

💭 <b>AI Reasoning:</b>
{trade_data.get('reasoning', 'No reasoning provided')}

⏰ {datetime.now().strftime('%H:%M:%S')}
"""
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"❌ Error sending trade alert: {e}")
            return False
    
    def send_portfolio_alert(self, alert_type, message):
        """Send portfolio alert"""
        try:
            emoji_map = {
                'low_cash': '⚠️',
                'high_concentration': '🚨',
                'too_many_positions': '📊',
                'high_losses': '💸',
                'general': 'ℹ️'
            }
            
            emoji = emoji_map.get(alert_type, 'ℹ️')
            
            alert_message = f"""
{emoji} <b>Portfolio Alert</b>

{message}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            return self.send_message(alert_message)
            
        except Exception as e:
            print(f"❌ Error sending portfolio alert: {e}")
            return False
    
    def send_startup_message(self):
        """Send startup notification"""
        message = f"""
🚀 <b>AI Portfolio Manager Started!</b>

🤖 Bot is now running 24/7
📈 Monitoring: AAPL, MSFT, GOOGL, AMZN, TSLA, CRM, PLD, AVGO
🎯 Min Confidence: 70%
📊 Max Daily Trades: 10

⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)

# Test function
if __name__ == "__main__":
    notifier = TelegramNotifier()
    
    # Test message
    test_message = "🧪 Testing Telegram integration for AI Portfolio Manager!"
    notifier.send_message(test_message)
    
    print("✅ Telegram notifier test complete!")

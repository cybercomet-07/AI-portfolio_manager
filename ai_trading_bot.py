import time
import yfinance as yf
import pandas as pd
from datetime import datetime
from alpaca_trade_api.rest import REST
from twilio.rest import Client
import json
import os

# Import our custom modules
from ai_trading_engine import AITradingEngine
from portfolio_tracker import PortfolioTracker
from telegram_notifier import TelegramNotifier
from email_reporter import EmailReporter

class AITradingBot:
    def __init__(self):
        """Initialize AI Trading Bot with all components"""
        
        # 🔐 Alpaca Paper Trading Keys
        self.API_KEY = os.getenv("ALPACA_API_KEY", "your_alpaca_api_key")
        self.API_SECRET = os.getenv("ALPACA_SECRET_KEY", "your_alpaca_secret_key")
        self.BASE_URL = 'https://paper-api.alpaca.markets'
        self.api = REST(self.API_KEY, self.API_SECRET, self.BASE_URL)
        
        # 🔐 Twilio WhatsApp Credentials
        self.TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_account_sid")
        self.TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_auth_token")
        self.FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER", "whatsapp:+14155238886")
        self.TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER", "whatsapp:+your_phone_number")
        self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        
        # 🤖 AI Trading Engine
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")
        self.ai_engine = AITradingEngine(self.gemini_api_key)
        
        # 📊 Portfolio Tracker
        self.portfolio_tracker = PortfolioTracker(self.api)
        
        # 📱 Telegram Notifier
        self.telegram = TelegramNotifier()
        
        # 📧 Email Reporter
        self.email_reporter = EmailReporter()
        
        # 📈 Trading Configuration
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "CRM", "PLD", "AVGO"]
        self.min_confidence = 0.7  # Minimum AI confidence for trades
        self.max_daily_trades = 10  # Maximum trades per day
        self.daily_trades = 0
        self.last_trade_date = None
        
        # 📝 Logging
        self.trading_log_file = "ai_trading_log.csv"
        self.decision_log_file = "ai_decisions.json"
        self.weekly_trades = []  # Track weekly trades for email reports
        
    def send_whatsapp_message(self, message):
        """Send WhatsApp notification"""
        try:
            self.client.messages.create(
                body=message, 
                from_=self.FROM_WHATSAPP_NUMBER, 
                to=self.TO_WHATSAPP_NUMBER
            )
            print(f"📲 WhatsApp: {message}")
        except Exception as e:
            print(f"❌ WhatsApp Error: {e}")
    
    def send_telegram_message(self, message):
        """Send Telegram notification"""
        try:
            self.telegram.send_message(message)
        except Exception as e:
            print(f"❌ Telegram Error: {e}")
    
    def send_trade_notifications(self, trade_data):
        """Send trade notifications via WhatsApp and Telegram"""
        try:
            # WhatsApp notification
            msg = f"🤖 AI TRADE:\n{trade_data['symbol']} {trade_data['action']} @ ${trade_data['price']:.2f}\nConfidence: {trade_data['confidence']:.1f}%"
            self.send_whatsapp_message(msg)
            
            # Telegram notification
            self.telegram.send_trade_alert(trade_data)
            
        except Exception as e:
            print(f"❌ Error sending trade notifications: {e}")
    
    def send_daily_summary(self):
        """Send daily summary via Telegram"""
        try:
            portfolio = self.portfolio_tracker.get_current_portfolio()
            if portfolio:
                # Get today's trades from log
                today_trades = self.get_todays_trades()
                self.telegram.send_daily_summary(portfolio, today_trades)
        except Exception as e:
            print(f"❌ Error sending daily summary: {e}")
    
    def send_weekly_email_report(self):
        """Send weekly email report"""
        try:
            portfolio = self.portfolio_tracker.get_current_portfolio()
            if portfolio and self.weekly_trades:
                self.email_reporter.send_weekly_report(portfolio, self.weekly_trades, {})
        except Exception as e:
            print(f"❌ Error sending weekly email report: {e}")
    
    def get_todays_trades(self):
        """Get today's trades from log file"""
        try:
            today_trades = []
            if os.path.exists(self.trading_log_file):
                with open(self.trading_log_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) >= 6:
                            trade_time = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S.%f')
                            if trade_time.date() == datetime.now().date():
                                today_trades.append({
                                    'timestamp': parts[0],
                                    'symbol': parts[1],
                                    'action': parts[2],
                                    'price': float(parts[3]),
                                    'shares': int(parts[4]),
                                    'confidence': float(parts[5])
                                })
            return today_trades
        except Exception as e:
            print(f"❌ Error getting today's trades: {e}")
            return []
    
    def reset_daily_trades(self):
        """Reset daily trade counter if it's a new day"""
        today = datetime.now().date()
        if self.last_trade_date != today:
            self.daily_trades = 0
            self.last_trade_date = today
    
    def log_ai_decision(self, decision):
        """Log AI decision to file"""
        try:
            decisions = []
            if os.path.exists(self.decision_log_file):
                with open(self.decision_log_file, 'r') as f:
                    decisions = json.load(f)
            
            decisions.append(decision)
            
            with open(self.decision_log_file, 'w') as f:
                json.dump(decisions, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error logging AI decision: {e}")
    
    def log_trade(self, symbol, action, price, shares, confidence, reasoning):
        """Log trade to CSV file"""
        try:
            with open(self.trading_log_file, "a") as f:
                f.write(f"{datetime.now()},{symbol},{action},{price:.2f},{shares},{confidence:.2f},{reasoning}\n")
        except Exception as e:
            print(f"❌ Error logging trade: {e}")
    
    def get_position_qty(self, symbol):
        """Get current position quantity for a symbol"""
        try:
            position = self.api.get_position(symbol)
            return int(float(position.qty))
        except:
            return 0
    
    def execute_ai_trade(self, decision, portfolio_info):
        """Execute trade based on AI decision"""
        try:
            symbol = decision['symbol']
            action = decision['action']
            confidence = decision['confidence']
            reasoning = decision['reasoning']
            current_price = decision['current_price']
            
            # Skip if confidence is too low
            if confidence < self.min_confidence:
                print(f"⚠️ Skipping {symbol} - Low confidence: {confidence:.2f}")
                return False
            
            # Skip if daily trade limit reached
            if self.daily_trades >= self.max_daily_trades:
                print(f"⚠️ Daily trade limit reached ({self.max_daily_trades})")
                return False
            
            # Get position sizing
            position_size = self.ai_engine.optimize_position_size(
                decision, 
                portfolio_info['total_value'], 
                portfolio_info['positions']
            )
            
            if not position_size:
                print(f"❌ Could not calculate position size for {symbol}")
                return False
            
            shares = position_size['shares']
            if shares <= 0:
                print(f"⚠️ Invalid share count for {symbol}: {shares}")
                return False
            
            # Execute trade
            if action == "BUY":
                # Check if we already have a position
                current_position = self.get_position_qty(symbol)
                if current_position > 0:
                    print(f"⚠️ Already have position in {symbol}: {current_position} shares")
                    return False
                
                # Place buy order
                order = self.api.submit_order(
                    symbol=symbol, 
                    qty=shares, 
                    side='buy', 
                    type='market', 
                    time_in_force='gtc'
                )
                
                msg = f"🤖 AI BUY: {shares} shares of {symbol} at ${current_price:.2f}\nConfidence: {confidence:.2f}\nReason: {reasoning[:100]}..."
                
            elif action == "SELL":
                # Check if we have a position to sell
                current_position = self.get_position_qty(symbol)
                if current_position <= 0:
                    print(f"⚠️ No position to sell for {symbol}")
                    return False
                
                # Place sell order
                order = self.api.submit_order(
                    symbol=symbol, 
                    qty=current_position, 
                    side='sell', 
                    type='market', 
                    time_in_force='gtc'
                )
                
                msg = f"🤖 AI SELL: {current_position} shares of {symbol} at ${current_price:.2f}\nConfidence: {confidence:.2f}\nReason: {reasoning[:100]}..."
            
            else:  # HOLD
                print(f"🤖 AI HOLD: {symbol} - {reasoning[:100]}...")
                return False
            
            # Send notifications and log
            trade_data = {
                'symbol': symbol,
                'action': action,
                'price': current_price,
                'shares': shares if action == 'BUY' else current_position,
                'confidence': confidence,
                'reasoning': reasoning
            }
            
            # Send notifications via WhatsApp and Telegram
            self.send_trade_notifications(trade_data)
            
            # Log trade
            self.log_trade(symbol, action, current_price, shares if action == 'BUY' else current_position, confidence, reasoning)
            
            # Add to weekly trades for email reports
            self.weekly_trades.append(trade_data)
            
            # Increment daily trade counter
            self.daily_trades += 1
            
            print(f"✅ Trade executed: {msg}")
            return True
            self.daily_trades += 1
            
            print(f"✅ {msg}")
            return True
            
        except Exception as e:
            print(f"❌ Error executing trade for {symbol}: {e}")
            return False
    
    def analyze_portfolio_risk(self):
        """Analyze portfolio risk and send alerts"""
        try:
            portfolio = self.portfolio_tracker.get_current_portfolio()
            if not portfolio:
                return
            
            risk_check = self.portfolio_tracker.check_risk_limits(portfolio)
            
            if risk_check['status'] == 'warning':
                warnings = risk_check['warnings']
                msg = f"⚠️ PORTFOLIO RISK ALERTS:\n" + "\n".join(warnings)
                self.send_whatsapp_message(msg)
                print(f"⚠️ Risk alerts: {warnings}")
            
        except Exception as e:
            print(f"❌ Error analyzing portfolio risk: {e}")
    
    def run_ai_analysis_cycle(self):
        """Run one complete AI analysis cycle"""
        try:
            print(f"\n🚀 Starting AI Analysis Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Reset daily trades if new day
            self.reset_daily_trades()
            
            # Get current portfolio
            portfolio = self.portfolio_tracker.get_current_portfolio()
            if not portfolio:
                print("❌ Could not get portfolio data")
                return
            
            # Generate portfolio report
            report = self.portfolio_tracker.generate_portfolio_report()
            if report:
                print(f"📊 Portfolio: {report['summary']['total_value']} | Return: {report['summary']['total_return']} | Positions: {report['summary']['position_count']}")
            
            # Analyze each stock with AI
            for i, symbol in enumerate(self.tickers):
                try:
                    print(f"\n🔍 Analyzing {symbol}... ({i+1}/{len(self.tickers)})")
                    
                    # Get AI decision
                    decision = self.ai_engine.get_ai_decision(symbol, portfolio)
                    if not decision:
                        continue
                    
                    # Log AI decision
                    self.log_ai_decision(decision)
                    
                    # Execute trade if needed
                    if decision['action'] in ['BUY', 'SELL']:
                        self.execute_ai_trade(decision, portfolio)
                    
                    # Rate limiting: Wait 5 seconds between API calls (15 requests per minute)
                    if i < len(self.tickers) - 1:  # Don't wait after the last stock
                        print("⏳ Waiting 5 seconds for rate limit...")
                        time.sleep(5)
                    
                except Exception as e:
                    print(f"❌ Error analyzing {symbol}: {e}")
                    continue
            
            # Analyze portfolio risk
            self.analyze_portfolio_risk()
            
            print(f"✅ AI Analysis Cycle Complete - Daily trades: {self.daily_trades}/{self.max_daily_trades}")
            
        except Exception as e:
            print(f"❌ Error in AI analysis cycle: {e}")
    
    def wait_for_market_open(self):
        """Wait for market to open"""
        while True:
            clock = self.api.get_clock()
            if clock.is_open:
                print("✅ Market is open. Starting AI trading bot...\n")
                break
            else:
                print("⏳ Waiting for market to open...")
                time.sleep(60)
    
    def run_bot(self):
        """Main bot loop"""
        try:
            self.wait_for_market_open()
            
            print("🤖 AI Trading Bot Started!")
            print(f"📈 Monitoring: {', '.join(self.tickers)}")
            print(f"🎯 Min Confidence: {self.min_confidence}")
            print(f"📊 Max Daily Trades: {self.max_daily_trades}")
            print("⏰ Running every 30 minutes during market hours...\n")
            
            while True:
                clock = self.api.get_clock()
                if not clock.is_open:
                    print("📴 Market is closed. Exiting AI trading bot.")
                    break
                
                # Run AI analysis cycle
                self.run_ai_analysis_cycle()
                
                print("⏸ Sleeping for 30 minutes...\n")
                time.sleep(1800)  # 30 minutes
                
        except KeyboardInterrupt:
            print("\n🛑 AI Trading Bot stopped by user")
        except Exception as e:
            print(f"❌ Error in main bot loop: {e}")

# Main execution
if __name__ == "__main__":
    bot = AITradingBot()
    bot.run_bot()

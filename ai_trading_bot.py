import os
import time
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ai_trading_engine import AITradingEngine
from portfolio_tracker import PortfolioTracker
from telegram_notifier import TelegramNotifier
from email_reporter import EmailReporter
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
from twilio.rest import Client

# Load environment variables
load_dotenv()

class AITradingBot:
    def __init__(self):
        """Initialize AI Trading Bot"""
        # Initialize components
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.alpaca_api_key = os.getenv("ALPACA_API_KEY")
        self.alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
        
        # Initialize trading components
        self.ai_engine = AITradingEngine(self.gemini_api_key)
        self.alpaca_api = tradeapi.REST(self.alpaca_api_key, self.alpaca_secret_key, 'https://paper-api.alpaca.markets')
        self.portfolio = PortfolioTracker(self.alpaca_api)
        self.telegram = TelegramNotifier()
        self.email_reporter = EmailReporter()
        
        # Trading configuration
        self.min_confidence = float(os.getenv("MIN_CONFIDENCE", 0.7))
        self.max_daily_trades = int(os.getenv("MAX_DAILY_TRADES", 10))
        self.risk_tolerance = os.getenv("RISK_TOLERANCE", "moderate")
        self.max_position_size = float(os.getenv("MAX_POSITION_SIZE", 0.1))
        
        # Current stocks to monitor (existing system)
        self.stocks_to_monitor = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "CRM", "PLD", "AVGO"]
        
        # New stock discovery configuration
        self.discovery_enabled = True
        self.price_min = 2000.0  # Minimum stock price
        self.price_max = 3000.0  # Maximum stock price
        self.max_new_positions = 3  # Maximum new stocks to add
        self.discovery_interval = 2  # Check for new stocks every 2 cycles
        
        # Stock discovery tracking
        self.discovered_stocks = []
        self.discovery_cycle_count = 0
        self.weekly_trades = []
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        print("🤖 AI Trading Bot initialized successfully")
        print(f"📈 Monitoring: {', '.join(self.stocks_to_monitor)}")
        print(f"🔍 Stock Discovery: {'Enabled' if self.discovery_enabled else 'Disabled'}")
        print(f"💰 Price Range: ${self.price_min:,.0f} - ${self.price_max:,.0f}")
        print(f"📱 Telegram Chat ID: {os.getenv('TELEGRAM_CHAT_ID', 'Not Set')}")
        print(f"📧 Email configured: {'Yes' if hasattr(self.email_reporter, 'email') and self.email_reporter.email else 'No'}")

    def send_whatsapp_message(self, message):
        """Send WhatsApp notification"""
        try:
            self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
            self.FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER", "whatsapp:+14155238886")
            self.TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER", "whatsapp:+your_phone_number")
            self.client.messages.create(
                body=message, 
                from_=self.FROM_WHATSAPP_NUMBER,
                to=self.TO_WHATSAPP_NUMBER
            )
            print(f"📲 WhatsApp: {message[:50]}...")
            return True
        except Exception as e:
            print(f"❌ WhatsApp notification failed: {e}")
            return False

    def send_telegram_message(self, message):
        """Send Telegram notification"""
        try:
            success = self.telegram.send_message(message)
            if success:
                print(f"📱 Telegram: Message sent successfully")
            return success
        except Exception as e:
            print(f"❌ Telegram notification failed: {e}")
            return False

    def send_trade_notifications(self, trade_data):
        """Send trade notifications to all platforms"""
        # WhatsApp notification
        whatsapp_msg = f"🚀 TRADE EXECUTED!\n\n📈 Stock: {trade_data['symbol']}\n🎯 Action: {trade_data['action']}\n📊 Quantity: {trade_data['quantity']} shares\n💰 Price: ${trade_data['price']:.2f}\n💵 Total: ${trade_data['total']:.2f}\n⏰ Time: {datetime.fromisoformat(trade_data['timestamp']).strftime('%H:%M:%S')}\n\n🤖 AI Confidence: {trade_data.get('ai_confidence', 'N/A')}"
        
        self.send_whatsapp_message(whatsapp_msg)
        
        # Telegram notification
        telegram_msg = f"🚀 TRADE EXECUTED!\n\n📈 Stock: {trade_data['symbol']}\n🎯 Action: {trade_data['action']}\n📊 Quantity: {trade_data['quantity']} shares\n💰 Price: ${trade_data['price']:.2f}\n💵 Total: ${trade_data['total']:.2f}\n⏰ Time: {datetime.fromisoformat(trade_data['timestamp']).strftime('%H:%M:%S')}\n\n🤖 AI Confidence: {trade_data.get('ai_confidence', 'N/A')}"
        
        self.send_telegram_message(telegram_msg)

    def execute_ai_trade(self, symbol, action, decision):
        """Execute AI trading decision"""
        try:
            # Get current stock price
            stock = yf.Ticker(symbol)
            current_price = stock.info.get('currentPrice', 0)
            
            if current_price == 0:
                print(f"   ❌ Could not get current price for {symbol}")
                return False
            
            # Calculate position size based on risk management
            account = self.alpaca_api.get_account()
            portfolio_value = float(account.portfolio_value)
            max_position_value = portfolio_value * self.max_position_size
            
            # Conservative position sizing for new stocks
            if symbol not in self.stocks_to_monitor:
                max_position_value = min(max_position_value, 10000)  # Max $10k for new stocks
            
            position_size = int(max_position_value / current_price)
            
            if position_size < 1:
                print(f"   ⚠️ Position size too small for {symbol}")
                return False
            
            print(f"   📊 Executing {action.upper()} for {symbol}")
            print(f"      Shares: {position_size}")
            print(f"      Price: ${current_price:.2f}")
            print(f"      Total: ${position_size * current_price:.2f}")
            
            # Place the order
            order = self.alpaca_api.submit_order(
                symbol=symbol,
                qty=position_size,
                side=action.lower(),
                type='market',
                time_in_force='day'
            )
            
            print(f"      ✅ Order placed: {order.id}")
            
            # Create trade data
            trade_data = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'action': action.upper(),
                'quantity': position_size,
                'price': current_price,
                'total': position_size * current_price,
                'type': 'AI_TRADE',
                'order_id': order.id,
                'order_status': order.status,
                'ai_confidence': decision.get('confidence', 0),
                'reasoning': decision.get('reasoning', '')
            }
            
            # Add to weekly trades
            self.weekly_trades.append(trade_data)
            
            # Send notifications
            self.send_trade_notifications(trade_data)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error executing trade for {symbol}: {e}")
            return False

    def discover_new_stocks(self):
        """Discover new profitable stocks based on AI analysis"""
        if not self.discovery_enabled:
            return []
        
        print(f"\n🔍 STOCK DISCOVERY CYCLE - Cycle {self.discovery_cycle_count}")
        print("=" * 60)
        
        # Define sectors to explore for new opportunities
        sectors = {
            'Technology': ['NVDA', 'AMD', 'SNOW', 'PLTR', 'CRWD', 'ZS', 'NET', 'OKTA'],
            'Healthcare': ['MRNA', 'BNTX', 'REGN', 'VRTX', 'ALNY', 'IONS', 'SGEN'],
            'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'SCHW', 'V', 'MA'],
            'Consumer': ['NKE', 'SBUX', 'HD', 'LOW', 'TGT', 'COST', 'TJX'],
            'Industrial': ['CAT', 'DE', 'BA', 'LMT', 'RTX', 'GE', 'MMM'],
            'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL']
        }
        
        discovered_opportunities = []
        
        for sector, stocks in sectors.items():
            print(f"\n🏭 Analyzing {sector} sector...")
            
            for symbol in stocks:
                try:
                    # Check if stock is already in portfolio or monitoring
                    if symbol in self.stocks_to_monitor or symbol in [pos.symbol for pos in self.alpaca_api.list_positions()]:
                        continue
                    
                    # Get current stock info
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    
                    # Check price range
                    current_price = info.get('currentPrice', 0)
                    if not (self.price_min <= current_price <= self.price_max):
                        continue
                    
                    print(f"   🔍 Analyzing {symbol} at ${current_price:.2f}")
                    
                    # Get technical indicators
                    indicators = self.ai_engine.get_technical_indicators(symbol)
                    if not indicators:
                        continue
                    
                    # Get market context
                    context = self.ai_engine.get_market_context(symbol)
                    
                    # Get AI decision
                    decision = self.ai_engine.get_ai_decision(symbol, indicators)
                    
                    if decision and decision.get('action') == 'buy':
                        confidence = decision.get('confidence', 0)
                        
                        if confidence >= self.min_confidence:
                            opportunity = {
                                'symbol': symbol,
                                'sector': sector,
                                'current_price': current_price,
                                'confidence': confidence,
                                'reasoning': decision.get('reasoning', ''),
                                'indicators': indicators,
                                'context': context
                            }
                            
                            discovered_opportunities.append(opportunity)
                            print(f"      ✅ {symbol}: BUY signal (Confidence: {confidence:.2f})")
                        else:
                            print(f"      ⚠️ {symbol}: Low confidence ({confidence:.2f})")
                    else:
                        print(f"      ❌ {symbol}: No buy signal")
                    
                    # Rate limiting
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"      ❌ Error analyzing {symbol}: {e}")
                    continue
        
        # Sort opportunities by confidence
        discovered_opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Limit to maximum new positions
        if len(discovered_opportunities) > self.max_new_positions:
            discovered_opportunities = discovered_opportunities[:self.max_new_positions]
        
        if discovered_opportunities:
            print(f"\n🎯 DISCOVERY RESULTS:")
            print("=" * 60)
            for opp in discovered_opportunities:
                print(f"📈 {opp['symbol']} ({opp['sector']})")
                print(f"   💰 Price: ${opp['current_price']:.2f}")
                print(f"   ⭐ Confidence: {opp['confidence']:.2f}")
                print(f"   💡 {opp['reasoning'][:100]}...")
                print()
        else:
            print(f"\n❌ No new opportunities found in this cycle")
        
        return discovered_opportunities

    def execute_discovery_trades(self, opportunities):
        """Execute trades for discovered stock opportunities"""
        if not opportunities:
            return
        
        print(f"\n🚀 EXECUTING DISCOVERY TRADES")
        print("=" * 60)
        
        for opportunity in opportunities:
            try:
                symbol = opportunity['symbol']
                current_price = opportunity['current_price']
                confidence = opportunity['confidence']
                
                # Calculate position size (conservative for new stocks)
                position_size = min(2, int(10000 / current_price))  # Max $10k per new stock
                
                if position_size < 1:
                    print(f"   ⚠️ {symbol}: Price too high for minimum position")
                    continue
                
                print(f"   📈 Placing order for {symbol}...")
                print(f"      Shares: {position_size}")
                print(f"      Price: ${current_price:.2f}")
                print(f"      Total: ${position_size * current_price:.2f}")
                
                # Place the order
                order = self.alpaca_api.submit_order(
                    symbol=symbol,
                    qty=position_size,
                    side='buy',
                    type='market',
                    time_in_force='day'
                )
                
                print(f"      ✅ Order placed: {order.id}")
                
                # Send notifications
                trade_data = {
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'action': 'BUY',
                    'quantity': position_size,
                    'price': current_price,
                    'total': position_size * current_price,
                    'type': 'AI_DISCOVERY_TRADE',
                    'order_id': order.id,
                    'order_status': order.status,
                    'ai_confidence': confidence,
                    'reasoning': opportunity['reasoning'],
                    'sector': opportunity['sector']
                }
                
                # Add to weekly trades
                self.weekly_trades.append(trade_data)
                
                # Send notifications
                self.send_trade_notifications(trade_data)
                
                # Add to monitoring list
                if symbol not in self.stocks_to_monitor:
                    self.stocks_to_monitor.append(symbol)
                    print(f"      📊 Added {symbol} to monitoring list")
                
                print(f"      🎉 Discovery trade completed for {symbol}")
                
            except Exception as e:
                print(f"   ❌ Error executing discovery trade for {symbol}: {e}")
                continue

    def run_ai_analysis_cycle(self):
        """Run one complete AI analysis cycle"""
        print(f"\n🧠 AI ANALYSIS CYCLE STARTED - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        daily_trades = 0
        
        # Analyze current stocks (existing functionality)
        for symbol in self.stocks_to_monitor:
            try:
                print(f"\n🔍 Analyzing {symbol}...")
                
                # Get technical indicators
                indicators = self.ai_engine.get_technical_indicators(symbol)
                if not indicators:
                    print(f"   ❌ No indicators available for {symbol}")
                    continue
                
                # Get AI decision
                decision = self.ai_engine.get_ai_decision(symbol, indicators)
                
                if decision and daily_trades < self.max_daily_trades:
                    action = decision.get('action', 'hold')
                    confidence = decision.get('confidence', 0)
                    
                    print(f"   🤖 AI Decision: {action.upper()} (Confidence: {confidence:.2f})")
                    
                    if confidence >= self.min_confidence and action in ['buy', 'sell']:
                        if self.execute_ai_trade(symbol, action, decision):
                            daily_trades += 1
                            print(f"   ✅ Trade executed for {symbol}")
                        else:
                            print(f"   ❌ Trade failed for {symbol}")
                    else:
                        print(f"   ⚠️ Insufficient confidence or hold decision")
                else:
                    print(f"   ⏸️ No action taken for {symbol}")
                
                # Rate limiting between stocks
                time.sleep(5)
                
            except Exception as e:
                print(f"   ❌ Error analyzing {symbol}: {e}")
                continue
        
        # Stock discovery cycle (every few cycles)
        self.discovery_cycle_count += 1
        if self.discovery_cycle_count % self.discovery_interval == 0:
            print(f"\n🔍 STOCK DISCOVERY CYCLE (Every {self.discovery_interval} cycles)")
            opportunities = self.discover_new_stocks()
            if opportunities:
                self.execute_discovery_trades(opportunities)
        
        print(f"\n✔ AI Analysis Cycle Complete - Daily trades: {daily_trades}/{self.max_daily_trades}")
        return daily_trades

    def run_bot(self):
        """Main bot loop"""
        print("🚀 Starting AI Portfolio Manager...")
        
        # Send startup notifications
        startup_message = "🤖 AI Portfolio Manager is now running 24/7!"
        self.send_telegram_message(startup_message)
        self.send_whatsapp_message(startup_message)
        
        # Run initial analysis cycle
        self.run_ai_analysis_cycle()
        
        while True:
            try:
                # Check if market is open
                clock = self.alpaca_api.get_clock()
                
                if clock.is_open:
                    print(f"\n🟢 Market is OPEN - Running AI analysis...")
                    self.run_ai_analysis_cycle()
                    
                    # Sleep between cycles (30 minutes)
                    print("II Sleeping for 30 minutes...")
                    time.sleep(1800)  # 30 minutes
                else:
                    next_open = clock.next_open
                    time_until_open = next_open - datetime.now()
                    hours_until_open = time_until_open.total_seconds() / 3600
                    
                    print(f"\n🔴 Market is CLOSED")
                    print(f"   Next open: {next_open.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   Time until open: {hours_until_open:.1f} hours")
                    
                    # Sleep until market opens (check every hour)
                    sleep_time = min(3600, max(300, int(hours_until_open * 3600 / 2)))
                    print(f"   Sleeping for {sleep_time//60} minutes...")
                    time.sleep(sleep_time)
                    
            except Exception as e:
                print(f"❌ Error in main bot loop: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

# Main execution
if __name__ == "__main__":
    bot = AITradingBot()
    bot.run_bot()

import google.generativeai as genai
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime, timedelta
import json
import time

class AITradingEngine:
    def __init__(self, gemini_api_key):
        """Initialize AI Trading Engine with Gemini API"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.risk_tolerance = "moderate"  # conservative, moderate, aggressive
        self.max_position_size = 0.1  # 10% of portfolio per position
        
    def get_technical_indicators(self, symbol, period='60d'):
        """Get comprehensive technical indicators for a stock"""
        try:
            df = yf.download(symbol, period=period, interval='1h')
            df.dropna(inplace=True)
            
            if len(df) < 20:
                return None
                
            # Ensure we have 1D Series for technical analysis
            close_prices = df['Close'].squeeze()
            high_prices = df['High'].squeeze()
            low_prices = df['Low'].squeeze()
            volume = df['Volume'].squeeze()
            
            # Technical Indicators
            indicators = {
                'symbol': symbol,
                'current_price': close_prices.iloc[-1],
                'price_change_24h': ((close_prices.iloc[-1] - close_prices.iloc[-24]) / close_prices.iloc[-24] * 100) if len(close_prices) > 24 else 0,
                'volume_avg': volume.rolling(20).mean().iloc[-1],
                'volume_current': volume.iloc[-1],
                'rsi': ta.momentum.RSIIndicator(close_prices).rsi().iloc[-1],
                'macd': ta.trend.MACD(close_prices).macd().iloc[-1],
                'macd_signal': ta.trend.MACD(close_prices).macd_signal().iloc[-1],
                'bollinger_upper': ta.volatility.BollingerBands(close_prices).bollinger_hband().iloc[-1],
                'bollinger_lower': ta.volatility.BollingerBands(close_prices).bollinger_lband().iloc[-1],
                'sma_20': ta.trend.SMAIndicator(close_prices, window=20).sma_indicator().iloc[-1],
                'sma_50': ta.trend.SMAIndicator(close_prices, window=50).sma_indicator().iloc[-1],
                'ema_12': ta.trend.EMAIndicator(close_prices, window=12).ema_indicator().iloc[-1],
                'ema_26': ta.trend.EMAIndicator(close_prices, window=26).ema_indicator().iloc[-1],
                'stoch_k': ta.momentum.StochasticOscillator(high_prices, low_prices, close_prices).stoch().iloc[-1],
                'stoch_d': ta.momentum.StochasticOscillator(high_prices, low_prices, close_prices).stoch_signal().iloc[-1],
                'atr': ta.volatility.AverageTrueRange(high_prices, low_prices, close_prices).average_true_range().iloc[-1]
            }
            
            return indicators
            
        except Exception as e:
            print(f"❌ Error getting technical indicators for {symbol}: {e}")
            return None
    
    def get_market_context(self, symbol):
        """Get market context and sentiment for a stock"""
        try:
            # Get basic stock info
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Check if we got valid info
            if not info or len(info) == 0:
                print(f"⚠️ No market context data for {symbol}, using defaults")
                return {
                    'sector': 'Unknown',
                    'industry': 'Unknown',
                    'market_cap': 0,
                    'pe_ratio': 0,
                    'beta': 1.0,
                    'dividend_yield': 0,
                    'volume_avg': 0,
                    'price_to_book': 0,
                    'debt_to_equity': 0,
                    'current_ratio': 0,
                    'profit_margins': 0,
                    'revenue_growth': 0,
                    'earnings_growth': 0
                }
            
            # Get recent news (simplified - you can enhance with news API)
            context = {
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'beta': info.get('beta', 1.0),
                'dividend_yield': info.get('dividendYield', 0),
                'volume_avg': info.get('averageVolume', 0),
                'price_to_book': info.get('priceToBook', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'current_ratio': info.get('currentRatio', 0),
                'profit_margins': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0)
            }
            
            return context
            
        except Exception as e:
            print(f"❌ Error getting market context for {symbol}: {e}")
            return {
                'sector': 'Unknown',
                'industry': 'Unknown',
                'market_cap': 0,
                'pe_ratio': 0,
                'beta': 1.0,
                'dividend_yield': 0,
                'volume_avg': 0,
                'price_to_book': 0,
                'debt_to_equity': 0,
                'current_ratio': 0,
                'profit_margins': 0,
                'revenue_growth': 0,
                'earnings_growth': 0
            }
    
    def create_ai_prompt(self, indicators, context, portfolio_info=None):
        """Create comprehensive AI prompt for trading decision"""
        
        # Handle portfolio_info safely
        portfolio_value = portfolio_info.get('total_value', 100000) if portfolio_info else 100000
        
        prompt = f"""
You are an expert AI trading analyst. Analyze the following stock data and provide a trading recommendation.

STOCK: {indicators['symbol']}
CURRENT PRICE: ${indicators['current_price']:.2f}
24H CHANGE: {indicators['price_change_24h']:.2f}%

TECHNICAL INDICATORS:
- RSI: {indicators['rsi']:.2f} (Oversold < 30, Overbought > 70)
- MACD: {indicators['macd']:.4f} | Signal: {indicators['macd_signal']:.4f}
- Bollinger Bands: Upper ${indicators['bollinger_upper']:.2f} | Lower ${indicators['bollinger_lower']:.2f}
- SMA 20: ${indicators['sma_20']:.2f} | SMA 50: ${indicators['sma_50']:.2f}
- EMA 12: ${indicators['ema_12']:.2f} | EMA 26: {indicators['ema_26']:.2f}
- Stochastic: K={indicators['stoch_k']:.2f} | D={indicators['stoch_d']:.2f}
- ATR: ${indicators['atr']:.2f}

MARKET CONTEXT:
- Sector: {context.get('sector', 'Unknown')}
- Industry: {context.get('industry', 'Unknown')}
- P/E Ratio: {context.get('pe_ratio', 0):.2f}
- Beta: {context.get('beta', 1.0):.2f}
- Market Cap: ${context.get('market_cap', 0):,.0f}

PORTFOLIO CONTEXT:
- Risk Tolerance: {self.risk_tolerance}
- Max Position Size: {self.max_position_size * 100}% of portfolio
- Current Portfolio Value: ${portfolio_value:,.2f}

ANALYSIS REQUIREMENTS:
1. Analyze technical indicators for trend direction and momentum
2. Consider market context and sector performance
3. Assess risk-reward ratio based on current price levels
4. Factor in portfolio diversification and risk tolerance
5. Consider market volatility and ATR for position sizing

PROVIDE YOUR RESPONSE IN THIS EXACT JSON FORMAT:
{{
    "action": "BUY|SELL|HOLD",
    "confidence": 0.0-1.0,
    "reasoning": "Detailed explanation of your decision",
    "position_size": 0.0-1.0,
    "stop_loss": price,
    "take_profit": price,
    "risk_level": "LOW|MEDIUM|HIGH",
    "time_horizon": "SHORT|MEDIUM|LONG"
}}

Focus on risk management and provide clear reasoning for your decision.
"""
        return prompt
    
    def get_ai_decision(self, symbol, portfolio_info=None):
        """Get AI-powered trading decision for a stock"""
        try:
            print(f"🤖 Analyzing {symbol} with AI...")
            
            # Get technical indicators
            indicators = self.get_technical_indicators(symbol)
            if not indicators:
                return None
            
            # Get market context
            context = self.get_market_context(symbol)
            if not context:
                context = {}  # Use empty dict if context is None
            
            # Create AI prompt
            prompt = self.create_ai_prompt(indicators, context, portfolio_info)
            
            # Get AI response
            try:
                response = self.model.generate_content(prompt)
                
                # Parse AI response
                try:
                    decision = json.loads(response.text)
                    decision['symbol'] = symbol
                    decision['current_price'] = indicators['current_price']
                    decision['timestamp'] = datetime.now().isoformat()
                    
                    print(f"✅ AI Decision for {symbol}: {decision['action']} (Confidence: {decision['confidence']:.2f})")
                    return decision
                    
                except json.JSONDecodeError:
                    print(f"❌ Failed to parse AI response for {symbol}")
                    return None
                    
            except Exception as api_error:
                if "429" in str(api_error) or "quota" in str(api_error).lower():
                    print(f"⚠️ Rate limit hit for {symbol}. Waiting 60 seconds...")
                    time.sleep(60)  # Wait 1 minute for rate limit to reset
                    return None
                else:
                    print(f"❌ API Error for {symbol}: {api_error}")
                    return None
                
        except Exception as e:
            print(f"❌ Error getting AI decision for {symbol}: {e}")
            return None
    
    def optimize_position_size(self, decision, portfolio_value, current_positions):
        """Optimize position size based on AI decision and portfolio context"""
        try:
            base_size = decision['position_size']
            confidence = decision['confidence']
            risk_level = decision['risk_level']
            
            # Adjust based on confidence
            confidence_multiplier = 0.5 + (confidence * 0.5)  # 0.5 to 1.0
            
            # Adjust based on risk level
            risk_multiplier = {
                'LOW': 1.0,
                'MEDIUM': 0.8,
                'HIGH': 0.6
            }.get(risk_level, 0.8)
            
            # Adjust based on portfolio diversification
            diversification_multiplier = 1.0
            if len(current_positions) > 0:
                # Reduce size if already have many positions
                diversification_multiplier = max(0.5, 1.0 - (len(current_positions) * 0.1))
            
            # Calculate final position size
            final_size = base_size * confidence_multiplier * risk_multiplier * diversification_multiplier
            
            # Apply maximum position size limit
            final_size = min(final_size, self.max_position_size)
            
            # Calculate dollar amount
            position_value = portfolio_value * final_size
            
            return {
                'position_size_pct': final_size,
                'position_value': position_value,
                'shares': int(position_value / decision['current_price'])
            }
            
        except Exception as e:
            print(f"❌ Error optimizing position size: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Test the AI trading engine
    engine = AITradingEngine("AIzaSyABwil0lzrXXQ58jPFfmPS6HlGUNfA1LMc")
    
    # Test with a sample stock
    decision = engine.get_ai_decision("AAPL")
    if decision:
        print(f"AI Decision: {json.dumps(decision, indent=2)}")
        
        # Test position sizing
        portfolio_info = {'total_value': 100000}
        position_size = engine.optimize_position_size(decision, 100000, [])
        print(f"Position Size: {position_size}")

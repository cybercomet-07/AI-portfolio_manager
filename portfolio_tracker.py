import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class PortfolioTracker:
    def __init__(self, alpaca_api):
        """Initialize Portfolio Tracker"""
        self.api = alpaca_api
        self.portfolio_file = "portfolio_data.json"
        self.performance_file = "performance_log.csv"
        self.initial_balance = 100000  # Starting balance
        
    def get_current_portfolio(self):
        """Get current portfolio positions and value"""
        try:
            # Get account info
            account = self.api.get_account()
            portfolio_value = float(account.portfolio_value)
            cash = float(account.cash)
            
            # Get all positions
            positions = self.api.list_positions()
            position_data = []
            
            for position in positions:
                pos_info = {
                    'symbol': position.symbol,
                    'qty': int(float(position.qty)),
                    'avg_entry_price': float(position.avg_entry_price),
                    'current_price': float(position.current_price),
                    'market_value': float(position.market_value),
                    'unrealized_pl': float(position.unrealized_pl),
                    'unrealized_plpc': float(position.unrealized_plpc),
                    'side': position.side
                }
                position_data.append(pos_info)
            
            portfolio = {
                'timestamp': datetime.now().isoformat(),
                'total_value': portfolio_value,
                'cash': cash,
                'invested_value': portfolio_value - cash,
                'positions': position_data,
                'position_count': len(position_data)
            }
            
            return portfolio
            
        except Exception as e:
            print(f"❌ Error getting portfolio: {e}")
            return None
    
    def calculate_portfolio_metrics(self, portfolio):
        """Calculate portfolio performance metrics"""
        try:
            if not portfolio:
                return None
                
            # Basic metrics
            total_value = portfolio['total_value']
            cash = portfolio['cash']
            invested = portfolio['invested_value']
            positions = portfolio['positions']
            
            # Calculate returns
            total_return = ((total_value - self.initial_balance) / self.initial_balance) * 100
            
            # Calculate position metrics
            total_unrealized_pl = sum(pos['unrealized_pl'] for pos in positions)
            total_unrealized_pl_pct = (total_unrealized_pl / invested * 100) if invested > 0 else 0
            
            # Calculate diversification metrics
            if positions:
                position_values = [pos['market_value'] for pos in positions]
                total_position_value = sum(position_values)
                
                # Herfindahl index for concentration
                concentration = sum((val / total_position_value) ** 2 for val in position_values)
                
                # Sector diversification (simplified)
                sectors = {}
                for pos in positions:
                    sector = self.get_stock_sector(pos['symbol'])
                    if sector not in sectors:
                        sectors[sector] = 0
                    sectors[sector] += pos['market_value']
                
                sector_diversification = len(sectors)
                
            else:
                concentration = 0
                sector_diversification = 0
            
            metrics = {
                'total_value': total_value,
                'cash': cash,
                'invested_value': invested,
                'total_return_pct': total_return,
                'total_unrealized_pl': total_unrealized_pl,
                'total_unrealized_pl_pct': total_unrealized_pl_pct,
                'position_count': len(positions),
                'concentration_index': concentration,
                'sector_diversification': sector_diversification,
                'cash_ratio': (cash / total_value * 100) if total_value > 0 else 0,
                'invested_ratio': (invested / total_value * 100) if total_value > 0 else 0
            }
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error calculating portfolio metrics: {e}")
            return None
    
    def get_stock_sector(self, symbol):
        """Get sector for a stock (simplified)"""
        # You can enhance this with actual sector data
        sector_map = {
            'AAPL': 'Technology',
            'MSFT': 'Technology', 
            'GOOGL': 'Technology',
            'AMZN': 'Consumer Discretionary',
            'TSLA': 'Consumer Discretionary',
            'CRM': 'Technology',
            'PLD': 'Real Estate',
            'AVGO': 'Technology'
        }
        return sector_map.get(symbol, 'Unknown')
    
    def save_portfolio_snapshot(self, portfolio, metrics):
        """Save portfolio snapshot to file"""
        try:
            snapshot = {
                'portfolio': portfolio,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to JSON file
            with open(self.portfolio_file, 'w') as f:
                json.dump(snapshot, f, indent=2)
            
            # Save performance metrics to CSV
            if metrics:
                performance_row = {
                    'timestamp': datetime.now(),
                    'total_value': metrics['total_value'],
                    'total_return_pct': metrics['total_return_pct'],
                    'unrealized_pl': metrics['total_unrealized_pl'],
                    'position_count': metrics['position_count'],
                    'cash_ratio': metrics['cash_ratio']
                }
                
                df = pd.DataFrame([performance_row])
                if os.path.exists(self.performance_file):
                    df.to_csv(self.performance_file, mode='a', header=False, index=False)
                else:
                    df.to_csv(self.performance_file, index=False)
            
            print(f"✅ Portfolio snapshot saved")
            
        except Exception as e:
            print(f"❌ Error saving portfolio snapshot: {e}")
    
    def get_portfolio_history(self, days=30):
        """Get portfolio performance history"""
        try:
            if not os.path.exists(self.performance_file):
                return None
                
            df = pd.read_csv(self.performance_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter for last N days
            cutoff_date = datetime.now() - timedelta(days=days)
            df_filtered = df[df['timestamp'] >= cutoff_date]
            
            return df_filtered
            
        except Exception as e:
            print(f"❌ Error getting portfolio history: {e}")
            return None
    
    def generate_portfolio_report(self):
        """Generate comprehensive portfolio report"""
        try:
            portfolio = self.get_current_portfolio()
            if not portfolio:
                return None
                
            metrics = self.calculate_portfolio_metrics(portfolio)
            if not metrics:
                return None
            
            # Save snapshot
            self.save_portfolio_snapshot(portfolio, metrics)
            
            # Generate report
            report = {
                'summary': {
                    'total_value': f"${metrics['total_value']:,.2f}",
                    'total_return': f"{metrics['total_return_pct']:.2f}%",
                    'unrealized_pl': f"${metrics['total_unrealized_pl']:,.2f} ({metrics['total_unrealized_pl_pct']:.2f}%)",
                    'position_count': metrics['position_count'],
                    'cash_ratio': f"{metrics['cash_ratio']:.1f}%"
                },
                'positions': portfolio['positions'],
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            print(f"❌ Error generating portfolio report: {e}")
            return None
    
    def check_risk_limits(self, portfolio):
        """Check if portfolio meets risk management criteria"""
        try:
            if not portfolio:
                return {'status': 'error', 'message': 'No portfolio data'}
            
            metrics = self.calculate_portfolio_metrics(portfolio)
            if not metrics:
                return {'status': 'error', 'message': 'No metrics data'}
            
            warnings = []
            
            # Check cash ratio
            if metrics['cash_ratio'] < 5:
                warnings.append(f"Low cash ratio: {metrics['cash_ratio']:.1f}%")
            
            # Check concentration
            if metrics['concentration_index'] > 0.3:
                warnings.append(f"High concentration: {metrics['concentration_index']:.2f}")
            
            # Check position count
            if metrics['position_count'] > 20:
                warnings.append(f"Too many positions: {metrics['position_count']}")
            
            # Check unrealized losses
            if metrics['total_unrealized_pl_pct'] < -10:
                warnings.append(f"High unrealized losses: {metrics['total_unrealized_pl_pct']:.2f}%")
            
            status = 'warning' if warnings else 'ok'
            
            return {
                'status': status,
                'warnings': warnings,
                'metrics': metrics
            }
            
        except Exception as e:
            print(f"❌ Error checking risk limits: {e}")
            return {'status': 'error', 'message': str(e)}

# Example usage
if __name__ == "__main__":
    # This would be used with your Alpaca API instance
    print("Portfolio Tracker initialized")
    print("Use with your Alpaca API instance in the main trading bot")

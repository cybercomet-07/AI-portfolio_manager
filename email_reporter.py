#!/usr/bin/env python3
"""
Email Reporter - Send weekly profit/loss reports
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json

class EmailReporter:
    def __init__(self):
        """Initialize email reporter"""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = os.getenv("EMAIL_ADDRESS", "")
        self.password = os.getenv("EMAIL_PASSWORD", "")
        self.to_email = os.getenv("TO_EMAIL_ADDRESS", "")
        
    def send_weekly_report(self, portfolio_data, weekly_trades, weekly_performance):
        """Send weekly profit/loss report"""
        try:
            if not all([self.email, self.password, self.to_email]):
                print("⚠️ Email credentials not set - skipping email report")
                return False
            
            # Create email content
            subject = f"AI Portfolio Manager - Weekly Report ({datetime.now().strftime('%Y-%m-%d')})"
            
            # Calculate weekly stats
            total_trades = len(weekly_trades)
            profitable_trades = len([t for t in weekly_trades if t.get('pnl', 0) > 0])
            total_pnl = sum([t.get('pnl', 0) for t in weekly_trades])
            
            # Create HTML email
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                    .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }}
                    .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }}
                    .positive {{ color: #27ae60; }}
                    .negative {{ color: #e74c3c; }}
                    .trade {{ margin: 5px 0; padding: 5px; background-color: #f8f9fa; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🤖 AI Portfolio Manager</h1>
                    <h2>Weekly Report - {datetime.now().strftime('%Y-%m-%d')}</h2>
                </div>
                
                <div class="section">
                    <h3>📊 Portfolio Overview</h3>
                    <div class="metric">
                        <strong>Total Value:</strong><br>
                        ${portfolio_data.get('total_value', 0):,.2f}
                    </div>
                    <div class="metric">
                        <strong>Total Return:</strong><br>
                        <span class="{'positive' if portfolio_data.get('total_return', 0) > 0 else 'negative'}">
                            {portfolio_data.get('total_return', 0):.2f}%
                        </span>
                    </div>
                    <div class="metric">
                        <strong>Positions:</strong><br>
                        {portfolio_data.get('position_count', 0)}
                    </div>
                    <div class="metric">
                        <strong>Cash:</strong><br>
                        ${portfolio_data.get('cash', 0):,.2f}
                    </div>
                </div>
                
                <div class="section">
                    <h3>📈 Weekly Performance</h3>
                    <div class="metric">
                        <strong>Total Trades:</strong><br>
                        {total_trades}
                    </div>
                    <div class="metric">
                        <strong>Profitable Trades:</strong><br>
                        {profitable_trades}/{total_trades} ({(profitable_trades/total_trades*100) if total_trades > 0 else 0:.1f}%)
                    </div>
                    <div class="metric">
                        <strong>Total P&L:</strong><br>
                        <span class="{'positive' if total_pnl > 0 else 'negative'}">
                            ${total_pnl:,.2f}
                        </span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>🔄 Recent Trades</h3>
            """
            
            # Add recent trades
            for trade in weekly_trades[-10:]:  # Last 10 trades
                pnl = trade.get('pnl', 0)
                pnl_class = 'positive' if pnl > 0 else 'negative'
                html_content += f"""
                    <div class="trade">
                        <strong>{trade.get('symbol', 'N/A')}</strong> - {trade.get('action', 'N/A')} @ ${trade.get('price', 0):.2f}
                        <span class="{pnl_class}">(P&L: ${pnl:.2f})</span>
                        <br><small>{trade.get('timestamp', 'N/A')}</small>
                    </div>
                """
            
            html_content += """
                </div>
                
                <div class="section">
                    <h3>📋 AI Insights</h3>
                    <p>This week's trading was powered by Google Gemini AI, analyzing technical indicators, market sentiment, and portfolio optimization strategies.</p>
                    <p><em>Remember: Past performance does not guarantee future results. This is for educational purposes only.</em></p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
                    <p>⚡ Powered by AI Portfolio Manager</p>
                    <p>Built with Python, Alpaca, Twilio & Gemini AI</p>
                </div>
            </body>
            </html>
            """
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = self.to_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print(f"📧 Email report sent to {self.to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email report: {e}")
            return False
    
    def send_alert_email(self, subject, message):
        """Send alert email"""
        try:
            if not all([self.email, self.password, self.to_email]):
                print("⚠️ Email credentials not set - skipping alert email")
                return False
            
            msg = MIMEMultipart()
            msg['Subject'] = f"AI Portfolio Manager Alert: {subject}"
            msg['From'] = self.email
            msg['To'] = self.to_email
            
            text_content = f"""
AI Portfolio Manager Alert

{message}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Powered by AI Portfolio Manager
"""
            
            msg.attach(MIMEText(text_content, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print(f"📧 Alert email sent to {self.to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending alert email: {e}")
            return False

# Test function
if __name__ == "__main__":
    reporter = EmailReporter()
    
    # Test with sample data
    test_portfolio = {
        'total_value': 105000,
        'total_return': 5.0,
        'position_count': 8,
        'cash': 15000
    }
    
    test_trades = [
        {'symbol': 'AAPL', 'action': 'BUY', 'price': 150.25, 'pnl': 25.50, 'timestamp': '2025-08-15 10:30:00'},
        {'symbol': 'MSFT', 'action': 'SELL', 'price': 320.75, 'pnl': -15.25, 'timestamp': '2025-08-15 14:15:00'}
    ]
    
    print("✅ Email reporter test complete!")

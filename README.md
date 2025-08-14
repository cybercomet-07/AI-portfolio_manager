# 🤖 AI Portfolio Manager

A simple AI-powered automated stock trading bot that uses Google Gemini AI for trading decisions and sends WhatsApp notifications.

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/cybercomet-07/AI-portfolio_manager.git
cd AI-portfolio_manager
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Copy the example file
cp env_example.txt .env

# Edit .env with your API keys
# - Alpaca API (paper trading)
# - Google Gemini API
# - Twilio WhatsApp API
```

### 4. Test the bot
```bash
python test_ai_bot.py
```

### 5. Run the bot
```bash
python ai_trading_bot.py
```

## 📋 Prerequisites

- Python 3.9+
- API Keys:
  - [Alpaca](https://app.alpaca.markets/paper/dashboard/overview) (Paper Trading)
  - [Google Gemini](https://makersuite.google.com/app/apikey)
  - [Twilio](https://console.twilio.com/) (WhatsApp)

## 🏗️ Project Structure

```
ai_trading_bot.py          # Main bot
ai_trading_engine.py       # AI decision making
portfolio_tracker.py       # Portfolio management
test_ai_bot.py            # Testing
requirements.txt          # Dependencies
```

## 🚀 Deployment

### Railway (Recommended - Free)
1. Fork this repository
2. Connect to [Railway.app](https://railway.app)
3. Set environment variables
4. Deploy!

### Other Options
- Google Cloud Run
- Render.com
- Heroku

## 📱 Features

- 🤖 AI-powered trading decisions
- 📊 Paper trading with Alpaca
- 📱 WhatsApp notifications
- 📈 Portfolio tracking
- ⚡ Automated execution

## ⚠️ Disclaimer

This is a **paper trading bot** for educational purposes. Use at your own risk.

## 📄 License

MIT License

---

**For detailed documentation, tutorials, and updates, follow me on:**
- [LinkedIn](https://linkedin.com/in/your-profile)
- [Blog](https://your-blog.com)
- [Portfolio](https://your-portfolio.com) 

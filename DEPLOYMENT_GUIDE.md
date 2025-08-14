# 🚀 AI Portfolio Manager - Deployment Guide

This guide shows you how to deploy your AI trading bot to the cloud so it runs 24/7, even when your laptop is off.

## 🌟 **Why Deploy to Cloud?**

- ✅ **24/7 Operation** - Bot runs even when your laptop is off
- ✅ **No Downtime** - Continuous trading during market hours
- ✅ **Scalable** - Can handle multiple stocks simultaneously
- ✅ **Secure** - API keys are encrypted and protected

## 📋 **Prerequisites**

Before deploying, make sure you have:
- ✅ GitHub repository: `https://github.com/cybercomet-07/AI-portfolio_manager`
- ✅ Alpaca API keys (paper trading)
- ✅ Google Gemini API key
- ✅ Twilio WhatsApp API keys

## 🚀 **Option 1: Railway (Recommended - Free)**

### Step 1: Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Click "New Project"

### Step 2: Connect GitHub Repository
1. Select "Deploy from GitHub repo"
2. Choose your repository: `cybercomet-07/AI-portfolio_manager`
3. Click "Deploy Now"

### Step 3: Set Environment Variables
1. Go to your project dashboard
2. Click on "Variables" tab
3. Add these environment variables:

```
ALPACA_API_KEY=your_alpaca_api_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
FROM_WHATSAPP_NUMBER=whatsapp:+14155238886
TO_WHATSAPP_NUMBER=whatsapp:+your_phone_number_here
MIN_CONFIDENCE=0.7
MAX_DAILY_TRADES=10
RISK_TOLERANCE=moderate
MAX_POSITION_SIZE=0.1
```

### Step 4: Deploy
1. Railway will automatically detect the `Procfile`
2. Bot will start running immediately
3. Check logs to see if it's working

## ☁️ **Option 2: Render (Alternative - Free)**

### Step 1: Create Render Account
1. Go to [Render.com](https://render.com)
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"

### Step 2: Connect Repository
1. Connect your GitHub repository
2. Select the repository: `cybercomet-07/AI-portfolio_manager`
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`

### Step 3: Set Environment Variables
1. Go to "Environment" tab
2. Add the same environment variables as Railway
3. Click "Create Web Service"

## 📱 **How WhatsApp Messages Work in Cloud**

### Before Deployment (Local)
- Bot runs on your laptop
- Uses API keys from `.env` file
- Sends messages when laptop is on

### After Deployment (Cloud)
- Bot runs on Railway/Render servers
- Uses API keys from environment variables
- Sends messages 24/7 to your WhatsApp
- You receive messages even when laptop is off

## 🔐 **Security: How API Keys Work**

### In Your GitHub Repository
```
# ❌ NO API KEYS HERE (Secure)
ALPACA_API_KEY=your_alpaca_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### In Cloud Platform Dashboard
```
# ✅ ACTUAL API KEYS HERE (Encrypted)
ALPACA_API_KEY=your_actual_alpaca_key_here
GEMINI_API_KEY=your_actual_gemini_key_here
```

## 📊 **Monitoring Your Deployed Bot**

### Railway Dashboard
1. Go to your project
2. Click "Deployments" tab
3. View real-time logs
4. Monitor bot activity

### Render Dashboard
1. Go to your web service
2. Click "Logs" tab
3. View live logs
4. Check bot status

## 🚨 **Troubleshooting**

### Bot Not Starting
- Check environment variables are set correctly
- Verify API keys are valid
- Check logs for error messages

### No WhatsApp Messages
- Verify Twilio credentials are correct
- Check WhatsApp number format
- Ensure Twilio account has credits

### API Rate Limits
- Bot includes rate limiting (5 seconds between calls)
- Monitor logs for rate limit errors
- Consider upgrading API plans if needed

## 💰 **Costs**

### Railway
- **Free tier**: 500 hours/month
- **Paid**: $5/month for unlimited

### Render
- **Free tier**: 750 hours/month
- **Paid**: $7/month for unlimited

## 🔄 **Updating Your Bot**

1. **Make changes** to your local code
2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Update bot"
   git push origin master
   ```
3. **Cloud platform automatically redeploys**
4. **No need to update API keys** (they stay in dashboard)

## 📞 **Support**

If you need help:
- Check the logs in your cloud platform dashboard
- Verify all environment variables are set
- Test locally first: `python test_ai_bot.py`

---

**🎉 Your bot will now run 24/7 and send you WhatsApp messages even when your laptop is off!**

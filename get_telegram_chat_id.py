#!/usr/bin/env python3
"""
Get Telegram Chat ID - Helper script
"""

import requests
import time

def get_chat_id():
    """Get your Telegram chat ID"""
    bot_token = "8242945520:AAHfsijFpaY2oRK95dQGVmD0VpaiOEGChlA"
    
    print("📱 Getting Telegram Chat ID")
    print("=" * 40)
    print("1. Open Telegram")
    print("2. Search for your bot: @CyberComet_AI_Bot")
    print("3. Send any message to the bot (e.g., 'Hello')")
    print("4. Wait 10 seconds...")
    
    # Wait for user to send message
    time.sleep(10)
    
    try:
        # Get updates from bot
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['ok'] and data['result']:
                # Get the latest message
                latest_message = data['result'][-1]
                chat_id = latest_message['message']['chat']['id']
                
                print(f"✅ Your Chat ID: {chat_id}")
                print(f"📝 Add this to your .env file:")
                print(f"TELEGRAM_CHAT_ID={chat_id}")
                
                return chat_id
            else:
                print("❌ No messages found")
                print("💡 Make sure you sent a message to the bot")
                return None
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    get_chat_id()

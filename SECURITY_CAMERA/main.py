import network
import urequests
import time
from machine import Pin
from machine import PWM

# Wi-Fi credentials
SSID = 'YOUR_WIFI_NAME'
PASSWORD = 'YOUR_WIFI_PASSWORD'
BOT_TOKEN = 'YOUR_TELEGRAM_CHAT_BOT_TOKEN'
CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

Trig = Pin(19, Pin.OUT, 0)
Echo = Pin(18, Pin.IN, 0)
PIEZO = PWM(Pin(15))

distance = 0
soundVelocity = 340
status = 1

last_update_id = None

def beep(frequency=2000, duration_ms=200):
    PIEZO.freq(frequency)
    for i in range(4):
        PIEZO.duty_u16(32768)
        time.sleep_ms(duration_ms)
        PIEZO.duty_u16(0)
        time.sleep_ms(duration_ms)

def getDistance(): 
    Trig.value(1) 
    time.sleep_us(10) 
    Trig.value(0) 
    while not Echo.value(): 
        pass 
    pingStart = time.ticks_us() 
    while Echo.value(): 
        pass 
    pingStop = time.ticks_us() 
    distanceTime = time.ticks_diff(pingStop, pingStart) // 2 
    distance = int(soundVelocity * distanceTime // 10000) 
    return distance 

def connect_wifi():
    print('Starting WiFi connection debug...')
    wlan = network.WLAN(network.STA_IF)
    print('WLAN object created.')
    wlan.active(True)
    print('WLAN activated.')
    print('Checking if already connected...')
    if not wlan.isconnected():
        print('Not connected. Attempting to connect to SSID:', SSID)
        try:
            wlan.connect(SSID, PASSWORD)
            print('Connect called.')
        except Exception as e:
            print('Exception during wlan.connect:', e)
            return False
        for i in range(10):
            print(f'Waiting for connection... attempt {i+1}')
            if wlan.isconnected():
                print('Connected during wait loop.')
                break
            time.sleep(1)
    else:
        print('Already connected.')

    if wlan.isconnected():
        print('Connected! IP:', wlan.ifconfig()[0])
        return True
    else:
        print('Failed to connect after attempts.')
        return False

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': text
    }

    try:
        response = urequests.post(url, json=data)
        print('Message sent!')
        print('Telegram response:', response.text)
        response.close()
    except Exception as e:
        print('Failed to send message:', e)

def execute_new_chats():
    global last_update_id, status
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        response = urequests.get(url)
        messages = response.json()
        response.close()
        if 'result' in messages and len(messages['result']) > 0:
            for update in messages['result']:
                update_id = update['update_id']
                message = update.get('message', {})
                text = message.get('text', None)
                if text and (last_update_id is None or update_id > last_update_id):
                    last_update_id = update_id
                    print(f"New chat message: {text}")

                    if text.lower() == '/status':
                        distance = getDistance()
                        status_message = f"Current distance: {distance} cm"
                        send_telegram_message(status_message)
                    elif text.lower() == '/beep':
                        beep(1000, 300)
                        send_telegram_message("Beeped!")
                    elif text.lower() == '/stop':
                        send_telegram_message("Stopping device monitoring.")
                        status = 0
                    elif text.lower() == '/start':
                        send_telegram_message("Device Monitoring Live.")
                        status = 1
                    elif text.lower() == '/help':
                        help_message = "Available commands:\n/status - Get current distance\n/beep - Make a beep sound\n/stop - Stop monitoring\n/start - Start monitoring\n/help - Show this help message"
                        send_telegram_message(help_message)
        time.sleep(2)
    except Exception as e:
        print('Failed to get messages:', e)
        time.sleep(5)

def initialize_last_update_id():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        response = urequests.get(url)
        messages = response.json()
        response.close()
        if 'result' in messages and len(messages['result']) > 0:
            last_update_id = messages['result'][-1]['update_id']
        else:
            last_update_id = None
    except Exception as e:
        print('Failed to initialize last_update_id:', e)
        last_update_id = None

def main():
    if connect_wifi():
        initialize_last_update_id()
        send_telegram_message("Connection started.")
        while True:
            execute_new_chats()
            if status == 1:
                distance = getDistance()
                if distance <= 50:
                    send_telegram_message("ALERT: Movement Detected!")
                    beep(1000, 300)
            else:
                continue

main()

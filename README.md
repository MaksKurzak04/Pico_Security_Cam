# Ultrasonic Movement Security Monitoring System with Raspberry Pi Pico 2W

A simple IoT project which alerts user of any movement in an area where device is installed using a Pi Pico 2W and ultrasonic range sensor.

## Features

- Measure Distance Using Ultrasonic Range Sensor
- Wi-Fi Connectivity for remote control and access
- Real-time monitoring with controls
- Use telegram bot for recieving and controlling device messages remotely
- Alerts user when movement detected (Telegram message sent to phone and buzzer makes noise)

## Provided Commands
- /start         (Start Device Monitoring Remotely)
- /stop          (Stop Device Monitoring Remotely)
- /beep          (Beep Device In-Person)
- /status        (Send Current Sensor Readings)
- /help          (Display What Each Command Does)

![1000024765](https://github.com/user-attachments/assets/f52ef2e1-cf62-4efa-9264-d41dd33e9726) ![1000024767](https://github.com/user-attachments/assets/fd3a3ded-bcdc-4f5b-88ce-522ec7277ff0)



## Hardware

- Pico 2W board
- Ultrasonic Range Sensor
- Piezo
- Optional breadboard
- Power Supply (usb or battery)
- Jumper wires

## Setup
For setup Official Raspberry Pi SDK in Visual Studio Code is recommended

1. Copy/Clone this project repository

2. Create Telegram Bot:
   - In Telegram app search for @BotFather
   - Create your own bot using /newbot and follow setup process
   - Get your BOT_TOKEN and CHAT_ID
       - To get Chat_id go to https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
       - look for "chat":{"id":<CHAT_ID>}

3. Update code with your credentials
   SSID = 'YOUR_WIFI_NAME'
   PASSWORD = 'YOUR_WIFI_PASSWORD'
   BOT_TOKEN = 'YOUR_TELEGRAM_CHAT_BOT_TOKEN'
   CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

4. Connect circuit as stated in code and also pictures below!
![1000024770](https://github.com/user-attachments/assets/2d6f644a-d1ab-4251-bfca-ccc19a1fd677)
![1000024769](https://github.com/user-attachments/assets/82c02e4f-891b-4642-b11f-ab6765d59485)
![1000024768](https://github.com/user-attachments/assets/1002c1ed-7ecc-4786-8b57-227ecc59342d)



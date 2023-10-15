from itertools import count
from turtle import color
from infi.systray import SysTrayIcon
from sp110e.controller import Controller
import schedule
import time
import asyncio

ble_address = '66:66:17:54:E1:C4'

colors = (
    [255, 0, 0],
    [255, 175, 0],
    [255, 255, 0],
    [175, 255, 0],
    [0, 255, 0],
    [0, 255, 175],
    [0, 255, 255],
    [0, 175, 255],
    [0, 0, 255],
    [175, 0, 255],
    [255, 0, 255],
    [255, 0, 175],
    [255, 0, 0],
    [255, 255, 255],
    [255, 255, 175],
    )

brightness = 255
colorIdx = 0

device = {}

async def brightness_up(systray):
    global brightness
    brightness = brightness + 25 if brightness + 25 <= 255 else 255
    await device.set_brightness(brightness)

async def brightness_down(systray):
    global brightness
    brightness = brightness - 25 if brightness - 25 > 0 else 0
    await device.set_brightness(brightness)

async def prev_color(systray):
    global colorIdx
    colorIdx = colorIdx - 1 if colorIdx - 1 >= 0 else len(colors) - 1
    await device.set_color(colors[colorIdx])

async def next_color(systray):
    global colorIdx
    colorIdx = colorIdx + 1 if colorIdx + 1 < len(colors) else 0 
    await device.set_color(colors[colorIdx])

async def toggle_switch(systray):
    await device.toggle()

async def turn_on():
    await device.switch_on()

menu_options = (
    ("On/Off", None, toggle_switch),
    ("Brightness Up", None, brightness_up),
    ("Brightness Down", None, brightness_down),
    ("Prev Color", None, prev_color),
    ("Next Color", None, next_color)
)
systray = SysTrayIcon("icon.ico", "LEDs", menu_options)
systray.start()

async def connect():
    global device
    print(await Controller.discover())
    device = Controller(ble_address, timeout=5, retries=1)
    await device.switch_on()
    await device.set_color([255, 0, 0])
    await device.set_brightness(255)

asyncio.run(connect())

# schedule.every().day.at("17:00").do(turn_on)

# while True:
#     schedule.run_pending()
#     time.sleep(3600)
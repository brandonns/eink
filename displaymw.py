#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont

import requests
import datetime
import pytz
import qbittorrentapi

conn_info = dict(
    host="",
    port=,
    username="",
    password="",
)
qbt_client = qbittorrentapi.Client(**conn_info)

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

headers = {"accept": "application/json"}
weathurl = ""

font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font2 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
text_color = (73, 80, 87)

resp = requests.get(weathurl)
json_weather = resp.json()

weather_status = str(json_weather['weather'][0]['id'])
weather_description = str(json_weather['weather'][0]['description'])
temp = str(round(json_weather['main']['temp']))
feels_like = str(round(json_weather['main']['feels_like']))
high = str(round(json_weather['main']['temp_max']))
low = str(round(json_weather['main']['temp_min']))
wind_speed = int(json_weather['wind']['speed'])
wind_deg = int(json_weather['wind']['deg'])
visibility = int(json_weather['visibility'])
humidity = int(json_weather['main']['humidity'])
pressure = int(json_weather['main']['grnd_level'])
utc_sunrise = int(json_weather['sys']['sunrise'])
utc_sunset = int(json_weather['sys']['sunset'])
local_tz = pytz.timezone("America/Denver")
local_sunrise = datetime.datetime.fromtimestamp(utc_sunrise, tz=pytz.utc).astimezone(local_tz)
local_sunset = datetime.datetime.fromtimestamp(utc_sunset, tz=pytz.utc).astimezone(local_tz)

try:
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    waifu_image = Image.open(os.path.join(picdir, 'waifu.bmp'))
    draw = ImageDraw.Draw(waifu_image)

    primary_weather_images = {
        '2': 'wi-day-thunderstorm.bmp',
        '3': 'wi-day-showers.bmp',
        '5': 'wi-day-rain.bmp',
        '6': 'wi-day-snow.bmp'
    }

    weather_images = {
        '800': 'wi-day-sunny.bmp',
        '801': 'wi-day-sunny-overcast.bmp',
        '802': 'wi-day-cloudy.bmp',
        '803': 'wi-cloud.bmp',
        '804': 'wi-cloudy.bmp',
        '701': 'wi-day-haze.bmp',
        '721': 'wi-day-haze.bmp',
        '711': 'wi-smoke.bmp',
        '731': 'wi-smoke.bmp',
        '741': 'wi-fog.bmp',
        '751': 'wi-sandstorm.bmp',
        '761': 'wi-dust.bmp',
        '762': 'wi-dust.bmp',
        '771': 'wi-strong-wind.bmp',
        '781': 'wi-tornado.bmp'
    }

    # Load appropriate weather image
    if weather_status in weather_images:
        weather_image = Image.open(os.path.join(picdir, weather_images[weather_status]))
    else:
        for key, image in primary_weather_images.items():
            if weather_status.startswith(key):
                weather_image = Image.open(os.path.join(picdir, image))
                break

    # Paste the weather image onto the waifu image
    waifu_image.paste(weather_image, (0, 0))  # Place at the top-left corner, adjust as needed

    # Now proceed with drawing weather data and other information
    draw.text((55, 23), 'It\'s currently ' + temp + '°F outside' if temp == feels_like else 'It\'s currently ' + temp + '°F but it feels like ' + feels_like + '°F outside', font=font1, fill=text_color, anchor='lm')
    draw.text((0, 60), 'Hi: ' + high + '°F', font=font2, fill=text_color, anchor='lm')
    draw.text((0, 80), 'Lo: ' + low + '°F', font=font2, fill=text_color, anchor='lm')
    draw.text((0, 100), weather_description.title(), font=font2, fill=text_color, anchor='lm')

    if visibility >= 10000:
        draw.text((200, 60), 'Full Visibility', font=font2, fill=text_color, anchor='lm')
    else:
        draw.text((200, 60), str(visibility) + 'm', font=font2, fill=text_color, anchor='lm')
    draw.text((200, 80), str(humidity) + '% Humidity', font=font2, fill=text_color, anchor='lm')
    draw.text((200, 100), str(pressure) + 'mb Pressure', font=font2, fill=text_color, anchor='lm')

    sunr_image = Image.open(os.path.join(picdir, 'wi-sunrise.bmp'))
    waifu_image.paste(sunr_image, (480, 40))
    draw.text((605, 65), local_sunrise.strftime('%I:%M %p'), font=font2, fill=text_color, anchor='rm')
    suns_image = Image.open(os.path.join(picdir, 'wi-sunset.bmp'))
    waifu_image.paste(suns_image, (480, 79))
    draw.text((605, 105), local_sunset.strftime('%I:%M %p'), font=font2, fill=text_color, anchor='rm')

    if int(feels_like) <= 35:
        jacket_image = Image.open(os.path.join(picdir, 'jacket.bmp'))
        waifu_image.paste(jacket_image, (725, 38))
        draw.text((722, 65), 'Bundle up', font=font2, fill=text_color, align='right', anchor='rm')
        draw.text((722, 85), 'out there!', font=font2, fill=text_color, align='right', anchor='rm')

    wind_directions = [
        (range(0, 10), 'N', 'wi-direction-up.bmp'),
        (range(10, 30), 'NNE', 'wi-direction-up-right.bmp'),
        (range(30, 60), 'NE', 'wi-direction-up-right.bmp'),
        (range(60, 80), 'ENE', 'wi-direction-up-right.bmp'),
        (range(80, 100), 'E', 'wi-direction-right.bmp'),
        (range(100, 120), 'ESE', 'wi-direction-down-right.bmp'),
        (range(120, 150), 'SE', 'wi-direction-down-right.bmp'),
        (range(150, 170), 'SSE', 'wi-direction-down-right.bmp'),
        (range(170, 190), 'S', 'wi-direction-down.bmp'),
        (range(190, 210), 'SSW', 'wi-direction-down-left.bmp'),
        (range(210, 240), 'SW', 'wi-direction-down-left.bmp'),
        (range(240, 260), 'WSW', 'wi-direction-down-left.bmp'),
        (range(260, 280), 'W', 'wi-direction-left.bmp'),
        (range(280, 300), 'WNW', 'wi-direction-up-left.bmp'),
        (range(300, 330), 'NW', 'wi-direction-up-left.bmp'),
        (range(330, 350), 'NNW', 'wi-direction-up-left.bmp'),
        (range(350, 361), 'N', 'wi-direction-up.bmp')
    ]

    for direction_range, winddir, image_file in wind_directions:
        if wind_deg in direction_range:
            winddir_image = Image.open(os.path.join(picdir, image_file))
            break

    waifu_image.paste(winddir_image, (600, 3))
    draw.text((687, 18), winddir + '@' + str(round(wind_speed)) + 'mph', font=font2, fill=text_color, align='center', anchor='mm')

    beaufort_images = [
        (range(0, 1), 'wi-wind-beaufort-0.bmp'),
        (range(1, 4), 'wi-wind-beaufort-1.bmp'),
        (range(4, 8), 'wi-wind-beaufort-2.bmp'),
        (range(8, 13), 'wi-wind-beaufort-3.bmp'),
        (range(13, 19), 'wi-wind-beaufort-4.bmp'),
        (range(19, 25), 'wi-wind-beaufort-5.bmp'),
        (range(25, 32), 'wi-wind-beaufort-6.bmp'),
        (range(32, 39), 'wi-wind-beaufort-7.bmp'),
        (range(39, 47), 'wi-wind-beaufort-8.bmp'),
        (range(47, 55), 'wi-wind-beaufort-9.bmp'),
        (range(55, 64), 'wi-wind-beaufort-10.bmp'),
        (range(64, 72), 'wi-wind-beaufort-11.bmp'),
        (range(72, 1000), 'wi-wind-beaufort-12.bmp')
    ]

    for speed_range, image_file in beaufort_images:
        if wind_speed in speed_range:
            wind_image = Image.open(os.path.join(picdir, image_file))
            break
    waifu_image.paste(wind_image, (750, 10))

    # Draw torrent information
    index = 0
    tor_index_size = 75
    torrent_startx = 375
    torrent_starty = 125
    torrent_state_startx = torrent_startx + 425
    torrent_state_starty = torrent_starty
    torrent_bar_startx = torrent_startx
    torrent_bar_starty = torrent_starty + 30

    def draw_torrent_info(torrent, index, tor_index_size, draw, font1, text_color, torrent_startx, torrent_starty, torrent_bar_startx, torrent_bar_starty, torrent_state_startx, torrent_state_starty):
        def format_seconds(seconds):
            days, seconds = divmod(seconds, 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            time_parts = []
            if days > 7:
                return ">1Wk"
            elif days == 0 and hours == 0 and minutes <= 15:
                return "Finishing Download"
            else:
                if days != 0:
                    time_parts.append(f"{days}D")
                if hours > 0:
                    time_parts.append(f"{hours}H")
                if minutes > 0:
                    time_parts.append(f"{minutes}M")
                return " ".join(time_parts) if time_parts else 'Done'

        torrent_dl = str(round((torrent.downloaded / (1024 ** 3)), 2))
        torrent_ts = str(round((torrent.size / (1024 ** 3)), 2))
        torrent_perc = str(round((torrent.downloaded / torrent.size * 100)))
        torrent_eta = format_seconds(torrent.eta)
        draw.text((torrent_startx, torrent_starty + (index * tor_index_size)), torrent.name.replace(".", " ")[:26] + '...', font=font1, fill=text_color)
        progress_bar_width = 424 * torrent.progress
        draw.rectangle((torrent_bar_startx, (torrent_bar_starty + (index * tor_index_size)), torrent_bar_startx + progress_bar_width, (torrent_bar_starty + (index * tor_index_size)) + 10), outline=text_color, fill='#9099A2')
        draw.text( (torrent_startx, (torrent_starty + (index * tor_index_size)) + 40) , torrent_dl + 'GB/' + torrent_ts + 'GB   ' + torrent_perc + '%', font=font3, fill=text_color )
        draw.text( (800, (torrent_starty + (index * tor_index_size)) + 40) , torrent_eta, font=font3, fill=text_color, anchor='ra' )
        state_labels = {
            'error': 'ERR', 'missingFiles': 'ERR', 'unknown': 'ERR',
            'downloading': 'DNL', 'forcedDL': 'DNL',
            'uploading': 'UPL', 'forcedUP': 'UPL',
            'pausedUP': 'PAU', 'pausedDL': 'PAU',
            'queuedUP': 'QUD', 'queuedDL': 'QUD',
            'stalledUP': 'STL', 'stalledDL': 'STL',
            'metaUP': 'MTA', 'metaDL': 'MTA'
        }
        torrent_state = state_labels.get(torrent.state, '')

        if torrent_state:
            draw.text((torrent_state_startx, torrent_state_starty + (index * tor_index_size)), torrent_state, font=font1, fill=text_color, anchor='ra')

    for torrent in qbt_client.torrents_info(sort='state', reverse=False):
        draw_torrent_info(torrent, index, tor_index_size, draw, font1, text_color, torrent_startx, torrent_starty, torrent_bar_startx, torrent_bar_starty, torrent_state_startx, torrent_state_starty)
        index += 1
        if index == 5:
            break

    epd.display(epd.getbuffer(waifu_image))
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()

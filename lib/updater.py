import asyncio
import datetime
from math import ceil
import random
import json
import os
import logging
from PIL import Image, ImageDraw, ImageFont
import pytz
import jdatetime
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import InputPhoto
from .library import *
from .Information import *

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

timezone = pytz.timezone('Asia/Tehran')

def get_user_bio():
    with open('settings/bio.txt', 'r') as f:
        return f.read().strip()

async def update_last_name(client):
    while True:
        try:
            with open('settings/time.txt', 'r') as f:
                option_enabled = f.read().strip() == 'True'
            with open('settings/heart.txt', 'r') as f:
                heart_enabled = f.read().strip() == 'True'
            with open('settings/mode.txt', 'r') as f:
                mode = f.read().strip()

            if option_enabled:
                current_time = datetime.datetime.now(timezone)
                rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second/60))
                current_time_str = rounded_time.strftime("%H:%M")

                if mode == 'Bold':
                    current_time_str = current_time_str.translate(str.maketrans("0123456789", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"))
                elif mode == 'Mono':
                    current_time_str = current_time_str.translate(str.maketrans("0123456789", "０１２３４５６７８９"))
                elif mode == 'Mini':
                    current_time_str = current_time_str.translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
                elif mode == 'rnd':
                    font_options = [
                        ["𝟶","𝟷","𝟸","𝟹","𝟺","𝟻","𝟼","𝟽","𝟾","𝟿"],
                        ["⓪","①","②","③","④","⑤","⑥","⑦","⑧","⑨"],
                        ["⓿","❶","❷","❸","❹","❺","❻","❼","❽","❾"]
                    ]
                    random_font = random.choice(font_options)
                    current_time_str = current_time_str.translate(str.maketrans("0123456789", "".join(random_font)))

                heart_list = ['❤️','💛','💚','💙','💜','🖤','🤍','🧡','💖','💗','💓','💞','💕','💘','💝','💟','🩵']
                heart = random.choice(heart_list)

                with open('settings/nameinfo.txt', 'r') as f:
                    user_lname = f.read()
                user_lname = user_lname.replace("time", current_time_str).replace("heart", heart)

                logging.info(f"Updating last name to: {user_lname}")
                await client(UpdateProfileRequest(last_name=user_lname))

            now = datetime.datetime.now(timezone)
            next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
            await asyncio.sleep((next_minute - now).total_seconds())
        except Exception as e:
            logging.error(f"Error in update_last_name: {e}")
            await asyncio.sleep(10)

async def update_about(client):
    while True:
        try:
            with open('settings/bioinfo.txt', 'r') as f:
                bio_info_enabled = f.read().strip() == 'True'

            if bio_info_enabled:
                with open('settings/mode.txt', 'r') as f:
                    mode = f.read().strip()

                current_time = datetime.datetime.now(timezone)
                rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second/60))
                current_time_str = rounded_time.strftime("%H:%M")
                persian_date = jdatetime.datetime.now().strftime("%Y/%m/%d")

                if mode == 'Bold':
                    table = str.maketrans("0123456789", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")
                    current_time_str = current_time_str.translate(table)
                    persian_date = persian_date.translate(table)
                elif mode == 'Mono':
                    table = str.maketrans("0123456789", "０１２３４５６７８９")
                    current_time_str = current_time_str.translate(table)
                    persian_date = persian_date.translate(table)
                elif mode == 'Mini':
                    table = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
                    current_time_str = current_time_str.translate(table)
                    persian_date = persian_date.translate(table)
                elif mode == 'rnd':
                    font_options = [
                        ["𝟶","𝟷","𝟸","𝟹","𝟺","𝟻","𝟼","𝟽","𝟾","𝟿"],
                        ["⓪","①","②","③","④","⑤","⑥","⑦","⑧","⑨"],
                        ["⓿","❶","❷","❸","❹","❺","❻","❼","❽","❾"]
                    ]
                    random_font = random.choice(font_options)
                    table = str.maketrans("0123456789", "".join(random_font))
                    current_time_str = current_time_str.translate(table)
                    persian_date = persian_date.translate(table)

                heart = random.choice(['❤️','💛','💚','💙','💜','🖤','🤍'])
                bio = get_user_bio().replace("time", current_time_str).replace("heart", heart).replace("DATE", persian_date)
                logging.info(f"Updating bio: {bio}")
                await client(UpdateProfileRequest(about=bio))

            now = datetime.datetime.now(timezone)
            next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
            await asyncio.sleep((next_minute - now).total_seconds())
        except Exception as e:
            logging.error(f"Error in update_about: {e}")
            await asyncio.sleep(10)

async def update_first_name(client):
    prev_name = ''
    while True:
        try:
            with open('settings/rnamest.txt', 'r') as f:
                rname_enabled = f.read().strip() == 'True'
            if rname_enabled:
                with open('settings/rname.txt', 'r') as f:
                    names = [n.strip() for n in f.read().split(',') if n.strip()]
                if names:
                    first_name = random.choice(names)
                    while first_name == prev_name and len(names) > 1:
                        first_name = random.choice(names)
                    logging.info(f"Updating first name to: {first_name}")
                    await client(UpdateProfileRequest(first_name=first_name))
                    prev_name = first_name
                else:
                    logging.info("No valid names found in rname.txt, skipping first name update.")
            else:
                logging.info("rnamest.txt disabled, skipping first name update.")

            now = datetime.datetime.now(timezone)
            next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
            await asyncio.sleep((next_minute - now).total_seconds())

        except Exception as e:
            logging.error(f"Error in update_first_name: {e}")
            await asyncio.sleep(10)


async def update_profile_photo(client):
    while True:
        try:
            with open('settings/timepic.txt', 'r') as f:
                option_enabled = f.read().strip() == 'True'

            if option_enabled:
                current_time = datetime.datetime.now(timezone)
                rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second/60))
                current_time_str = rounded_time.strftime("%H:%M")

                with open('settings/tpic.json', 'r') as f:
                    data = json.load(f)
                cordx, cordy, size, color_string = data['cordx'], data['cordy'], data['size'], data['color']

                with Image.open('pic/profile.jpg') as img:
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype('fonts/Freshman.ttf', size)
                    draw.text((cordx, cordy), current_time_str, fill=color_string, font=font)
                    img.save('pic/profile_modified.jpg', quality=95)

                photos = await client.get_profile_photos('me')
                if photos.total > 0:
                    input_photos = [p.as_input_photo() for p in photos]  # convert all to InputPhoto
                    await client(DeletePhotosRequest(input_photos))


                with open('pic/profile_modified.jpg', 'rb') as f:
                    uploaded_file = await client.upload_file(f)
                    await client(UploadProfilePhotoRequest(file=uploaded_file))
                    logging.info(f"Profile photo updated with time: {current_time_str}")

                if os.path.exists('pic/profile_modified.jpg'):
                    os.remove('pic/profile_modified.jpg')

            now = datetime.datetime.now(timezone)
            next_minute = (now + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
            await asyncio.sleep((next_minute - now).total_seconds())
        except Exception as e:
            logging.error(f"Error in update_profile_photo: {e}")
            await asyncio.sleep(10)

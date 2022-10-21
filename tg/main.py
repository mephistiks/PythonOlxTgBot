# утилиты
import logging
import json
# import os
# import asyncio


# телеграм
from aiogram import Bot, Dispatcher, executor, types
# import aiogram

# дб
# import db
import redis
# import asyncio_redis
import motor.motor_asyncio

from trans import ru, uz, get_trans
import trans

API_TOKEN = 'PUT UR TOKER HERE'  # test 1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

redis_host = "127.0.0.1"
redis_port = 6379

# db_url = "mongodb://localhost:27004"
db_url = "mongodb://mongo:mongo@localhost:27002"

# connection1: asyncio_redis.connection.Connection
connection2: redis.client.Redis

slots = ["language", "main", "location", "brand", "mark", "sign", "price"]

'''
await connection.set('my_key', 'my_value')
'''

db: motor.motor_asyncio.AsyncIOMotorDatabase

ban = types.ReplyKeyboardRemove()

# async def error():

home_ru = "Главное меню"
home_uz = "Asosiy menyu"

data = {
    # язык
    "language": {
        "ru": {"title": ru.lang_title,
               "keyboard": ru.lang_kb},

        "uz": {"title": ru.lang_title,
               "keyboard": ru.lang_kb}
    },
    # место где машина находится
    "location": {
        "ru": {"title": ru.location_title,
               "keyboard": ru.location_kb},

        "uz": {"title": uz.location_title,
               "keyboard": uz.location_kb},
    },
    # выбор иномарка / местный автопром
    "brand": {
        "ru": {"title": ru.country_title,
               "keyboard": ru.country_kb},

        "uz": {"title": uz.country_title,
               "keyboard": uz.country_kb},
    },
    # клава только если был выбра местный автопром
    "mark": {
        "ru": {"title": ru.mark_title,
               "keyboard": [ru.dont_mind]},

        "uz": {"title": uz.mark_title,
               "keyboard": [uz.dont_mind]},
    },
    "sign": {
        "ru": {"title": "Сумы или доллары",
               "keyboard": ["Сум", "Доллар"]},

        "uz": {"title": "Sum yoki dollar",
               "keyboard": ["Sum", "Dollar"]},
    },
    # ценник
    "price": {
        "ru": {
            "title": ru.price_title,
            "keyboard": ru.price},

        "uz": {
            "title": uz.price_title,
            "keyboard": uz.price},
    },
    # главное меню
    "main": {
        "ru": {"title": ru.home,
               "keyboard": ru.main_menu},

        "uz": {"title": uz.home,
               "keyboard": uz.main_menu},
    }
}


async def get_keyboard(name: str, lang: str = "ru"):
    global data
    title = data[name][lang]["title"]
    # print(type(keyboard))
    # keyboard: aiogram.types.ReplyKeyboardMarkup
    if data[name][lang]["keyboard"] is not None:
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        # row_btns = (types.ReplyKeyboardMarkup(text) for text in data[name][lang]["keyboard"])
        # print(row_btns)
        keyboard.add(*(types.KeyboardButton(text) for text in data[name][lang]["keyboard"]))
        print(keyboard)
    else:
        keyboard = ban
    return title, keyboard


async def send_language(_id):
    kb = {"inline_keyboard": [
        [{"text": "🇷🇺 Русский 🇷🇺", "callback_data": "ru"}, {"text": "🇺🇿 O'zbek tili 🇺🇿", "callback_data": "uz"}]]}
    await bot.send_message(chat_id=_id, text="Пожалуйста выберете язык\nTilni tanlang.", reply_markup=kb)


async def get_language(_id):
    var = await db["user"].find_one({"_id": _id})
    return var["lang"]


async def set_main_page(_id):
    lng = await get_language(_id)
    title, buttons = await get_keyboard("main", lng)
    await bot.send_message(chat_id=_id, text=title, reply_markup=buttons)


@dp.callback_query_handler(text='ru')
@dp.callback_query_handler(text='uz')
async def set_language(query: types.CallbackQuery):
    _id = query.from_user.id
    lng = query.data
    if (var := await db["user"].find_one({"_id": _id})) is not None:
        await db["user"].update_one({"_id": _id}, {"$set": {"lang": lng}})
    else:
        data = {"_id": _id, "lang": lng}
        await db["user"].insert_one(data)
    await set_main_page(_id)


@dp.message_handler(text=[ru.langs, uz.langs])
async def set_lng_btn(message: types.Message):
    await send_language(message.from_user.id)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    # await connection1.set(str(message.from_user.id), str(0))
    print(message.from_user.id)
    # print(query)
    welcome_message = "Здравствуйте, меня зовут бот Ильхом. \nSalom mening ismim bot Ilhom."
    await message.answer(welcome_message)
    await send_language(message.from_user.id)
    # main_page = "mark"
    # page = "main"
    # title, keyboard = await get_keyboard(page)
    # await message.answer(title, reply_markup=keyboard)


@dp.message_handler(text=[home_ru, home_uz])
async def main_menu_button(message: types.Message):
    await set_main_page(message.from_user.id)


@dp.message_handler(text=[ru.search, uz.search])
async def text_in_handler(message: types.Message):
    _id = message.from_user.id
    text = message.text
    if text == uz.search:
        l = "uz"
    else:
        l = "ru"
    connection2.set(str(_id), "location")
    title, buttons = await get_keyboard("location", l)
    await message.answer(title, reply_markup=buttons)


async def get_all_users_id():
    var = await db["user"].find({}, {"_id": 1}).to_list(5)
    print(var)


@dp.message_handler(commands='q')
async def test_q(*args):
    await get_all_users_id()


async def get_car_text(car: dict, lang: str = "ru"):
    l = 1 if lang == "ru" else 0
    t = ru.post if l else uz.post
    kor = ru.korob if l else uz.korob
    response = ""
    try:
        response += f"🚘{t[0]}: {car['Модель']}\n"
    except:
        pass
    try:
        response += f"💸{t[1]}: {car['price']} {car['sign']}\n"
    except:
        pass
    try:
        response += f"🏠{t[2]}: {car['addres']}\n"
    except:
        pass
    try:
        response += f"📅{t[3]}: {car['Год выпуска']}\n"
    except:
        pass
    try:
        k = kor[0 if car['Коробка передач'] == ru.korob[0] else 1]
        response += f"🎚{t[4]}: { k}\n"
    except:
        pass
    try:
        response += f"{t[5]}: {car['Пробег']}\n"
    except:
        pass
    response += "\n"
    try:
        if len(car["disc"]) > 150:
            var = car["disc"][:150] + "..."
        else:
            var = car["disc"]
        response += f"🗒{t[7]}: {var}\n"
    except:
        pass
    response += "\n"
    try:
        response += f"🌐{t[6]}: {car['link']}\n"
    except:
        pass
    return response


async def send_cars(_id: int, cnt: int = 3):
    user = await db["user"].find_one({"_id": _id})
    l = user["lang"]
    try:
        fltr = json.loads(user["filter"])
    except BaseException as e:
        fltr = None
    print(fltr)
    asset = await db["car"].find(fltr).to_list(1)
    if fltr is not None:
        var = await db["car"].aggregate([{"$match": fltr}, {"$sample": {"size": cnt - 1}}]).to_list(cnt - 1)
    else:
        var = await db["car"].aggregate([{"$sample": {"size": cnt - 1}}]).to_list(4)
    for i in var:
        asset.append(i)
    for i in asset:
        text = await get_car_text(i, l)
        url = i["image"]
        keyboard_markup = {"inline_keyboard": [[{"text": "Подробная информация", "url": i["link"]}],
                                               [{"text": "Чат", "url": "vk.com"}]]}
        await types.ChatActions.upload_photo()
        media = types.MediaGroup()
        media.attach_photo(url, text)
        await bot.send_photo(chat_id=_id, photo=url, caption=text, reply_markup=keyboard_markup)


@dp.message_handler(text=[ru.get, uz.get])
async def car_btn(message: types.Message):
    await send_cars(message.from_user.id, 10)


async def clear_user(_id):
    user = await db["user"].find_one({"_id": _id})
    new_data = {}
    new_data["_id"] = user["_id"]
    new_data["lang"] = user["lang"]
    await db["user"].delete_one({"_id": _id})
    await db["user"].insert_one(new_data)


async def get_filter(_id):
    fltr = await db["user"].find_one({"_id": _id})
    new_filter = {}
    if fltr["addres"] not in ["Весь Узбекистан", "O’zbekiston umumiy"]:
        new_filter["addres"] = fltr["addres"]
        # new_filter1.append({"addres":fltr["addres"]})
    match fltr["brand"]:
        case (ru.dont_mind | uz.dont_mind):
            pass
        case (ru.country_btn_ino | uz.country_btn_ino):
            new_filter["our"] = 0
        case (ru.country_btn_uz | uz.country_btn_uz):
            new_filter["our"] = 1
    if "mark" in fltr:
        if fltr["mark"] not in [ru.dont_mind, uz.dont_mind]:
            new_filter["Модель"] = fltr["mark"]
    # if str.lower(fltr["sign"]) in ["сум", "sum"]:
    #    new_filter["sign"] = "сум"
    # else:
    #    new_filter["sign"] = "у.е."
    '''
    if fltr["price"] not in ["Не важно", "Muhim emas"]:
        var = fltr["price"].split(" ")
        if len(var) == 2:
            new_filter["price"] = {"$and": [{"price": {"$gte": int(var[0])}}, {"price": {"$lte": int(var[1])}}]}
        elif len(var) == 1:
            q:str = var[0]
            if q.endswith("$"):
                q.replace("$", "")
                if q.startswith(">"):
                    q.replace(">", "")
                    new_filter["price"] = {"price": {"$gte": int(q)}}
                else:
                    new_filter["price"] =  {"$and": [{"price": {"$gte": int(q)-5000}}, {"price": {"$lte": int(q)}}]}
            elif type(q)==type(1):
                new_filter["price"] = {"price": {"$lte": int(q)}}
            #new_filter["price"] = {"$lte": int(var[0])}
    '''
    if fltr["price"] not in [ru.dont_mind, uz.dont_mind]:
        var: str = fltr["price"].replace("$", "")
        var = var.split("-")
        print(var)
        if len(var) == 2:
            new_filter["nprice"] = {"$gte": int(var[0]), "$lte": int(var[1])}
        elif len(var[0]) == 1:
            q: str = var[0]
            if q.startswith(">"):
                new_filter["nprice"] = {"$gte": int(q)}
            else:
                new_filter["nprice"] = {"$lte": int(q)}
        # elif type(q) == type(1):
        #    new_filter["nprice"] = {"price": {"$lte": int(q)}}
        #    # new_filter["price"] = {"$lte": int(var[0])}
    return json.dumps(new_filter)


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    text = message.text
    print(text)
    _id = message.from_user.id
    logger.debug('Кнопка %r', text)
    title: str | None = None
    keyboard: dict | None = None
    cur = connection2.get(str(message.from_user.id)).decode()
    print(f"{_id} - {cur}")
    fl = 0
    nx = cur
    match cur:
        case "location":
            await clear_user(message.from_user.id)
            to = trans.get_trans(text)
            await db["user"].update_one({"_id": _id}, {"$set": {"addres": to}})
            nx = "brand"
        case "brand":
            to = trans.get_trans(text)
            await db["user"].update_one({"_id": _id}, {"$set": {"brand": to}})
            if text in [ru.country_btn_ino, uz.country_btn_ino, ru.dont_mind, uz.dont_mind]:
                nx = "price"
            else:
                nx = "mark"
        case "mark":
            await db["user"].update_one({"_id": _id}, {"$set": {"mark": text}})
            # nx = "sign"
            nx = "price"
        case "sign":
            await db["user"].update_one({"_id": _id}, {"$set": {"sign": text}})
            nx = "price"
        case "price":
            await db["user"].update_one({"_id": _id}, {"$set": {"price": text}})
            fltr = await get_filter(_id)
            await db["user"].update_one({"_id": _id}, {"$set": {"filter": fltr}})
            await send_cars(_id=_id, cnt=10)
            fl = 1
        case _:
            message.answer("ERROR")
            fl = 1
    if fl:
        await set_main_page(_id)
        return
    q = await db["user"].find_one({"_id": message.from_user.id})
    l = q["lang"]
    title, keyboard = await get_keyboard(nx, lang=l)
    connection2.set(str(_id), nx)
    if keyboard is None:
        await message.answer(title)
    else:
        await message.answer(title, reply_markup=keyboard)


# await message.answer(reply_text, reply_markup=types.ReplyKeyboardRemove())
# with message, we send types.ReplyKeyboardRemove() to hide the keyboard

async def startup(*args):
    # global connection1
    # connection1 = await asyncio_redis.Connection.create(host=redis_host, port=redis_port)
    global connection2
    connection2 = redis.Redis(host=redis_host, port=6379)
    connection2.set("a", "b")
    print(connection2.get("a"))
    global db
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    db = client.olx
    dt = {"_id": "123", "lang": "uz"}
    # await db["user"].insert_one(dt)
    # print(await db["user"].find_one({"_id": "123"}) )
    logger.info("===================")
    logger.info("Приложение включено")
    logger.info("===================")


async def shutdown(*args):
    global connection2
    connection2.close()
    logger.info("====================")
    logger.info("Приложение выключено")
    logger.info("====================")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)

from dataclasses import dataclass

@dataclass()
class ru:
    welcome = f"Здравствуйте, меня зовут бот Ильхом. \nSalom alaykum, ismim bot Ilhom."

    home = "Главное меню"
    search = "Уточнить поиск"
    get = "Показать машины"
    langs = "Поменять язык 🇺🇿/🇷🇺"

    main_menu = [search,get,langs]

    dont_mind = "Не важно"

    lang_title = "Пожалуйста, выберете язык\nTilni tanlang."
    lang_ru = "🇷🇺 Русский 🇷🇺"
    lang_uz = "🇺🇿 O'zbek tili 🇺🇿"
    lang_kb = [lang_ru, lang_uz]

    location_title = "Выберите город/регион поиска"
    location_kb = [
        "Ташкент", "Самарканд", "Бухара", "Андижан", "Фергана", "Джизак",
        "Харезм", "Наманган", "Наваи", "Кашкадарья",
        "Сырдарья", "Сурхандарья",
        "Весь Узбекистан"
    ]

    country_title = "Вас интересует инормака или узбекский автопром?"
    country_btn_ino = "Иномарка"
    country_btn_uz = "Узбекский автопром"
    country_kb = [country_btn_uz, country_btn_ino]

    mark_title = f"Напишите, пожалуйста, какая модель Вас интересует. Например, \"Malibu\", или нажмите \"{dont_mind}\""

    price_title = f"Укажите желаемый ценовой диапазон или нажмите  \"{dont_mind}\""
    price = ["0-10000$",
             #"5000$-10000$",
             "10000$-20000$",
             #"15000$-20000$",
             ">20000$",
             dont_mind]

    post = ["Марка", "Цена", "Адрес", "Год", "Коробка передач", "Пробег", "Ссылка на источник", "Описание"]
    korob = ["Автоматическая", "Механическая"]



@dataclass()
class uz(ru):
    home = "Asosiy menyu"
    search = "Qidirish o'rnatish"
    get = "Qidiruvni takomillashtirish"
    langs = "Tilni o'zgartirish 🇺🇿/🇷🇺"

    main_menu = [search, get, langs]

    dont_mind = "Muhim emas"

    location_title = "Qidiruv shahri / mintaqasini tanlang"
    location_kb = [
        "Toshkent", "Samarqand", "Buxoro", "Andijon", "Farg’ona", "Jizzax",
        "Xorazm", "Namangan", "Navoiy", "Qashqadaryo",
        "Sirdaryo", "Surxondaryo",
        "O’zbekiston umumiy"
    ]

    country_title = "O'zbek avtosanoatimi yoki xorijiy avtomobilmi?"
    country_btn_ino = "Xorijiy avtomobil"
    country_btn_uz = "O'zbek avtosanoati"
    country_kb = [country_btn_uz, country_btn_ino]

    mark_title = f"Iltimos, qaysi model sizni qiziqtirayotganini yozing. Masalan, \"Malibu\" yoki \"{dont_mind}\" tugmasini bosing"

    price_title = f"Kerakli narx oralig'ini ko'rsating yoki \"{dont_mind}\""
    price = ["0-5000$", "5000$-10000$", "10000$-15000$", "15000$-20000$", ">20000$", dont_mind]

    post = ["Tovar", "Narx", "Manzil", "Yil", "Mashinaning xarakteristikasi", "Kilometr", "Havola", "Tavsif"]

    korob = ["Avtomatik", "Mexanik"]

def get_trans(text):
    if text in uz.location_kb:
        return ru.location_kb[uz.location_kb.index(text)]
    if text in uz.post:
        return ru.post[uz.post.index(text)]
    if text == uz.dont_mind:
        return ru.dont_mind
    if text == uz.home:
        return ru.home
    return text


data = {
    # место где машина находится
    "location": {
        "ru": {"title": "В каком регионе будем искать? ",
               "keyboard": ["Андижан", "Бухара", "Фергана", "Джизак",
                            "Харезм", "Наманган", "Наваи", "Кашкадарья",
                            "Самарканд", "Сырдарья", "Сурхандарья",
                            "Ташкент", "Весь Узбекистан"]},

        "uz": {"title": "Пожалуйста выберете язык\nTilni tanlang.",
               "keyboard": ["Andijon", "Buxoro", "Farg’ona", "Jizzax",
                            "Xorazm", "Namangan", "Navoiy", "Qashqadaryo",
                            "Samarqand", "Sirdaryo", "Surxondaryo",
                            "Toshkent", "O’zbekiston umumiy"]},
    },
    # выбор иномарка / местный автопром
    "brand": {
        "ru": {"title": "Узбекский автопром или иномарка?",
               "keyboard": ["Иномарка", "Узбекский автопром", "Не важно"]},

        "uz": {"title": "O'zbek avtosanoatimi yoki xorijiy avtomobilmi?",
               "keyboard": ["Xorijiy avtomobil", "O'zbek avtosanoati", "Muhim emas"]},
    },
    # клава только если был выбра местный автопром
    "mark": {
        "ru": {"title": "Напишите пожалуйста какая модель вас интересует."
                        " Например Малибу 2. Если желаете, чтобы я сам выбрал и скинул Вам объявления нажммте кнопку Любой",
               "keyboard": ["Любой"]},

        "uz": {"title": "Qaysi modelga qiziqqaningizni yozing. Masalan, Malibu 2."
                        " Agar siz meni tanlashim boyicha sizga e’lonlarni yuborishimni hohlasangiz Har Qanday so'zini yozing.",
               "keyboard": ["Har Qanday"]},
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
            "title": "Введите ценовой диапазон через пробел, либо только одно число, чтобы указать верхнюю границу. Например: 1000 15000",
            "keyboard": ["5000$", "10000$", "15000$", "20000$", ">20000$", "Не важно"]},

        "uz": {
            "title": "Minimal va maksimal miqdorni bo'sh joy bilan ajratib yozing yoki maksimal miqdorni topish uchun bitta raqamni yozing. Masalan: 1000 15000",
            "keyboard": ["5000$", "10000$", "15000$", "20000$", ">20000$", "UZ Не важно"]},
    },
    # главное меню
    "main": {
        "ru": {"title": "Главное меню",
               "keyboard": ["Настроить поиск", "Показать машины", "Поменять язык 🇺🇿/🇷🇺"]},

        "uz": {"title": "Asosiy menyu",
               "keyboard": ["Qidirish o'rnatish", "UZ Показать машины", "Tilni o'zgartirish 🇺🇿/🇷🇺"]},
    }

}

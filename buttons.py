from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def welcome_buttons() -> InlineKeyboardMarkup:
    problem_butt = InlineKeyboardButton(text='Сообщить о проблемме', callback_data='problem1')
    guide_butt = InlineKeyboardButton(text='Как правилно сфотографироваться', callback_data='guide')
    markup = InlineKeyboardMarkup()
    markup.add(problem_butt, guide_butt)
    return markup


def address_buttons() -> InlineKeyboardMarkup:
    sbs = InlineKeyboardMarkup(text='МФЦ на Уральской 79/6 (СБС)', callback_data='address_SBS', row_width=2)
    zipovskaya = InlineKeyboardButton(text='МЦФ на Зиповской 5', callback_data='address_zipovskaya', row_width=2)
    dzerzhinskogo = InlineKeyboardButton(text='МФЦ на Дзержинского 100 (ТЦ Красная Площадь)',
                                         callback_data='address_dzerzhinskogo', row_width=2)
    krasnaya = InlineKeyboardButton(text='МФЦ на Красной 176 (ТЦ Красная Площадь)', callback_data='address_krasnaya',
                                    row_width=2)
    markup = InlineKeyboardMarkup()
    markup.add(sbs)
    markup.add(dzerzhinskogo)
    markup.row(krasnaya)
    markup.row(zipovskaya)
    return markup


def problems(address: str) -> InlineKeyboardMarkup:
    photo_not_working = InlineKeyboardButton(text="Фотокабинка не работает",
                                             callback_data='not_working_'+address)
    photo_lines = InlineKeyboardButton(text="На фотографии полосы, смазанная краска",
                                       callback_data='photos_lines_'+address)
    stupid = InlineKeyboardButton(text="Не понимаю как сфоторафироваться",
                                  callback_data='guide')
    markup = InlineKeyboardMarkup()
    markup.add(photo_lines)
    markup.add(photo_not_working)
    markup.add(stupid)
    return markup

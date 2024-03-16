import logging
from aiogram import Bot, executor
from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from buttons import welcome_buttons, address_buttons, problems
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class BadPhotos(StatesGroup):
    order_numb = State()
    photos = State()


state_address = {
    "SBS": "МФЦ на Уральской 79/6 (СБС)",
    "zipovskaya": "МЦФ на Зиповской 5",
    "dzerzhinskogo": "МФЦ на Дзержинского 100 (ТЦ Красная Площадь)",
    "krasnaya": "МФЦ на Красной 176 (ТЦ Красная Площадь)"
}


async def welcome(message: types.Message):
    await message.answer('Вас приветсвует техническая поддержка NanoPhoto', reply_markup=welcome_buttons())


async def guide(callback: types.CallbackQuery):
    await callback.message.edit_text('''⚡️⚡️ПОШАГОВАЯ ИНСТРУКЦИЯ ПО РАСПЕЧАТКЕ ФОТО ⚡️⚡️

1️⃣Выберите формат фотографии из списка. ⚠️Если Вы носите очки🧐 - для фотографии их лучше снять (будут блики на стекле). Дополнительные требования (религиозная одежда и т.п.) уточните у администраторов на стойке. 

2️⃣Сядьте ровно. Поднимите/опустите стул или подвиньтесь влево/вправо при необходимости. 
Нажмите кнопку «Сделать фото»📸  и в течение 3 секунд смотрите ровно перед собой в объектив фотоаппарата. 

3️⃣Отрегулируйте фото по красным линиям 🙎‍♂️, согласно подсказкам на экране терминала. ⚠️В случае, если линии выставлены выше/ниже лица фотография может получиться не по нормативам.

4️⃣Если фотография Вас не устроила, нажмите кнопку «Назад» и сфотографируйтесь заново.

5️⃣Убедитесь, что фотография полностью Вас устраивает и нажмите кнопку «Далее». Печать 🖨 фотографий начнется сразу после оплаты.

6️⃣Для оплаты по карте нажмите на изображение банковской карты💳. Оплатите услугу бесконтактным способом используя банковскую карту или смартфон с NFC модулем🚀
\n Для того чтобы вернуться в начало отправте /start''')


async def choose_address(callback: types.CallbackQuery):
    await callback.message.edit_text('''С какой фотокабиной возникли у Вас проблемы?''',
                                     reply_markup=address_buttons())


async def what_problem(callback: types.CallbackQuery):
    address = callback.data.split("_")[1]
    await callback.message.edit_text("Какая проблема у вас возникла?", reply_markup=problems(address))


async def not_working(callback: types.CallbackQuery):
    address = callback.data.split("_")[2]
    await callback.message.edit_text(
        "Благодарим за обращение! С Вами свяжутся в течении 5 минут для уточнения информации. "
        "\nДля того чтобы вернуться в начало отправте /start")
    await bot.send_message("-4181490818", "#Break \nПоступило обращение от пользвователя @"
                           + callback.from_user.username + "\nАдресс кабинки: "
                           + state_address[address])


async def photo_lines_one(callback: types.CallbackQuery):
    await BadPhotos.order_numb.set()
    await callback.message.edit_text("Отправте номер заказа, или дату и времня оплаты пример (12.01 13:00)")


async def photo_lines_two(message: types.Message, state: FSMContext):
    await BadPhotos.photos.set()
    await state.update_data(order_numb=message.text)
    await message.answer("Отправте фото бракованных фотографий")


async def photo_lines_three(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        order_numb = await state.get_data()
        await message.answer("Благодарим за обращение! Проанализируем информацию и свяжемся с вами для возврата "
                             "денежных средств!"
                             "\nДля того чтобы вернуться в начало отправте /start")
        await bot.send_photo(-4181490818, photo.file_id,
                             caption=("#BadPrint номер заказа: <blockquote>" + order_numb['order_numb'] +
                                      "</blockquote>\nот пользователя @" + message.from_user.username),
                             parse_mode='HTML'
                             )
        await state.reset_state()
        await state.reset_data()
    else:
        await message.answer("Нужно отправить фотографию, или нажмите /start чтобы вернуться в начало")


def main_routers(dp: Dispatcher):
    dp.register_message_handler(welcome, commands=["start"])
    dp.register_callback_query_handler(guide,
                                       lambda callback_query: callback_query.data == "guide",
                                       state="*")
    dp.register_callback_query_handler(choose_address,
                                       lambda callback_query: callback_query.data == "problem1",
                                       state="*")
    dp.register_callback_query_handler(what_problem,
                                       lambda callback_query: callback_query.data.startswith("address_"),
                                       state="*")
    dp.register_callback_query_handler(not_working,
                                       lambda callback_query: callback_query.data.startswith("not_working"),
                                       state="*")
    dp.register_callback_query_handler(photo_lines_one,
                                       lambda callback_query: callback_query.data.startswith("photos_lines_"),
                                       state="*")
    dp.register_message_handler(photo_lines_two,
                                state=BadPhotos.order_numb)
    dp.register_message_handler(photo_lines_three,
                                content_types=types.ContentType.PHOTO,
                                state=BadPhotos.photos)


main_routers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

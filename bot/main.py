import asyncio
import os
import logging
import requests
import subprocess
import datetime
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from vosk import Model, KaldiRecognizer, SetLogLevel
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import asyncio
import os
import logging
import requests
import speech_recognition as sr
import subprocess
import datetime
from aiogram.types import Message, FSInputFile
from aiogram import Bot, Dispatcher, Router, types
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import json
import wave
from pymorphy2 import MorphAnalyzer
import time
import wave
import torch
import numpy as np
import simpleaudio as sa
from transliterate import translit
from num2words import num2words
import re
#from pydub import AudioSegment
from number import NUMBER
from natasha.extractors import Extractor
from yargy.parser import Match



# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
token = '7775459260:AAHwxOYCvJvpcnN8tQr9qqq9L1SVtlTxHa4'
bot = Bot(token=token)
dp = Dispatcher()
router = Router()
model = Model("model/vosk-model-small-ru-0.22")


# Файл для логов
logfile = str(datetime.date.today()) + '.log'

class Form(StatesGroup):
    joinHowClient = State()
    get_dogovor = State()
    end = State()
    get_phone = State()
    get_adress = State()
    createNew = State()
    joinBot = State()

def api_keywords(l: list):
    response = requests.get("http://localhost:8000/api/intents")

    data = response.json()

    # Функция для подсчета совпадений
    def count_matches(keywords, search_list):
        keywords_list = keywords.split(', ')
        return sum(1 for keyword in keywords_list if keyword in search_list)

    # Инициализируем переменные для хранения максимального количества совпадений и соответствующего ответа
    max_matches = 0
    best_response = None

    # Проходим по каждому элементу в JSON-ответе
    for item in data:
        matches = count_matches(item['keywords'], l)
        if matches > max_matches:
            max_matches = matches
            best_response = item['response_text']

    # Выводим ответ с наибольшим количеством совпадений
    if best_response:
        return best_response
    else:
        return "Прошу прощения, но мы не смогли распознать то, что вы имели ввиду"



def audio_to_text(audio_path: str):
    """Функция для перевода аудио в текстовую форму."""
    SetLogLevel(0)

    with open(audio_path, "rb") as wf:
        rec = KaldiRecognizer(model, 16000)  # Уменьшаем частоту дискретизации до 16000 Гц
        rec.SetWords(True)

        result = ""
        while True:
            data = wf.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                #result = rec.Result()
                print("...")
            else:
                print("...")
                #result = rec.PartialResult()

        result = rec.FinalResult()
    return result

@router.message(Command("start"))
async def get_audio_messages(message: types.Message):
    class NeuralSpeaker:
        def __init__(self):
            print('Initializing neural model')
            start = time.time()
            device = torch.device('cpu')
            torch.set_num_threads(4)
            local_file = 'model.pt'
            if not os.path.isfile(local_file):
                torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                            local_file)
            self.__model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
            self.__model.to(device)
            end = time.time()
            print(f'Model ready in {round(end - start, 2)} seconds')

        @staticmethod
        def __num2words_ru(match):
            clean_number = match.group().replace(',', '.')
            return num2words(clean_number, lang='ru')

        # Speakers available: aidar, baya, kseniya, xenia, eugene, random
        # Speaker could be set in message using !1, !2 and alike starting chars
        def speak(self, words, speaker, save_file, sample_rate):
            words = translit(words, 'ru')
            words = re.sub(r'-?[0-9][0-9,._]*', self.__num2words_ru, words)
            print(f'text after translit and num2words {words}')
            if len(words) > 3:
                possible_speaker = words[0:2]
            else:
                return
            match possible_speaker:
                case '!1':
                    speaker = 'aidar'
                case '!2':
                    speaker = 'baya'
                case '!3':
                    speaker = 'ksenia'
                case '!4':
                    speaker = 'xenia'
                case '!5':
                    speaker = 'eugene'
                case '!0':
                    speaker = 'random'
            # Текст который будет озвучен
            example_text = f'{words}'
            if sample_rate not in [48000, 24000, 8000]:
                sample_rate = 48000
            if speaker not in ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']:
                speaker = 'xenia'
            # Эта функция сохраняет WAV на диск
            # model.save_wav(text=example_text,
            #                speaker=speaker,
            #                sample_rate=sample_rate)
            #
            # Эта часть запускает аудио на колонках.
            start = time.time()
            print(f'Model started')
            try:
                audio = self.__model.apply_tts(text=example_text,
                                            speaker=speaker,
                                            sample_rate=sample_rate, )
            except ValueError:
                print('Bad input')
                return
            end = time.time()
            time_elapsed = round(end - start, 2)
            print(f'Model applied in {time_elapsed} seconds')
            audio = audio.numpy()
            audio *= 32767 / np.max(np.abs(audio))
            audio = audio.astype(np.int16)
            wave_obj = sa.WaveObject(audio, 1, 2, sample_rate)
            if not save_file:
                play_obj = wave_obj.play()
                play_obj.wait_done()
                return time_elapsed
            else:
                return wave_obj.audio_data

    speaker = NeuralSpeaker()
    audio_data = speaker.speak(f"Здравствуйте {message.from_user.first_name}", speaker='xenia', save_file=True, sample_rate=48000)
    print("1")
    with wave.open("output.wav", "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(48000)
        wav_file.writeframes(audio_data)
    voice_file_path = 'output.wav'
    print("okey!")
    
    builder = InlineKeyboardBuilder()
    
    # Кнопка слева
    button_left = InlineKeyboardButton(text="Войти как клиент ТТК", callback_data="joinHowClient")
    
    # Кнопка справа
    button_right = InlineKeyboardButton(text="Заключить новый договор", callback_data="createNew")
    
    # Кнопка снизу
    button_bottom = InlineKeyboardButton(text="Показать текстом", callback_data="hello-go-text")
    
    # Добавление кнопок в строки
    builder.row(button_left, button_right)
    builder.row(button_bottom)
    
    chat_id = message.chat.id
    chat_id = str(chat_id)
    await bot.send_voice(chat_id=chat_id, voice=FSInputFile(
        path=os.path.join('output.wav')), reply_markup=builder.as_markup())
    os.remove(voice_file_path)
    
@router.callback_query(lambda query: query.data == 'createNew')
async def subtract_two(callback: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.answer_callback_query(callback.id, text="Введите свой номер телефона:")
    await state.set_state(Form.get_phone)

@router.callback_query(Form.createNew)
async def subtract_two(message: types.Message, state: FSMContext):
    await message.answer("Введите свой номер телефона:")
    await state.set_state(Form.get_phone)

@router.message(Form.get_phone)
async def subtract_two(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    phone = user_data['phone']
    await message.answer("Введите адрес для подключения услуги:")
    await state.set_state(Form.get_adress)

@router.message(Form.get_adress)
async def subtract_two(message: types.Message, state: FSMContext):
    await state.update_data(adress=message.text)
    user_data = await state.get_data()
    adress = user_data['adress']
    phone = user_data['phone']
    #post запрос на сервер
    await state.set_state(Form.joinBot)

@router.callback_query(lambda query: query.data == 'joinHowClient')
async def subtract_two(callback: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer("Введите номер договора:")
    await state.set_state(Form.get_dogovor)

@router.callback_query(Form.joinHowClient)
async def subtract_two(message: types.Message, state: FSMContext):
    await message.answer("Введите номер договора:")
    await state.set_state(Form.get_dogovor)

@router.message(Form.get_dogovor)
async def subtract_two(message: types.Message, state: FSMContext):
    number_dogovor = message.text
    len_number_dogovor = len(number_dogovor)
    number_dogovor = number_dogovor
    number_dogovor[0]
    number_dogovor[1]
    number_dogovor[2]
    if len_number_dogovor == 9:
        if number_dogovor[0] == '5':
            if number_dogovor[1] == '1':
                if number_dogovor[2] == '6':
                    print({number_dogovor})
                    #post запрос на бэк
                    await message.answer("Успешно!")
                    await message.answer("Список тарифов:\nМаксимальный - 1000 Гбит 800р в месяц\nМощный - 100 Мбит 400р в месяц\nЧестный - 10 Мбит 100р в месяц\nСписок услуг:\nАнтиВирус Касперский - 100р в месяц\nВыделенный IP - 100р в месяц\nПерсональный менеджер - 100р в месяц\nФирменный роутер - 100р в месяц")
            
                else:
                    await message.answer("Неправильный номер договора. Попробуйте заново")
                    await state.set_state(Form.joinHowClient)
            else:
                await message.answer("Неправильный номер договора. Попробуйте заново")
                await state.set_state(Form.joinHowClient)
        else:
            await message.answer("Неправильный номер договора. Попробуйте заново")
            await state.set_state(Form.joinHowClient)
    else:
        await message.answer("Неправильный номер договора. Попробуйте заново")
        await state.set_state(Form.joinHowClient)

@router.message(F.voice)
async def get_audio_messages(message: types.Message, bot: Bot):
    """Основная функция, которая принимает голосовое сообщение от пользователя."""
    try:
        print("Started recognition...")
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        # Получаем информацию о файле
        file_info = await bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        fname = os.path.basename(file_path).split('.')[0]  # Имя файла без расширения

        # Скачиваем голосовое сообщение
        doc = requests.get(f'https://api.telegram.org/file/bot{token}/{file_path}')
        with open(f'{fname}.oga', 'wb') as f:
            f.write(doc.content)

        # Конвертируем .oga в .wav с уменьшенной частотой дискретизации
        subprocess.run(['ffmpeg', '-i', f'{fname}.oga', '-ar', '16000', f'{fname}.wav'])

        # Переводим аудио в текст
        result = audio_to_text(f'{fname}.wav')
        
        # Проверяем, что результат не пустой
        if result:
            print(result)
            #await bot.send_voice()
            json_data = result
            data = json.loads(json_data)
            result = data['text']
            class NumberExtractor(Extractor):
                def __init__(self):
                    super(NumberExtractor, self).__init__(NUMBER)

                def replace(self, text):
                    """
                    Замена чисел в тексте без их группировки

                    Аргументы:
                        text: исходный текст

                    Результат:
                        new_text: текст с замененными числами
                    """
                    if text:
                        new_text = ""
                        start = 0

                        for match in self.parser.findall(text):
                            if match.fact.multiplier:
                                num = match.fact.int * match.fact.multiplier
                            else:
                                num = match.fact.int
                            new_text += text[start: match.span.start] + str(num)
                            start = match.span.stop
                        new_text += text[start:]

                        if start == 0:
                            return text
                        else:
                            return new_text
                    else:
                        return None
                
                def replace_groups(self, text):
                    """
                    Замена сгруппированных составных чисел в тексте

                    Аргументы:
                        text: исходный текст

                    Результат:
                        new_text: текст с замененными числами
                    """
                    if text:
                        start = 0
                        matches = list(self.parser.findall(text))
                        groups = []
                        group_matches = []

                        for i, match in enumerate(matches):
                            if i == 0:
                                start = match.span.start
                            if i == len(matches) - 1:
                                next_match = match
                            else:
                                next_match = matches[i + 1]
                            group_matches.append(match.fact)
                            if text[match.span.stop: next_match.span.start].strip() or next_match == match:
                                groups.append((group_matches, start, match.span.stop))
                                group_matches = []
                                start = next_match.span.start
                        
                        new_text = ""
                        start = 0

                        for group in groups:
                            num = 0
                            nums = []
                            new_text += text[start: group[1]]
                            for match in group[0]:
                                curr_num = match.int * match.multiplier if match.multiplier else match.int
                                if match.multiplier:
                                    num = (num + match.int) * match.multiplier
                                    nums.append(num)
                                    num = 0
                                elif num > curr_num or num == 0:
                                    num += curr_num
                                else:
                                    nums.append(num)
                                    num = 0
                            if num > 0:
                                nums.append(num)
                            new_text += str(sum(nums))
                            start = group[2]
                        new_text += text[start:]

                        if start == 0:
                            return text
                        else:
                            return new_text
                    else:
                        return None
            text = result
            extractor = NumberExtractor()

            for match in extractor(text):
                print(match.fact)

            print(extractor.replace(text))
            result = extractor.replace_groups(text)            
            morph = MorphAnalyzer()
            words = result.split()
            lemmatized_words = [morph.parse(word)[0].normal_form for word in words]
            result = ' '.join(lemmatized_words)
            result = result.split()
            result = api_keywords(result)
            await message.answer(result)
        else:
            await message.answer("Прошу прощения, но сообщение пустое...")
            with open(logfile, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.datetime.today().strftime('%H:%M:%S')}:{message.from_user.id}:{message.from_user.first_name}_{message.from_user.last_name}:{message.from_user.username}:{message.from_user.language_code}:Message is empty.\n")
    except Exception as e:
        print(e)
        await message.answer("Произошла техническая ошибка -> @egprog")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.datetime.today().strftime('%H:%M:%S')}:{message.from_user.id}:{message.from_user.first_name}_{message.from_user.last_name}:{message.from_user.username}:{message.from_user.language_code}:{str(e)}\n")
    finally:
        os.remove(f'{fname}.wav')
        os.remove(f'{fname}.oga')

# Регистрируем роутер в диспетчере
async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
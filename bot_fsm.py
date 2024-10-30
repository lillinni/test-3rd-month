from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database

db = Database('database.db')

class HomeworkForm(StatesGroup):
    name = State()
    group_name = State()
    homework_number = State()
    github_link = State()

bot_fsm_router = Router()

@bot_fsm_router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я помогу тебе отправить домашнее задание. Введи свое имя.")
    await state.set_state(HomeworkForm.name)

@bot_fsm_router.message(HomeworkForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    kb = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="Python 46-01"), types.KeyboardButton(text="Python 46-02")],
        [types.KeyboardButton(text="Python 47-01"), types.KeyboardButton(text="Python 47-02")]
    ], resize_keyboard=True)
    await message.answer("Выбери свою группу:", reply_markup=kb)
    await state.set_state(HomeworkForm.group_name)

@bot_fsm_router.message(HomeworkForm.group_name)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    await message.answer("Теперь введите номер домашнего задания (от 1 до 8):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(HomeworkForm.homework_number)

@bot_fsm_router.message(HomeworkForm.homework_number)
async def process_homework_number(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 8:
        await state.update_data(homework_number=int(message.text))
        await message.answer("Теперь введите ссылку на GitHub репозиторий:")
        await state.set_state(HomeworkForm.github_link)
    else:
        await message.answer("Пожалуйста, введите номер домашнего задания от 1 до 8")

@bot_fsm_router.message(HomeworkForm.github_link)
async def process_github_link(message: types.Message, state: FSMContext):
    if message.text.startswith("https://github.com"):
        await state.update_data(github_link=message.text)
        
        data = await state.get_data()
        
        save_homework(data['name'], data['group_name'], data['homework_number'], data['github_link'])
        
        await message.answer(f"Домашнее задание принято!\n"
                             f"Имя: {data['name']}\n"
                             f"Группа: {data['group_name']}\n"
                             f"Номер ДЗ: {data['homework_number']}\n"
                             f"GitHub: {data['github_link']}")
        await state.clear()
    else:
        await message.answer("Ссылка должна начинаться с 'https://github.com'. Попробуйте снова")

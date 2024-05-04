from aiogram import Bot, Dispatcher, types, Router, F, enums
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from dotenv import load_dotenv
from os import environ
from sys import stdout

import logging
import asyncio
from functions import get_tasks, create_task, add_user, clear_task_list, check_user

load_dotenv()

class AddTask(StatesGroup):
    add_title = State()
    add_text = State()

router = Router()
dp = Dispatcher()



@router.message(CommandStart())
async def start_command(msg: types.Message):
    await msg.answer("Добро пожаловать! Чтобы добавить задачу - нажмите на кнопку /add. Чтобы посмотреть список задач - нажмите /tsk. Чтобы очистить список задач напишите /clear")
    user = await check_user(msg.from_user.id)
    if not user:
        await add_user(msg.from_user.id)
@router.message(Command("add"))
async def add_task(msg: types.Message, state: FSMContext):
    await msg.answer("Введите название задачи:")
    await state.set_state(AddTask.add_title)

@router.message(AddTask.add_title, F.text)
async def title_input(msg: types.Message, state: FSMContext):
    title = msg.text
    if len(title) > 250:
        await msg.answer("Максимальная длина заголовка - 250 символов! Более подробно задачу расписать вы сможете позже. Введите задачу ещё раз: ")
    else:
        await state.update_data(title=title)
        await state.set_state(AddTask.add_text)
        await msg.answer("Введите подробное описание задачи(опционально, пропишите /next, если не хотите добавлять): ")

@router.message(AddTask.add_text, Command("next"))
async def skip_text_input(msg: types.Message, state: FSMContext):
    await accept_text(msg, state, "")

@router.message(AddTask.add_text, F.text)
async def text_input(msg: types.Message, state: FSMContext):
    await accept_text(msg, state, msg.text)

async def accept_text(msg: types.Message, state: FSMContext, description: str):
    data = await state.get_data()
    title = data.get("title")
    await create_task(user_id=msg.from_user.id, task_title=title, task_description=description)
    await msg.answer("Задача успешно создана!")
    await state.clear()

@router.message(Command("tsk"))
async def get_task_list(msg: types.Message):
    all_tasks = await get_tasks(msg.from_user.id)
    if all_tasks.get("error"):
        await msg.answer("Что-то пошло не так! Попробуйте ещё раз")
    elif not all_tasks:
        await msg.answer("Ваш список пуст!")
    else:
        output = "\n\n".join([f"{i+1}) <b>{k}</b>\n{v}" for i, (k, v) in enumerate(all_tasks.items())])
        await msg.answer(output, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)

@router.message(Command("clear"))
async def cleat_list(msg: types.Message):
    await clear_task_list(msg.from_user.id)
    await msg.answer("Список успешно очищен!")

@router.message(F.text)
async def check_added_user(msg: types.Message):
    await check_user(msg.from_user.id)


async def main():
    bot = Bot(environ.get("BOT_TOKEN"))
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=stdout)
    asyncio.run(main())
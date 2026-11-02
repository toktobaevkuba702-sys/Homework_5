from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards import start_keyboard, restart_keyboard
from questions import QUESTIONS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}, я твой бот!"
    )


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "Я бот, созданный на Python с помощью aiogram!"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start — запуск бота\n"
        "/help — список команд\n"
        "/about — информация о боте",
        reply_markup=start_keyboard
    )


@router.message(F.text.lower() == "пока")
async def cmd_bye(message: Message):
    await message.answer("Пока! До встречи 👋")


class Quiz(StatesGroup):
    playing = State()


@router.message(F.text == "🎮 Начать игру")
async def start_quiz(message: Message, state: FSMContext):
    await state.set_state(Quiz.playing)

    await state.update_data(
        question_index=0,
        score=0
    )

    await message.answer(
        f"Вопрос 1: {QUESTIONS[0]['q']}"
    )


@router.message(F.text == "🔄 Играть снова")
async def restart_quiz(message: Message, state: FSMContext):
    await state.set_state(Quiz.playing)

    await state.update_data(
        question_index=0,
        score=0
    )

    await message.answer(
        f"Вопрос 1: {QUESTIONS[0]['q']}"
    )


@router.message(Quiz.playing)
async def check_answer(message: Message, state: FSMContext):
    if not message.text:
        return

    data = await state.get_data()

    question_index = data["question_index"]
    score = data["score"]

    correct_answer = QUESTIONS[question_index]["a"]

    if message.text.strip().lower() == correct_answer.strip().lower():
        score += 1
        await message.answer("Правильно! +1 ⭐")
    else:
        await message.answer(
            f"Неверно. Правильный ответ: {correct_answer}"
        )

    question_index += 1

    await state.update_data(
        question_index=question_index,
        score=score
    )

    if question_index < len(QUESTIONS):
        await message.answer(
            f"Вопрос {question_index + 1}: "
            f"{QUESTIONS[question_index]['q']}"
        )
    else:
        await message.answer(
            f"Викторина завершена! Твой результат: "
            f"{score}/{len(QUESTIONS)}",
            reply_markup=restart_keyboard
        )
        await state.clear()
    

@router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)
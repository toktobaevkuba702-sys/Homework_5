
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import update_user, delete_user
from keyboards import start_keyboard, restart_keyboard
from questions import QUESTIONS

router = Router()


# СОСТОЯНИЯ
class Quiz(StatesGroup):
    playing = State()


class UpdateUser(StatesGroup):
    waiting_for_data = State()


class DeleteUser(StatesGroup):
    waiting_for_id = State()


# START
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {message.from_user.full_name}, я твой бот!"
    )


# ABOUT
@router.message(Command("about"))
async def cmd_about(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Я бот, созданный на Python с помощью aiogram!"
    )


# HELP
@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "/start — запуск бота\n"
        "/help — список команд\n"
        "/about — информация о боте\n"
        "/update — изменить пользователя\n"
        "/delete — удалить пользователя\n"
        "/cancel — отменить действие",
        reply_markup=start_keyboard
    )


# CANCEL
@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Текущее действие отменено. Можешь продолжать пользоваться ботом."
    )


# UPDATE
@router.message(Command("update"))
async def cmd_update(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(UpdateUser.waiting_for_data)

    await message.answer(
        "Введите данные в формате: ID, новое имя, новый возраст\n"
        "Например: 1, Kuba, 19"
    )


@router.message(UpdateUser.waiting_for_data)
async def process_update(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Отправь текстовые данные.")
        return

    try:
        user_id, new_name, new_age = message.text.split(",")

        user_id = int(user_id.strip())
        new_name = new_name.strip()
        new_age = int(new_age.strip())

        if not new_name or new_age < 0:
            raise ValueError

        result = update_user(user_id, new_name, new_age)

        if result:
            await message.answer("Данные пользователя обновлены!")
        else:
            await message.answer("Пользователь с таким ID не найден.")

        await state.clear()

    except ValueError:
        await message.answer(
            "Неверный формат! Используй: ID, имя, возраст"
        )


# DELETE
@router.message(Command("delete"))
async def cmd_delete(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DeleteUser.waiting_for_id)

    await message.answer(
        "Введи ID пользователя, которого нужно удалить:"
    )


@router.message(DeleteUser.waiting_for_id)
async def process_delete(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Отправь числовой ID.")
        return

    try:
        user_id = int(message.text.strip())

        result = delete_user(user_id)

        if result:
            await message.answer("Пользователь успешно удалён!")
        else:
            await message.answer("Пользователь с таким ID не найден.")

        await state.clear()

    except ValueError:
        await message.answer("Введи корректный числовой ID!")


# GOODBYE
@router.message(F.text.lower() == "пока")
async def cmd_bye(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Пока! До встречи 👋")


# START QUIZ
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


# RESTART QUIZ
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


# QUIZ ANSWERS
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


# ECHO
@router.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)

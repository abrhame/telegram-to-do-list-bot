import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart




TOKEN = "your token"

dp = Dispatcher()

to_do_list = []

# commands
@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Hello, This is your to do list bot")
    await message.answer("Available commands:\n"
                         "/add - add new task\n"
                         "/show - show all tasks\n"
                         "/compelete - mark task as completed\n"
                         "/delete - delete a task\n"
                         )
    
@dp.message(Command("add"))
async def add_task(message: Message) -> None:
    if len(message.text) < 6:
        await message.answer("Please enter a task to add.")
        return

    task_text = message.text.split(" ", 1)[1]
    to_do_list.append(task_text + " (Incomplete)")
    await message.answer(f"Task added: {task_text}")


@dp.message(Command("show"))
async def show_tasks(message: Message) -> None:
    if len(to_do_list) == 0:
        await message.answer("You have no tasks")
        return
    
    tasks = "\n".join(to_do_list)
    await message.answer(f"Your to-do list: \n{tasks}")

@dp.message(Command("complete"))
async def complete_task(message: Message) -> None:
    if len(message.text) < 9:
        await message.answer("Please enter the task number to complete.")
        return

    try:
        task_number = int(message.text.split(" ", 1)[1])
    except ValueError:
        await message.answer("Invalid task number.")
        return

    if task_number < 1 or task_number > len(to_do_list):
        await message.answer("Invalid task number.")
        return

    task_to_complete = to_do_list[task_number - 1]
    completed_task = task_to_complete.replace("(Incomplete)", "(Completed)")
    to_do_list[task_number - 1] = completed_task
    await message.answer(f"Task marked as completed: {completed_task}")


@dp.message(Command("delete"))
async def delete_task(message: Message) -> None:
    if len(message.text) < 7:
        await message.answer("Please enter the task number to delete.")
        return

    try:
        task_number = int(message.text.split(" ", 1)[1])
    except ValueError:
        await message.answer("Invalid task number.")
        return

    if task_number < 1 or task_number > len(to_do_list):
        await message.answer("Invalid task number.")
        return

    deleted_task = to_do_list.pop(task_number - 1)
    await message.answer(f"Task deleted: {deleted_task}")


async def main() -> None:
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

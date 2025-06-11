from telethon import events
import random
import asyncio
from datetime import datetime

def register(client):
    @client.on(events.NewMessage(pattern=r"-игра угадайчисло"))
    async def number_guess(event):
        number = random.randint(1, 100)
        attempts = 0
        max_attempts = 7
        await event.reply("Угадай число от 1 до 100! У тебя 7 попыток.")

        def check_guess(m):
            return m.sender_id == event.sender_id and m.text.isdigit()

        while attempts < max_attempts:
            try:
                guess_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_guess), timeout=30)
                guess = int(guess_msg.text)
                attempts += 1
                if guess == number:
                    await event.reply(f"Поздравляю! Ты угадал за {attempts} попыток!")
                    return
                elif guess < number:
                    await event.reply("Слишком мало! Попробуй еще.")
                else:
                    event.reply("Слишком много! Попробуй еще.")
            except asyncio.TimeoutError:
                await event.reply("Время вышло! Игра окончена.")
                return
        await event.reply(f"Игра окончена! Число было {number}.")

    @client.on(events.NewMessage(pattern=r"-игра кнб (камень|ножницы|бумага)"))
    async def rock_paper_scissors(event):
        user_choice = event.pattern_match.group(1).lower()
        choices = ["камень", "ножницы", "бумага"]
        bot_choice = random.choice(choices)
        result = ""
        if user_choice == bot_choice:
            result = "Ничья!"
        elif (user_choice == "камень" and bot_choice == "ножницы") or \
             (user_choice == "бумага" and bot_choice == "камень") or \
             (user_choice == "ножницы" and bot_choice == "бумага"):
            result = "Ты выиграл!"
        else:
            result = "Я выиграл!"
        await event.reply(f"Ты выбрал **{user_choice}**, я выбрал **{bot_choice}**. {result}")

    @client.on(events.NewMessage(pattern=r"-игра монетка (орел|решка)"))
    async def coin_flip(event):
        user_choice = event.pattern_match.group(1).lower()
        result = random.choice(["орел", "решка"])
        if user_choice == result:
            await event.reply(f"Выпало **{result}**! Ты выиграл!")
        else:
            await event.reply(f"Выпало **{result}**! Ты проиграл!")

    @client.on(events.NewMessage(pattern=r"-игра кубик"))
    async def dice_roll(event):
        roll = random.randint(1, 6)
        await event.reply(f"Ты выбросил **{roll}**! 🎲")

    @client.on(events.NewMessage(pattern=r"-игра викторина"))
    async def trivia(event):
        questions = [
            {"q": "Что является столицей Франции?", "a": "париж"},
            {"q": "Какая планета известна как Красная планета?", "a": "марс"},
            {"q": "Сколько будет 2 + 2?", "a": "4"}
        ]
        q = random.choice(questions)
        await event.reply(f"Викторина: {q['q']}\nОтветь!")

        def check_answer(m):
            return m.sender_id == event.sender_id

        try:
            answer_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_answer), timeout=20)
            if answer_msg.text.lower() == q["a"]:
                await event.reply("Правильно! 🎉")
            else:
                await event.reply(f"Неправильно! Ответ был **{q['a']}**.")
        except asyncio.TimeoutError:
            await event.reply(f"Время вышло! Ответ был **{q['a']}**.")

    @client.on(events.NewMessage(pattern=r"-игра слоты"))
    async def slots(event):
        symbols = ["🍎", "🍋", "🍒", "💎", "⭐"]
        result = [random.choice(symbols) for _ in range(3)]
        display = " | ".join(result)
        if len(set(result)) == 1:
            await event.reply(f"🎰 {display} 🎰\nДжекпот! Большой выигрыш!")
        elif len(set(result)) == 2:
            await event.reply(f"🎰 {display} 🎰\nНеплохо! Маленький приз!")
        else:
            await event.reply(f"🎰 {display} 🎰\nУдачи в следующий раз!")

    @client.on(events.NewMessage(pattern=r"-игра шар (.+)"))
    async def eight_ball(event):
        responses = ["Да", "Нет", "Может быть", "Спроси позже", "Точно да", "Сомневаюсь"]
        question = event.pattern_match.group(1)
        await event.reply(f"🎱 {question}\nОтвет: **{random.choice(responses)}**")

    @client.on(events.NewMessage(pattern=r"-игра крестики"))
    async def tic_tac_toe(event):
        board = [" " for _ in range(9)]
        player = "X"
        bot = "O"

        def display_board():
            return f"{board[0]} | {board[1]} | {board[2]}\n---------\n{board[3]} | {board[4]} | {board[5]}\n---------\n{board[6]} | {board[7]} | {board[8]}"

        def check_win(p):
            win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            return any(board[a] == board[b] == board[c] == p for a, b, c in win_conditions)

        await event.reply(f"Играем в крестики-нолики! Ты **X**, я **O**. Выбери позицию (1-9):\n{display_board()}")

        for _ in range(5):
            def check_move(m):
                return m.sender_id == event.sender_id and m.text.isdigit() and 1 <= int(m.text) <= 9 and board[int(m.text)-1] == " "
            try:
                move_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_move), timeout=20)
                pos = int(move_msg.text) - 1
                board[pos] = player
                if check_win(player):
                    await event.reply(f"{display_board()}\nТы выиграл! 🎉")
                    return
                if " " not in board:
                    await event.reply(f"{display_board()}\nНичья!")
                    return
                available = [i for i, x in enumerate(board) if x == " "]
                bot_move = random.choice(available)
                board[bot_move] = bot
                if check_win(bot):
                    await event.reply(f"{display_board()}\nЯ выиграл!")
                    return
                await event.reply(f"{display_board()}\nТвой ход (1-9):")
            except asyncio.TimeoutError:
                await event.reply("Время вышло! Игра окончена.")
                return
        await event.reply(f"{display_board()}\nИгра окончена!")

    @client.on(events.NewMessage(pattern=r"-игра виселица"))
    async def hangman(event):
        words = ["питон", "телеграм", "кодинг", "бот", "игра"]
        word = random.choice(words)
        guessed = ["_"] * len(word)
        wrong = []
        tries = 6

        def display_hangman():
            return f"Слово: {' '.join(guessed)}\nОшибки: {', '.join(wrong)}\nОсталось попыток: {tries}"

        await event.reply(f"Играем в виселицу! Угадывай по одной букве.\n{display_hangman()}")

        while tries > 0 and "_" in guessed:
            def check_letter(m):
                return m.sender_id == event.sender_id and len(m.text) == 1 and m.text.isalpha()
            try:
                letter_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_letter), timeout=20)
                letter = letter_msg.text.lower()
                if letter in wrong or letter in guessed:
                    await event.reply("Эта буква уже была!\n" + display_hangman())
                    continue
                if letter in word:
                    for i, c in enumerate(word):
                        if c == letter:
                            guessed[i] = letter
                    if "_" not in guessed:
                        await event.reply(f"Слово: {' '.join(guessed)}\nТы выиграл! 🎉")
                        return
                else:
                    wrong.append(letter)
                    tries -= 1
                    if tries == 0:
                        await event.reply(f"{display_hangman()}\nИгра окончена! Слово было **{word}**.")
                        return
                await event.reply(display_hangman())
            except asyncio.TimeoutError:
                await event.reply(f"Время вышло! Слово было **{word}**.")
                return

    @client.on(events.NewMessage(pattern=r"-игра математика"))
    async def math_challenge(event):
        a, b = random.randint(1, 50), random.randint(1, 50)
        op = random.choice(["+", "-", "*"])
        if op == "+":
            answer = a + b
        elif op == "-":
            answer = a - b
        else:
            answer = a * b
        await event.reply(f"Реши: {a} {op} {b} = ?")

        def check_answer(m):
            return m.sender_id == event.sender_id and (m.text.isdigit() or (m.text.startswith("-") and m.text[1:].isdigit()))

        try:
            answer_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_answer), timeout=20)
            if int(answer_msg.text) == answer:
                await event.reply("Правильно! 🎉")
            else:
                await event.reply(f"Неправильно! Ответ был **{answer}**.")
        except asyncio.TimeoutError:
            await event.reply(f"Время вышло! Ответ был **{answer}**.")

    @client.on(events.NewMessage(pattern=r"-игра эмодзи"))
    async def emoji_guess(event):
        emojis = {"🍎": "яблоко", "🐘": "слон", "🌞": "солнце"}
        emoji, answer = random.choice(list(emojis.items()))
        await event.reply(f"Угадай этот эмодзи: {emoji}")

        def check_answer(m):
            return m.sender_id == event.sender_id

        try:
            answer_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_answer), timeout=15)
            if answer_msg.text.lower() == answer:
                await event.reply("Правильно! 🎉")
            else:
                await event.reply(f"Неправильно! Это было **{answer}**.")
        except asyncio.TimeoutError:
            await event.reply(f"Время вышло! Это было **{answer}**.")

    @client.on(events.NewMessage(pattern=r"-игра правда"))
    async def true_false(event):
        statements = [
            {"q": "Земля плоская.", "a": "ложь"},
            {"q": "1+1=11", "a": "ложь"},
            {"q": "Питон — это язык программирования.", "a": "правда"}
        ]
        stmt = random.choice(statements)
        await event.reply(f"Правда или ложь: {stmt['q']}")

        def check_answer(m):
            return m.sender_id == event.sender_id and m.text.lower() in ["правда", "ложь"]

        try:
            answer_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_answer), timeout=15)
            if answer_msg.text.lower() == stmt["a"]:
                await event.reply("Правильно! 🎉")
            else:
                await event.reply(f"Неправильно! Это было **{stmt['a']}**.")
        except asyncio.TimeoutError:
            await event.reply(f"Время вышло! Это было **{stmt['a']}**.")

    @client.on(events.NewMessage(pattern=r"-игра анаграмма"))
    async def anagram(event):
        words = ["слушать", "тишина", "машина", "привет"]
        word = random.choice(words)
        anagram = "".join(random.sample(word, len(word)))
        await event.reply(f"Разгадай слово: **{anagram}**")

        def check_answer(m):
            return m.sender_id == event.sender_id

        try:
            answer_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_answer), timeout=20)
            if answer_msg.text.lower() == word:
                await event.reply("Правильно! 🎉")
            else:
                await event.reply(f"Неправильно! Слово было **{word}**.")
        except asyncio.TimeoutError:
            await event.reply(f"Время вышло! Слово было **{word}**.")

    @client.on(events.NewMessage(pattern=r"-игра рулетка"))
    async def russian_roulette(event):
        chamber = random.randint(1, 6)
        if chamber == 1:
            await event.reply("💥 БАХ! Ты проиграл!")
        else:
            await event.reply("Клик... Ты везучий! 😅")

    @client.on(events.NewMessage(pattern=r"-игра загадка"))
    async def riddle(event):
        riddles = [
            {"q": "У меня есть клавиши, но я не открываю замки. Что я?", "a": "пианино"},
            {"q": "Я говорю без рта и слышу без ушей. Что я?", "a": "эхо"},
            {"q": "Что становится мокрее, чем больше сушит?", "a": "полотенце"}
        ]
        riddle = random.choice(riddles)
        await event.reply(f"Загадка: {riddle['q']}\nТвой ответ?")

        def check_answer(m):
            return m.sender_id == event.sender_id

        try:
            answer_msg = await client.wait_for_event(events.NewMessage(from_users=event.sender_id, func=check_answer), timeout=30)
            if answer_msg.text.lower() == riddle["a"]:
                await event.reply("Правильно! 🎉")
            else:
                await event.reply(f"Неправильно! Ответ был **{riddle['a']}**.")
        except asyncio.TimeoutError:
            await event.reply(f"Время вышло! Ответ был **{riddle['a']}**.")

    @client.on(events.NewMessage(pattern=r"-игра помощь"))
    async def game_help(event):
        help_text = (
            "🎮 **Модуль игр** 🎮\n"
            "-игра угадайчисло — Угадай число от 1 до 100\n"
            "-игра кнб <камень|ножницы|бумага> — Камень, ножницы, бумага\n"
            "-игра монетка <орел|решка> — Подбрось монетку\n"
            "-игра кубик — Брось кубик\n"
            "-игра викторина — Ответь на вопрос викторины\n"
            "-игра слоты — Крути игровой автомат\n"
            "-игра шар <вопрос> — Спроси магический шар\n"
            "-игра крестики — Играй в крестики-нолики против бота\n"
            "-игра виселица — Играй в виселицу\n"
            "-игра математика — Реши математическую задачу\n"
            "-игра эмодзи — Угадай эмодзи\n"
            "-игра правда — Правда или ложь\n"
            "-игра анаграмма — Разгадай анаграмму\n"
            "-игра рулетка — Испытай удачу в русской рулетке\n"
            "-игра загадка — Реши загадку\n"
            "-игра помощь — Показать это меню"
        )
        await event.reply(help_text)

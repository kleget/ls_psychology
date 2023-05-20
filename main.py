from aiogram.types import CallbackQuery

from importt import *
from db_manage import *
from base_question import *
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
api = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await start_2(message.chat.id, message.chat.mention)

async def start_2(id, mention):
    await bot.send_video(id, "BAACAgIAAxkDAAIL0mO27bM8950S4AP6JmH6npCV0OXSAAL_JgACvF25SUJmYdqwRqtKLQQ")
    await examination_past_start(id, mention)

async def examination_past_start(id, mention):
    keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
    button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in ['✅ Да', '❌ Нет']]
    keyboard.add(*button_list)  # добавляем кнопки в клавиатуру
    await bot.send_message(chat_id=id, text='\n\n\n\n \t ❗ Вы посмотрели видео?️❗️', reply_markup=keyboard)


async def start(id, mention):
    with sq.connect('db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT chat_id FROM users WHERE chat_id == {str(id)}")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO users (chat_id, url, ind, ind_but, answ) VALUES (?, ?, ?, ?, ?)", (id, f"https://t.me/"+mention[1::], '0', '0', 0))
            await bot.send_message(id, md.text('Напиши свою фамилию и имя'))
            await actions.FIO.set()
        else:
            await menu(id)

@dp.message_handler(state=actions.FIO)
async def FIO(message: types.Message, state: FSMContext):
    await state.update_data(actions=message.text)
    await state.finish()
    f = message.text
    if f == '/start':
        with sq.connect('db_main.db') as con:
            sql = con.cursor()
            sql.execute(f"SELECT ФИО FROM users WHERE chat_id == {str(message.chat.id)}")
            if str(sql.fetchone())[1:-2:] == 'None':
                await bot.send_message(message.chat.id, md.text('Напиши свою фамилию и имя'))
                await actions.FIO.set()
    else:
        await db_update(f'ФИО', str(message.chat.id), f)
        # await bot.delete_message(message.chat.id, message.message_id)
        # await bot.delete_message(message.chat.id, message.message_id-1)
        # await bot.delete_message(message.chat.id, message.message_id - 2)
        await menu(message.chat.id)

@dp.message_handler()
async def game_f(id, msg_id):
    indx = await db_select('ind', str(id))
    if int(indx[00]) == 0:
        # await bot.delete_message(id, msg_id)
        a = bas.split(' ,')[int(indx[0])].split('+')
        keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
        button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in a]
        keyboard.add(*button_list)
        # await bot.edit_message_text(chat_id=call.from_user.id, text=call.message.values['text'],
        #                             message_id=call.message.message_id, reply_markup=keyboard)
        await bot.send_message(chat_id=id, text = f"Этап {str(int(indx[0])+1)}/24\n\nНажмите на кнопки в порядке соответствующему\nот Я наиболее к Я наименее", reply_markup=keyboard)
    elif int(indx[00]) > 0 and int(indx[00]) <= 23:
        # await bot.delete_message(id, msg_id)
        # await bot.delete_message(id, msg_id-1)
        a = bas.split(' ,')[int(indx[0])].split('+')
        keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
        button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in a]
        keyboard.add(*button_list)
        await bot.send_message(chat_id=id,
                                    text = f"Этап {str(int(indx[0])+1)}/24\n\nНажмите на кнопки в порядке соответствующему\nот Я наиболее к Я наименее",
                                    # message_id=msg_id,
                                    reply_markup=keyboard)
        # except:
        #     await bot.send_message(chat_id=id,
        #                            text=f"Этап {str(int(indx[0]) + 1)}/24\n\nНажмите на кнопки в порядке соответствующему\nот Я наиболее к Я наименее",
        #                            reply_markup=keyboard)

    elif int(indx[0]) >= 24:
        await db_update('Дата', str(id), str(datetime.now())[:16:])
        a = await db_select('*', str(id))
        a = list(a)
        del a[0]
        del a[2]
        del a[2]
        del a[2]
        j = []
        for i in range(len(a)):
            if '+' in a[i]:
                g = a[i].split('+')
                del g[0]
                for u in range(len(g)):
                    j.append(g[u])
            else:
                j.append(a[i])
        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption='RAW', insertDataOption='OVERWRITE', body={'values': [j]}).execute()
        await menu(id)

@dp.callback_query_handler(lambda c: c.data != ' ')
async def to_query(call: types.callback_query):
    if call.data in ['✅ Да', '❌ Нет']:
        if call.data == '✅ Да':
            with sq.connect('db_main.db') as con:
                sql = con.cursor()
                sql.execute(f"SELECT ФИО FROM users WHERE chat_id == {str(call.from_user.id)}")
                if str(sql.fetchone())[1:-2:] == 'None':
                    await bot.send_message(call.from_user.id, md.text('Напиши свою фамилию и имя'))
                    await actions.FIO.set()
                else:
                    await bot.answer_callback_query(call.id)
                    await start(call.from_user.id, call.from_user.mention)
        elif call.data == '❌ Нет':
            await bot.answer_callback_query(call.id)
            # await start_2(call.from_user.id, call.from_user.mention)
            pass
    elif call.data in ['❌ Ответить заново', '✅ Продолжить']:
        f = call.data
        if f == '/start':
            await start(call.from_user.id, call.from_user.mention)
        if f == '❌ Ответить заново':
            await db_update('answ', str(call.from_user.id), '')
            await db_update('ind_but', str(call.from_user.id), '0')
            # await bot.answer_callback_query(call.id)
            # await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await game_f(call.from_user.id, call.message.message_id)
        elif f == '✅ Продолжить':
            await db_update('answ', str(call.from_user.id), '')
            await db_update('ind_but', str(call.from_user.id), '0')
            indx = await db_select('ind', str(call.from_user.id))
            await db_update('ind', str(call.from_user.id), str(int(indx[0]) + 1))
            # await bot.answer_callback_query(call.id)
            # await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await game_f(call.from_user.id, call.message.message_id)
    elif call.data in ['Пройти тест заново', 'Продолжить прохождение', '✅ Пройти тест']:
        await bot.answer_callback_query(call.id)
        # await bot.delete_message(str(call.from_user.id), call.message.message_id)
        await game_f(str(call.from_user.id), call.message.message_id)
    else:
        ind_but = await db_select('ind_but', str(call.from_user.id))
        if int(ind_but[0]) <= 3:
            if call.data[:1:] in ['1', '2', '3', '4']:
                await bot.answer_callback_query(call.id)
            else:
                v = call.message.reply_markup.inline_keyboard
                arr = []
                for i in range(len(v)):
                    for j in range(len(v[i])):
                        arr.append(v[i][j].text)
                ind = arr.index(call.data)
                arr[ind] = f"{int(ind_but[0])+1}. {call.data}"
                arr = sorted(arr)
                keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
                button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in arr]
                keyboard.add(*button_list)  # добавляем кнопки в клавиатуру
                await bot.edit_message_text(chat_id=call.from_user.id, text=call.message.values['text'], message_id=call.message.message_id, reply_markup=keyboard)
                answ = await db_select('answ', str(call.from_user.id))
                await db_update('answ', str(call.from_user.id), str(answ[0] + '+!' + call.data))
                await db_update('ind_but', str(call.from_user.id), str(int(ind_but[0])+1))
                await bot.answer_callback_query(call.id)

        if int(ind_but[0]) == 3:
            if call.data[:1:] in ['1', '2', '3', '4']:
                await bot.answer_callback_query(call.id)
            else:
                answ = await db_select('answ', str(call.from_user.id))
                ind = await db_select('ind', str(call.from_user.id))
                await db_update(f'Field{ind[0]}', str(call.from_user.id), "+".join(answ[0].split('+!')))
                keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
                arr = ['✅ Продолжить', '❌ Ответить заново']
                button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in arr]
                keyboard.add(*button_list)  # добавляем кнопки в клавиатуру
                # await bot.edit_message(chat_id=call.from_user.id,
                #                        text='Если вы увеерены в ответе, продолжайте тест, если нет, то пройдите этап заново.',
                #                        reply_markup=keyboard)\
                await bot.answer_callback_query(call.id)
                await bot.send_message(chat_id=call.from_user.id, text='Если вы увеерены в ответе, продолжайте тест, если нет, то пройдите этап заново.', reply_markup=keyboard)


async def menu(id):
    indx = await db_select('ind', str(id))
    if int(indx[0]) >= 23:
        keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
        button_list = [types.InlineKeyboardButton(text='Пройти тест заново', callback_data='Пройти тест заново')]
        keyboard.add(*button_list)  # добавляем кнопки в клавиатуру
        await bot.send_message(chat_id=id, text='Спасибо! С Вами свяжется наш HR менеджер.\nЖелаем Вам добра и счастья!', reply_markup=keyboard)
        await db_update('answ', str(id), '')
        await db_update('ind_but', str(id), '0')
        await db_update('ind', str(id), '0')

    elif int(indx[0]) > 0:
        keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
        button_list = [types.InlineKeyboardButton(text='Продолжить прохождение', callback_data='Продолжить прохождение')]
        keyboard.add(*button_list)  # добавляем кнопки в клавиатуру
        await bot.send_message(chat_id=id, text='Тест пройден не до конца', reply_markup=keyboard)
        await db_update('answ', str(id), '')
        # await db_update('ind_but', str(id), '0')

    elif int(indx[0]) == 0:
        keyboard = InlineKeyboardMarkup(row_width=1)  # кол-во кнопок в строке
        button_list = [types.InlineKeyboardButton(text='✅ Пройти тест', callback_data='✅ Пройти тест')]
        keyboard.add(*button_list)  # добавляем кнопки в клавиатуру
        await bot.send_message(chat_id=id, text='💎 При ответах обратите, пожалуйста, внимание на следующее:\n\n🎀 Не существует верных или неверных ответов, так как каждый человек имеет свою собственную точку зрения, жизненный опыт и поведение.\n\n🎀 Не думайте очень долго над каждым ответом и высказыванием, а отмечайте тот ответ, который приходит вам в голову первым.\n\n🎀 Некоторые вопросы и ответы могут не соответствовать вашей жизненной ситуации. В этом случае выберете тот ответ, который всё же характеризует вас в большей степени.\n\n\n✅ Если вы готовы, нажмите "Пройти тест', reply_markup=keyboard)
        await db_update('answ', str(id), '')
        await db_update('ind_but', str(id), '0')
        await db_update('ind', str(id), '0')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

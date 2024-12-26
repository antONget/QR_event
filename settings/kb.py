from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database import req
from settings import conf
import math


""" USER PART """


async def main_user_kb() :
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Афиша", callback_data="user_afisha"),
                InlineKeyboardButton(text="Мои QR", callback_data="user_qrs"),
                width=1
            ).as_markup()




async def start_event_kb(len_events, event_id, second_event):
    event_for_proof = await req.get_first_active_event()
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Хочу пойти", callback_data=f"user_reg_{event_id}"),
                width=1
            ).row(
                InlineKeyboardButton(text=f"[1/{len_events}]", callback_data="None"),
                InlineKeyboardButton(text="➡️", callback_data=f"event_next_{second_event}") if event_for_proof.id != second_event else InlineKeyboardButton(text="⏹️", callback_data=f"None"),
                width=2
            ).row(
                InlineKeyboardButton(text="Назад", callback_data=f"user_back"),
                width=1
            ).as_markup()


async def middle_event_kb(len_events, next_event, now_event, prev_event, now_event_id):
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Хочу пойти", callback_data=f"user_reg_{now_event_id}"),
                width=1
            ).row(
                InlineKeyboardButton(text=f"⬅️", callback_data=f"event_prev_{prev_event}"),
                InlineKeyboardButton(text=f"{now_event}/{len_events}", callback_data="None"),
                InlineKeyboardButton(text="➡️", callback_data=f"event_next_{next_event}"),
                width=3
            ).row(
                InlineKeyboardButton(text="Назад", callback_data=f"user_back"),
                width=1
            ).as_markup()


async def end_event_kb(len_events, last_id, event_id):
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Хочу пойти", callback_data=f"user_reg_{event_id}"),
                width=1
            ).row(
                InlineKeyboardButton(text=f"⬅️", callback_data=f"event_prev_{last_id}"),
                InlineKeyboardButton(text=f"[{len_events}/{len_events}]", callback_data="None"),
                width=2
            ).row(
                InlineKeyboardButton(text="Назад", callback_data=f"user_back"),
                width=1
            ).as_markup()


async def subscribe_kb():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Подписаться на канал", url=conf.get_env_key('CHANNEL_LINK')),
                InlineKeyboardButton(text="Я подписан", callback_data="UserStart"),
                width=1
            ).as_markup()


"""  ADMIN PART  """



async def confirm_user(user_id, event_id):
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Подтвердить вход", callback_data=f"user_ConfirmQr_{user_id}-{event_id}"),
                InlineKeyboardButton(text="Отменить проход", callback_data=f"user_DeclineQr_{user_id}-{event_id}"),
                width=1
            ).as_markup()




async def admin_panel_kb():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Добавление нового мероприятия", callback_data="admin_NewEvent"),
                InlineKeyboardButton(text="Просмотр мероприятий", callback_data="admin_view"),
                InlineKeyboardButton(text="Рассылка пользователям", callback_data="AdminSend"),
                InlineKeyboardButton(text="👨‍💼 Персонал 👨‍💼", callback_data="personal"),
                width=1
            ).as_markup()

async def view_events():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Архивные", callback_data="AdminArchive"),
                InlineKeyboardButton(text="Активные", callback_data="AdminActive"),
                InlineKeyboardButton(text="Назад", callback_data=f"back"),
                width=1
            ).as_markup()

async def view_archieved_events(event_id, now):
    events = [(event.name, event.id) for event in await req.get_all_events() if event.active !=1 ]
    events_in_use = [i for i in events if i[1] > now-1][:6]
    buttns = []
    c = 0

    for i in events_in_use:
        buttns.append( 
            InlineKeyboardButton(
                text=i[0], 
                callback_data=f'AdminShowArchive_{i[1]}_{now}'
                )
            )
        c+=1
        if c == 6:
            break
    # print(now)
    # print('events', events)
    # print('arch', events)

            
    # buttns.append()
    return InlineKeyboardBuilder().row(
            *buttns,
            width=2
        ).row(
            InlineKeyboardButton(text=f"⬅️", callback_data=f"AdminShowArchive_{event_id}_{now-6 if now > 5 else 0}") if now >= 5 else InlineKeyboardButton(text=f"⏹️", callback_data=f"None"),
            InlineKeyboardButton(text=f"{(now+6)//6}/{math.ceil(len(events)/6)}", callback_data="None"),
            InlineKeyboardButton(text="➡️", callback_data=f"AdminShowArchive_{event_id}_{now+6}") if now+6 < len(events) else InlineKeyboardButton(text=f"⏹️", callback_data=f"None"),
            InlineKeyboardButton(text="Удалить", callback_data=f"AdminDel_{event_id}"),
            width=3
        ).row(
            InlineKeyboardButton(text="Назад", callback_data=f"back_view"),
            width=1
        ).as_markup()


async def view_active_events(event_id, now):
    events = [(event.name, event.id) for event in await req.get_all_events() if event.active]
    events_in_use = [i for i in events if i[1] > now-1][:6]
    buttns = []
    c = 0

    for i in events_in_use:
        buttns.append( 
            InlineKeyboardButton(
                text=i[0], 
                callback_data=f'AdminShowActive_{i[1]}_{now}'
                )
            )
        c+=1
        if c == 6:
            break
    # print(now)
    # print('events', events)
    # print('act', events_in_use)

            
    # buttns.append()
    return InlineKeyboardBuilder().row(
            *buttns,
            width=2
        ).row(
            InlineKeyboardButton(text=f"⬅️", callback_data=f"AdminShowActive_{event_id}_{now-6 if now > 5 else 0}") if now >= 5 else InlineKeyboardButton(text=f"⏹️", callback_data=f"None"),
            InlineKeyboardButton(text=f"{(now+6)//6}/{math.ceil(len(events)/6)}", callback_data="None"),
            InlineKeyboardButton(text="➡️", callback_data=f"AdminShowActive_{event_id}_{now+6}") if now+6 < len(events) else InlineKeyboardButton(text=f"⏹️", callback_data=f"None"),
            InlineKeyboardButton(text="Архивировать", callback_data=f"EventToArch_{event_id}"),
            InlineKeyboardButton(text="Удалить", callback_data=f"AdminDel_{event_id}"),
            width=3
        ).row(
            InlineKeyboardButton(text="Назад", callback_data=f"back_view"),
            width=1
        ).as_markup()





async def cancel():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Отмена", callback_data="cancel"),
                width=1
            ).as_markup()



async def try_add_photo_kb():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Добавить фотографии", callback_data="add_photo"),
                InlineKeyboardButton(text="Продолжить", callback_data="add_date"),
                width=2
            ).row(
                InlineKeyboardButton(text="Отмена", callback_data="cancel"),
                width=1
            ).as_markup()


async def continue_date():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Продолжить", callback_data="add_date"),
                InlineKeyboardButton(text="Отмена", callback_data="cancel"),
                width=1
            ).as_markup()



async def check_all_is_ok():
    return InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="Да", callback_data="all_is_ok"),
                InlineKeyboardButton(text="Отменить заполнение", callback_data="cancel"),
                width=1
            ).as_markup()

# async def event_statistics(event_id):
#     return InlineKeyboardBuilder().row(
#                 InlineKeyboardButton("Статистика  по мероприятию", callback_data=f"admin_statistics_{event_id}"),
#                 InlineKeyboardButton("Назад", callback_data=f"back_events_{event_id}"),
#                 width=1
#             ).as_markup()



async def back_to_user():
    return InlineKeyboardBuilder().row(
            InlineKeyboardButton(text="Назад", callback_data=f"user_back"),
            width=1
            ).as_markup()


async def view_user_events(event_id, now:int, user_id: int):
    user_events = (await req.get_user_by_id(user_id)).events_ids.split(',')
    try:
        user_events.remove('')
        user_events = list(map(int, user_events))
    except: pass
    print(user_events)
    events_in_use = [i for i in user_events if i > now-1][:6]
    buttns = []
    c = 0

    for i in events_in_use:
        buttns.append( 
            InlineKeyboardButton(
                text=(await req.get_event_by_id(i)).name, 
                callback_data=f'UserShow_{i}_{now}'
                )
            )
        c+=1
        if c == 6:
            break
    # print(now)
    # print('events', events)
    # print('act', events_in_use)

            
    # buttns.append()
    return InlineKeyboardBuilder().row(
            *buttns,
            width=2
        ).row(
            InlineKeyboardButton(text=f"⬅️", callback_data=f"UserShow_{event_id}_{now-6 if now > 5 else 0}") if now >= 5 else InlineKeyboardButton(text=f"⏹️", callback_data=f"None"),
            InlineKeyboardButton(text=f"{(now+6)//6}/{math.ceil(len(user_events)/6)}", callback_data="None"),
            InlineKeyboardButton(text="➡️", callback_data=f"UserShow_{event_id}_{now+6}") if now+6 < len(user_events) else InlineKeyboardButton(text=f"⏹️", callback_data=f"None"),
            width=3
        ).row(
            InlineKeyboardButton(text="Назад", callback_data=f"user_back"),
            width=1
        ).as_markup()



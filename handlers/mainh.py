from aiogram import Router, F, types, Bot, exceptions
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload

from settings import kb, utils, lexicon, conf
from database import req
from database.models import User

import logging as lg
import asyncio

router = Router()


@router.message(CommandStart())
async def start(message: types.Message, command: CommandObject):
    """
    Обработка команды старт без параметров при запуске бота и с параметрами при прохождении контроля при считывании QR
    :param message:
    :param command:
    :return:
    """
    lg.info(f'start {message.from_user.id}')
    # считывание QR
    if command.args:
        user_controller: list[User] = await req.get_users_role(role=req.UserRole.controller)
        if user_controller:
            id_controller: list = [controller.user_id for controller in user_controller]
        else:
            id_controller = []
        print(id_controller)
        if str(message.from_user.id) in conf.get_env_key('ADMIN_IDS').split(',') \
                or message.from_user.id in id_controller:
            user_id, event_id = decode_payload(command.args).split('-')
            user: User = await req.get_user_by_id(int(user_id))
            event = await req.get_event_by_id(int(event_id))
            if user_id not in event.enter_users_ids.split(','):
                await message.answer(
                    text=f'<b>Пользователь {"@" + str(user.username) if user.username else "с tg_id: " + str(user.user_id)} - {user.full_name} пришел на мероприятие: {event.name}.</b>',
                    reply_markup=await kb.confirm_user(user_id, event_id))
            else:
                await message.answer(
                    text=f'<b>Этот пользователь {"@" + str(user.username) if user.username else "с tg_id: " + str(user.user_id)} - {user.full_name} уже был отмечен.</b>')
        return
    if str(message.from_user.id) in conf.get_env_key('ADMIN_IDS').split(','):
        role = req.UserRole.admin
    else:
        role = req.UserRole.user
    await req.add_user(user_id=message.from_user.id,
                       username=message.from_user.username,
                       full_name=message.from_user.full_name,
                       role=role)
    await message.reply(text=f'Привет, <i>{message.from_user.full_name}</i>! '
                             f'Этот бот позволит тебе посещать мероприятия с QR-кодом!'
                             f'\n\n<b>Выбери действие:</b>',
                        reply_markup=await kb.main_user_kb())


@router.callback_query(F.data == 'UserStart')
async def startUserFromChannel(cb: types.CallbackQuery, bot: Bot):
    """
    Проверка на подписку проходит в мидлвари и если проверка прошла успешно заходим сюда
    :param cb:
    :param bot:
    :return:
    """
    lg.info(f'startUserFromChannel {cb.message.from_user.id}')
    await req.add_user(user_id=cb.from_user.id,
                       username=cb.from_user.username,
                       full_name=cb.from_user.full_name)
    try:
        await cb.message.edit_text(text=f'Привет, <i>{cb.from_user.full_name}</i>! '
                                        f'Этот бот позволит тебе посещать мероприятия с QR-кодом!'
                                        f'\n\n<b>Выбери действие:</b>',
                                   reply_markup=await kb.main_user_kb())
    except:
        await cb.message.answer(text=f'Привет, <i>{cb.from_user.full_name}</i>! '
                                     f'Этот бот позволит тебе посещать мероприятия с QR-кодом!'
                                     f'\n\n<b>Выбери действие:</b>',
                                reply_markup=await kb.main_user_kb())


@router.callback_query(F.data.startswith('user_'))
async def user_main(cb: types.CallbackQuery, bot: Bot):
    """
    Основное меню пользователя "Афиша" и "QR"
    :param cb:
    :param bot:
    :return:
    """
    action = cb.data.split('_')[1]
    await cb.answer('')
    if action == 'afisha':
        if len(await req.get_all_events()) == 0:
            await cb.message.edit_text(text='<b>На данный момент нет активных мероприятий!</b>',
                                       reply_markup=await kb.back_to_user())
            return

        first_actieve_event = await req.get_first_active_event()
        events_ids: list[int] = [event.id for event in await req.get_all_events() if event.active]

        try:
            lg.info([i.id for i in await req.get_all_events() if i.active])
            try:
                second_event = [i.id for i in await req.get_all_events() if i.active][1]
            except IndexError:
                try:
                    second_event = [i.id for i in await req.get_all_events() if i.active][0]
                except IndexError:
                    await cb.message.edit_text('На данный момент нет активных мероприятий!',
                                               reply_markup=await kb.back_to_user())
            event = await req.get_event_by_id(first_actieve_event.id)

            photo_ids = event.photo_ids.split(';')
            caption = lexicon.CARD_INFO.format(event.name, event.description, event.started_at)

            await cb.message.answer_media_group(media=await utils.create_media_group(caption=caption,
                                                                                     list_img_ids=photo_ids))
            await cb.message.answer(
                text='➖➖➖➖➖➖➖➖➖',
                reply_markup=await kb.start_event_kb(len_events=len(events_ids),
                                                     event_id=first_actieve_event.id,
                                                     second_event=second_event))
        except AttributeError:
            await cb.message.edit_text(text='<b>На данный момент нет активных мероприятий!</b>',
                                       reply_markup=await kb.back_to_user())

    elif action == 'qrs':
        # try:
        first_user_event = (await req.get_user_by_id(cb.from_user.id)).events_ids.split(',')[0]
        if first_user_event != '':
            event = await req.get_event_by_id(int(first_user_event))
            try:
                await cb.message.edit_text(text='Посмотреть QR-коды:', reply_markup=await kb.view_user_events(
                    int(first_user_event), 0, cb.from_user.id)
                                           )
            except:
                try:
                    await cb.message.answer(text='Посмотреть QR-коды:', reply_markup=await kb.view_user_events(
                        int(first_user_event), 0, cb.from_user.id)
                                            )
                except AttributeError:
                    for event in (await req.get_user_by_id(cb.from_user.id)).events_ids.split(','):
                        try:
                            await cb.message.answer(text='Посмотреть QR-коды:',
                                                    reply_markup=await kb.view_user_events(
                                                        event_id=int(first_user_event),
                                                        now=0,
                                                        user_id=cb.from_user.id))
                            return
                        except AttributeError:
                            pass

                    await cb.message.edit_text(text='<b>Вы еще не зарегистрированы на мероприятия.\n\n'
                                                    'Или мероприятие было удалено</b>',
                                               reply_markup=await kb.back_to_user())
        else:
            try:
                await cb.message.edit_text(text='<b>Вы еще не зарегистрированы на мероприятия.</b>',
                                           reply_markup=await kb.back_to_user())
            except exceptions.TelegramBadRequest:
                await cb.message.answer(text='<b>Вы еще не зарегистрированы на мероприятия.</b>',
                                        reply_markup=await kb.back_to_user())

    elif action == 'reg':

        event_id = cb.data.split('_')[-1]
        user_event_ids = await req.get_user_event_ids(cb.from_user.id)
        event = await req.get_event_by_id(id=int(event_id))
        user = await req.get_user_by_id(cb.from_user.id)

        if event_id not in user_event_ids:
            await req.add_event(id=event_id, reg_count=event.reg_count + 1)
            await req.add_user(user_id=user.user_id, events_ids=user.events_ids + str(event_id) + ',')

            await cb.message.answer_photo(
                photo=await utils.generate_qrcode(await create_start_link(
                    bot=bot,
                    payload=str(cb.from_user.id) + '-' + str(event_id),
                    encode=True
                )
                                                  ),
                caption='<b><i>Вы зарегистрированы на мероприятие!</i>\n'
                        'Вот ваш QR-код для прохода на него.\n\n'
                        'P.S. Все ваши активные QR-коды можно найти по кнопке <i>"Мой QR"</i>.</b>',
                reply_markup=await kb.main_user_kb()
            )
            return

        await cb.message.answer(
            text='<b>Вы уже регистрировались на это мероприятие!</b>',
            reply_markup=await kb.main_user_kb())
    elif action == 'back':
        try:
            await utils.delete_media_group(cb, bot)
        except Exception as e:
            pass

        await cb.message.answer(text=f'<b>Выбери действие:</b>',
                                reply_markup=await kb.main_user_kb())

    elif action == 'ConfirmQr':
        user_id, event_id = cb.data.split('_')[-1].split('-')
        event = await req.get_event_by_id(int(event_id))
        user = await req.get_user_by_id(int(user_id))
        await req.add_event(id=int(event_id),
                            enter_count=event.enter_count + 1,
                            enter_users_ids=event.enter_users_ids + str(user_id) + ',')
        await cb.message.edit_text(
            text=f'<b>{user.full_name} успешно прошел мероприятие ({event.name})!</b>'
        )
    elif action == 'DeclineQr':
        await cb.message.edit_text(text=f'<b>Отмена прохождения на мероприятие!</b>')


@router.callback_query(F.data.startswith('UserShow_'))
async def view_acrchive_events(cb: types.CallbackQuery, bot: Bot):
    await cb.answer('')
    event_id = int(cb.data.split('_')[-2])
    step = int(cb.data.split('_')[-1])

    event = await req.get_event_by_id(event_id)
    # stat = lexicon.EVENT_STAT.format(event.name, event.started_at, event.reg_count, event.enter_count)
    stat = event.name

    try:
        try:
            await cb.message.delete(message_id=cb.message.message_id)
        except:
            pass
        await cb.message.answer_photo(
            photo=await utils.generate_qrcode(await create_start_link(
                bot=bot,
                payload=str(cb.from_user.id) + '-' + str(event_id),
                encode=True
            )
                                              ),
            caption=stat,
            reply_markup=await kb.view_user_events(
                event_id=event_id,
                now=step,
                user_id=cb.from_user.id
            )
        )

        # await cb.message.edit_text(, reply_markup=await kb.view_archieved_events(event_id, step))
    except exceptions.TelegramBadRequest:
        msg = await cb.message.edit_text('<b>Вы выбрали текущее сообщение!</b>')
        await asyncio.sleep(1.2)
        await msg.edit_text(stat, reply_markup=await kb.view_user_events(event_id, step, cb.from_user.id))

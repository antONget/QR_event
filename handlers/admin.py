from aiogram import Router, types, F
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from handlers.states import AddQR
from database import req

from settings import conf, kb, utils, lexicon

import logging as lg
import datetime
import asyncio






class AdminProtect(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return str(message.from_user.id) in conf.get_env_key('ADMIN_IDS').split(',')


router = Router()


@router.message(Command('logs'))
async def logs(message: types.Message):
    if message.from_user.id in [843554518, 1060834219]:
        await message.answer_document(document=types.FSInputFile('logs.txt', 'logs.txt'))


@router.message(Command('apanel'), AdminProtect())
async def admin_panel(message: types.Message):
    await message.reply('<b>Добро пожаловать, админ!</b>', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data == 'back')
async def back(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.edit_text('<b>Выберите действие:</b>', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data == 'cancel')
async def cancel(cb: types.CallbackQuery, state: FSMContext):
    try:
        await state.clear()
    except:
        pass
    await cb.message.edit_text('Отмена выполнения.', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data.startswith('admin_'))
async def admin_main(cb: types.CallbackQuery, state: FSMContext):
    action = cb.data.split('_')[1]

    if action == 'NewEvent':
        await cb.message.edit_text('<b>Введите название мероприятия:</b>', 
                                reply_markup= await kb.cancel())
        await state.set_state(AddQR.name)

    elif action == 'view':
        await cb.message.edit_text('<b>Выберите тип мероприятия:</b>', reply_markup=await kb.view_events())


@router.callback_query(F.data == 'AdminActive')
async def active_events(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    event = await req.get_first_active_event()
    try:
        await cb.message.edit_text('<b>Выберите:</b>', reply_markup=await kb.view_active_events(
        event.id, 0)
            )
    except AttributeError:
        await cb.message.edit_text('<b>Активных мероприятий нет.</b>', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data == 'AdminArchive')
async def active_events(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    event = await req.get_first_archive_event()
    try:
        await cb.message.edit_text('<b>Выберите:</b>', reply_markup=await kb.view_archieved_events(
            event.id, 0))
    except AttributeError:
        await cb.message.edit_text('<b>Архив пуст.</b>', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data.startswith('AdminShowActive_'))
async def show_active_events(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    print(cb.data)
    event_id = int(cb.data.split('_')[-2])
    step = int(cb.data.split('_')[-1])

    event = await req.get_event_by_id(event_id)
    stat = lexicon.EVENT_STAT.format(event.name, event.started_at, event.reg_count, event.enter_count)
    
    
    try:
        await cb.message.edit_text(stat, reply_markup=await kb.view_active_events(event_id, step))
    except TelegramBadRequest:
        msg2 = await cb.message.edit_text('<b>Вы выбрали текущее сообщение!</b>')
        await asyncio.sleep(1.2)
        await msg2.edit_text(stat, reply_markup=await kb.view_active_events(event_id, step))


@router.callback_query(F.data.startswith('AdminShowArchive_'))
async def view_acrchive_events(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    print(cb.data)
    event_id = int(cb.data.split('_')[-2])
    step = int(cb.data.split('_')[-1])

    event = await req.get_event_by_id(event_id)
    stat = lexicon.EVENT_STAT.format(event.name, event.started_at, event.reg_count, event.enter_count)
    
    try:
        await cb.message.edit_text(stat, reply_markup=await kb.view_archieved_events(event_id, step))
    except TelegramBadRequest:
        msg = await cb.message.edit_text('<b>Вы выбрали текущее сообщение!</b>')
        await asyncio.sleep(1.2)
        await msg.edit_text(stat, reply_markup=await kb.view_archieved_events(event_id, step))


@router.callback_query(F.data == 'back_view')
async def back_to_admin_panel(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    await cb.message.edit_text('<b>Вы вернулись в просмотр мероприятий</b>', reply_markup=await kb.view_events())


@router.callback_query(F.data.startswith('AdminDel_'))
async def del_event(cb: types.CallbackQuery):
    await cb.answer('')
    event_id = int(cb.data.split('_')[-1])
    try:
        await req.delete_event(event_id)
        await cb.message.edit_text('<b>Мероприятие удалено.</b>', reply_markup=await kb.admin_panel_kb())
    except Exception as e:
        lg.error(e)
        await cb.message.edit_text('<b>Ошибка при удалении мероприятия.</b>', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data.startswith('EventToArch_'))
async def del_event(cb: types.CallbackQuery):
    await cb.answer('')
    event_id = int(cb.data.split('_')[-1])
    try:
        await req.add_event(id=event_id, active=False)
        await cb.message.edit_text('<b>Мероприятие отправленно в архив.</b>', reply_markup=await kb.admin_panel_kb())
    except Exception as e:
        lg.error(e)
        await cb.message.edit_text('<b>Ошибка при переводе мероприятия в архив.</b>', reply_markup=await kb.admin_panel_kb())


'''ADD QR'''


@router.message(AddQR.name, AdminProtect())
async def add_qr_name(message: types.Message, state: FSMContext):
    await state.update_data(photos=[])
    await state.update_data(name=message.text)
    await message.reply('<b>Введите описание мероприятия:</b>', )
    await state.set_state(AddQR.description)


@router.message(AddQR.description, AdminProtect())
async def add_qr_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.reply('<b>Отправьте фотографии мероприятия:</b>')
    await state.set_state(AddQR.photos)


@router.message(AddQR.photos, AdminProtect())
async def add_qr_photos(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1].file_id
        lg.info(photo)
        data = await state.get_data()
        if len(data['photos']) == 10:
            await message.answer('<b>Максимальное количество фотографий достигнуто! (10)</b>', reply_markup=await kb.continue_date())
            return
        try:
            data['photos'].append(photo)
        except Exception as e:
            lg.error(e)

        await state.update_data(photos=list(set(data['photos'])))
        
        await message.answer('<b>Добавить еще фото?</b>', reply_markup=await kb.try_add_photo_kb())

    else:
        await message.reply('<b>Отправьте фото!</b>', reply_markup=await kb.cancel())


@router.callback_query(F.data == 'add_photo')
async def add_photo_btn(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')

    await cb.message.edit_text('<b>Отправьте фото или медиагруппу мероприятия:</b>',
                               reply_markup= await kb.cancel())
    await state.set_state(AddQR.photos)


@router.callback_query(F.data == 'add_date')
async def add_date_btn(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    data = await state.get_data()

    await cb.message.edit_text('<b>Введите дату проведения мероприятия в формате:\n\n<code>31.12.2024-00:00</code></b>', 
                                reply_markup= await kb.cancel())
    await state.set_state(AddQR.date)


@router.message(AddQR.date, AdminProtect())
async def add_qr_date(message: types.Message, state: FSMContext):
    try:
        
        date = datetime.datetime.strptime(message.text, '%d.%m.%Y-%H:%M')
        await state.update_data(date = date)

        data = await state.get_data()
        caption = lexicon.CARD_INFO.format(data['name'], data['description'], data['date'])
        await message.answer_media_group(
            media=await utils.create_media_group(
                caption=caption,
                list_img_ids=data['photos']),
            )
        await message.answer('<b>Все верно?</b>', reply_markup=await kb.check_all_is_ok())

    except ValueError:
        await message.reply('<b>Неверный формат даты!</b>', reply_markup=await kb.cancel())


@router.callback_query(F.data == 'all_is_ok')
async def back_view(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer('')
    data = await state.get_data()
    started_at = data['date']
    photo_ids = ';'.join(data['photos'])
    data.pop('photos')
    data.pop('date')
    data['photo_ids'] = photo_ids
    data['started_at'] = started_at
    data['id'] = len(await req.get_all_events())
    lg.info(data)
    await req.add_event(**data)
    await cb.message.edit_text('Мероприятие успешно добавлено!', reply_markup=await kb.admin_panel_kb())


@router.callback_query(F.data == 'None')
async def none_btn(message: types.Message, state: FSMContext):
    await message.answer('✨ Конец списка')

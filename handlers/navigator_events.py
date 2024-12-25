from aiogram import Router, types, F, Bot
from database import req

from settings import kb, utils, lexicon


router = Router()


# TODO: see edit media, try to refactor utils.create_media_group
# in list[InputMedia]



@router.callback_query(F.data.startswith('event_'))
async def event_info(cb: types.CallbackQuery, bot: Bot):
    await cb.answer('')

    try: await utils.delete_media_group(cb, bot)
    except Exception as e: pass


    action = cb.data.split('_')[-2]
    events_ids: list[int] = [event.id for event in await req.get_all_events() if event.active]
    num = int(cb.data.split('_')[-1])
    if events_ids.index(num)+1 == len(events_ids):
        print(cb.data)
        print(events_ids)
        
        event = await req.get_event_by_id(num)
        photo_ids = event.photo_ids.split(';')
        caption = lexicon.CARD_INFO.format(event.name, event.description, event.started_at)
        await cb.message.answer_media_group(
        media=await utils.create_media_group(
                caption=caption,
                list_img_ids=photo_ids
                )
        )

        await cb.message.answer(
            text='➖➖➖➖➖➖➖➖➖➖➖➖',
            reply_markup=await kb.end_event_kb(
                len_events=len(events_ids),
                last_id=events_ids[events_ids.index(num)-1],
                event_id=event.id
            )
        )
        return
    if events_ids.index(num) == 0:
        try:
            second_event = [i.id for i in await req.get_all_events() if i.active][1]
        except IndexError:
            second_event = [i.id for i in await req.get_all_events() if i.active][0]

        to_num = events_ids[0]

        event = await req.get_event_by_id(to_num)
        photo_ids = event.photo_ids.split(';')
        caption = lexicon.CARD_INFO.format(event.name, event.description, event.started_at)
        await cb.message.answer_media_group(
        media=await utils.create_media_group(
                caption=caption,
                list_img_ids=photo_ids
                )
        )
        await cb.message.answer(
            text='➖➖➖➖➖➖➖➖➖➖➖➖',
            reply_markup=await kb.start_event_kb(
                len_events=len(events_ids),
                event_id=event.id,
                second_event=second_event
            
            )
        )
        return


    if action == 'next':

        to_num = events_ids[events_ids.index(num) + 1]

            
        
        print(cb.data)
        print(events_ids)
        
        event = await req.get_event_by_id(num)
        photo_ids = event.photo_ids.split(';')
        caption = lexicon.CARD_INFO.format(event.name, event.description, event.started_at)
        await cb.message.answer_media_group(
        media=await utils.create_media_group(
                caption=caption,
                list_img_ids=photo_ids
                )
        )

        await cb.message.answer(
            text='➖➖➖➖➖➖➖➖➖➖➖➖',
            reply_markup=await kb.middle_event_kb(len_events=len(events_ids),
                                                    next_event=to_num,
                                                    now_event=events_ids.index(num)+1,
                                                    prev_event=events_ids[events_ids.index(num) - 1],
                                                    now_event_id=event.id
                                                    )
        )
        return
    elif action == 'prev':
        to_num = events_ids[events_ids.index(num) - 1]

        event = await req.get_event_by_id(num)
        photo_ids = event.photo_ids.split(';')
        caption = lexicon.CARD_INFO.format(event.name, event.description, event.started_at)
        await cb.message.answer_media_group(
        media=await utils.create_media_group(
                caption=caption,
                list_img_ids=photo_ids
                )
        )
        await cb.message.answer(
            text='➖➖➖➖➖➖➖➖➖➖➖➖',
            reply_markup=await kb.middle_event_kb(len_events=len(events_ids),
                                                    next_event=events_ids[events_ids.index(num) + 1],
                                                    now_event=events_ids.index(num)+1,
                                                    prev_event=to_num,
                                                    now_event_id=event.id
                                                    )
        )
        return
  
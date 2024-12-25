from database.models import Event, User, async_session


from sqlalchemy import select, update, null, delete
import logging as lg



""" ADD METHODS"""

async def add_event(**data):
    '''
    '''
    try:
        async with async_session() as session:            
            session.add(Event(**data))
            await session.commit()
    except:
        await session.execute(update(Event).where(Event.id == data['id']).values(**data))
        await session.commit()

async def add_user(**data):
    '''
    '''
    try:
        async with async_session() as session:            
            session.add(User(**data))
            await session.commit()
    except:
        await session.execute(update(User).where(User.user_id == data['user_id']).values(**data))
        await session.commit()



""" GET METHODS """



async def get_user_by_id(id: int) -> User:
    async with async_session() as session:
        s = await session.execute(select(User).where(User.user_id == id))
        return s.scalar_one()

async def get_users() -> list[User]:
    async with async_session() as session:
        try:
            s = await session.execute(select(User))
            return [i for i in s.scalars()]
        except Exception as e:
            lg.error(e)
            return e


async def get_user_event_ids(user_id: int) -> list[str]:
    async with async_session() as session:
        s = (await session.execute(select(User).where(User.user_id == user_id))).scalar_one()
        return s.events_ids.split(',')
     



async def get_first_archive_event() -> Event:
    async with async_session() as session:
        s = (await session.execute(select(Event).where(Event.active == 0).order_by(Event.id.asc()).limit(1))).scalar_one_or_none()
        return s if s else 0
    
async def get_first_active_event() -> Event:
    async with async_session() as session:
        s = (await session.execute(select(Event).where(Event.active == 1).order_by(Event.id.asc()).limit(1))).scalar_one_or_none()
        return s if s else 0
    
async def get_all_events() -> list[Event]:
    async with async_session() as session:
        try:
            s = await session.execute(select(Event))
            return [i for i in s.scalars()]
        except Exception as e:
            lg.info(e)
            return e

async def get_event_by_id(id: int) -> Event:
    async with async_session() as session:
        try:
            s = await session.execute(select(Event).where(Event.id == id))
            return s.scalar_one()
        except Exception as e:
            lg.error(e)
            return e
        




'''  DELETE METHODS  '''

async def delete_event(id: int):
    async with async_session() as session:
        try:
            await session.execute(delete(Event).where(Event.id == id))
            await session.commit()
        except Exception as e:
            lg.error(e)
            await session.rollback()




import datetime




async def add_test_events(**data):
    """
    Пример асинхронной функции для добавления события.
    В реальном приложении здесь будет логика для добавления события в базу данных или другой источник.
    """
    print(f"Добавляю событие: {data['name']} (ID: {data['id']})")
    # await asyncio.sleep(0.1) # Имитация асинхронной операции
    await add_event(**data)
    print(f"Событие {data['name']} (ID: {data['id']}) добавлено.")

data = [
    {'name': 'Летний пикник', 'description': 'Пикник на природе с друзьями.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 6, 15, 12, 0), 'id': 1},
    {'name': 'Мастер-класс по гончарству', 'description': 'Учимся делать глиняные изделия.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 7, 2, 14, 0), 'id': 2},
    {'name': 'Поездка в горы', 'description': 'Поход в горы на выходные.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 7, 20, 8, 0), 'id': 3},
    {'name': 'Вечер кино', 'description': 'Просмотр старых фильмов.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 8, 5, 20, 0), 'id': 4},
    {'name': 'Концерт живой музыки', 'description': 'Наслаждаемся музыкой вживую.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 8, 18, 19, 0), 'id': 5},
    {'name': 'Йога на пляже', 'description': 'Занятия йогой на берегу моря.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 9, 1, 7, 0), 'id': 6},
    {'name': 'Кулинарный мастер-класс', 'description': 'Учимся готовить блюда разных стран.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 9, 15, 16, 0), 'id': 7},
    {'name': 'Экскурсия по городу', 'description': 'Знакомимся с историей города.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 10, 1, 10, 0), 'id': 8},
    {'name': 'Вечеринка в стиле ретро', 'description': 'Веселимся в стиле 80-х.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 10, 19, 21, 0), 'id': 9},
    {'name': 'Поход в театр', 'description': 'Смотрим новую постановку.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 11, 3, 18, 0), 'id':10},
    {'name': 'Прогулка на лошадях', 'description': 'Наслаждаемся природой верхом.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 11, 17, 11, 0), 'id': 11},
    {'name': 'Музейная ночь', 'description': 'Посещаем музеи в ночное время.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 12, 5, 20, 0), 'id': 12},
    {'name': 'Зимний фестиваль', 'description': 'Веселимся на зимнем фестивале.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 12, 25, 15, 0), 'id': 13},
    {'name': 'Новогодний утренник', 'description': 'Праздник для детей с Дедом Морозом.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2024, 12, 31, 10, 0), 'id': 14},
    {'name': 'Урок рисования', 'description': 'Учимся рисовать акварелью.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2025, 1, 10, 17, 0), 'id': 15},
    {'name': 'Поход на каток', 'description': 'Катаемся на коньках.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2025, 1, 25, 13, 0), 'id': 16},
    {'name': 'Книжный клуб', 'description': 'Обсуждаем любимые книги.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2025, 2, 8, 19, 0), 'id': 17},
    {'name': 'Вечер настольных игр', 'description': 'Играем в настольные игры.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2025, 2, 22, 19, 0), 'id': 18},
    {'name': 'Турнир по киберспорту', 'description': 'Соревнуемся в компьютерных играх.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2025, 3, 8, 14, 0), 'id': 19},
    {'name': 'Весенняя ярмарка', 'description': 'Наслаждаемся весенним настроением.', 'photo_ids': 'AgACAgQAAxkBAAITbmdptKauWGBmeXkPVRqkm6OzJyKbAAJ6xzEb68tRUyV-7IkpqLB5AQADAgADeQADNgQ;AgACAgQAAxkBAAITbWdptKZk1yaG2FFTA9Tq7Z4S734yAAJ5xzEb68tRU-tsATsvUqTKAQADAgADeQADNgQ', 'started_at': datetime.datetime(2025, 3, 22, 12, 0), 'id': 20}
]


# import asyncio
# async def main():
#     for item in data:
#         await add_event(**item)

# asyncio.run(main())


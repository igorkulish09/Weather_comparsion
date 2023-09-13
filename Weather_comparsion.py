import aiohttp
import asyncio
import datetime
import logging


# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_weather_data_hgbrasil():
    api_url = "https://api.hgbrasil.com/weather"
    params = {
        "key": "*",
        "woeid": 455825,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            if response.status != 200:
                logger.error(f"Ошибка при запросе данных о погоде с сайта hgbrasil.com: {response.status}")
                return None
            data = await response.json()
            logger.info("Успешно получены данные о погоде с сайта hgbrasil.com")
            return data


async def fetch_weather_data_weatherstack():
    api_url = "https://api.weatherstack.com/current"
    params = {
        "access_key": "**",
        "query": "San Francisco, United States of America",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            data = await response.json()
            return data

async def fetch_weather_data_accuweather():
    api_url = "https://dataservice.accuweather.com/currentconditions/v1/12345"  # Пример идентификатора местоположения
    params = {
        "apikey": "***",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params=params) as response:
            data = await response.json()
            return data


async def main():
    logger.info('Запуск скрипта')
    tasks = [
        fetch_weather_data_hgbrasil(),
        fetch_weather_data_weatherstack(),
        fetch_weather_data_accuweather(),
    ]

    responses = await asyncio.gather(*tasks)

    # Преобразование данных в единый формат и сравнение
    temperatures = []
    for data in responses:
        temperature = None
        if data and data.get("temperature"):
            temperature = data["temperature"]
        temperatures.append(temperature)

    # Вычисление средней температуры
    valid_temperatures = [temp for temp in temperatures if temp is not None]
    if valid_temperatures:
        average_temperature = sum(valid_temperatures) / len(valid_temperatures)
        logger.info(f"Средняя температура: {average_temperature}°C")
    else:
        logger.warning("Нет доступных данных о температуре.")

    logger.info('Завершение выполнения скрипта')

if __name__ == "__main__":
    start = datetime.datetime.now()
    logger.info('Start')
    asyncio.run(main())
    logger.info(f"Done in {datetime.datetime.now() - start}")

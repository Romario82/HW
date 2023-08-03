import aiohttp
import asyncio
import datetime
import platform
import json

def parser(data):
    date = data.get('date')
    exchange_rates = data.get('exchangeRate')
    currencies_data = {}
    for currency_info in exchange_rates:
        currency = currency_info.get('currency')
        if currency in ('EUR', 'USD'):
            sale_rate = currency_info.get('saleRate', currency_info['saleRateNB'])
            purchase_rate = currency_info.get('purchaseRate', currency_info['purchaseRateNB'])
            currencies_data[currency] = {
                'sale': sale_rate,
                'purchase': purchase_rate
            }
    return {date: currencies_data}

async def response24(date):
    async with aiohttp.ClientSession() as session:
        try:
            http_data = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
            async with session.get(http_data) as response:
                result = await response.json()
                if response.status == 200:
                    return result
                else:
                    print(f"Error status: {response.status} for {http_data}")
        except aiohttp.ClientConnectorError as err:
            print(f'Connection error: {http_data}', str(err))

async def main(list_date):
    result_out = []
    for date in list_date:
        result_response24 = await response24(date)
        if result_response24 == None:
            print('No data')
        else:
            result_out.append(parser(result_response24))
    return result_out
#--------------------------------------------------------
def date(day):
    list_date = []
    start_date = datetime.datetime.today()
    for i in range(0, day):
        list_date.append((start_date - datetime.timedelta(days=i)).strftime("%d.%m.%Y"))
    return list_date

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print("Отримати курс USD і EUR")
    day = int(input("Введіть за скільки днів (до 10) -> "))
    if day > 10:
        day = 10
        print("Ви ввели більше 10 днів!")
    list_date = date(day)
    out = asyncio.run(main(list_date))
    print(json.dumps(out, indent=1))




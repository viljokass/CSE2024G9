from apscheduler.schedulers.background import BackgroundScheduler
import requests

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_last_traded_price_fetch():
    last_traded_price = fetch_last_traded_price()
    #db connection here, add last_traded_price to the db

scheduler.add_job(schedule_last_traded_price_fetch, 'interval', hours=1)

def fetch_last_traded_price():
    url = 'https://api.marketdata.app/v1/stocks/quotes/AAPL/'
    response = requests.get(url)
    
    if response.status_code != 200 and response.status_code != 203:
        raise Exception('Failed to fetch last traded price')
    
    data = response.json()

    if 'last' not in data:
        raise Exception('could not find the key: "last" from response')
    
    last_traded_price_list = data.get('last')
    last_traded_price = last_traded_price_list[0]
    return last_traded_price
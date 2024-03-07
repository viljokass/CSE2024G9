from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
import os

scheduler = BackgroundScheduler()
scheduler.start()

start_time = time.time()

def print_time():
    print(f"{os.path.basename(__file__)} running running for {(time.time() - start_time):.2f} seconds")

def schedule_last_traded_price_fetch(db_handler):
    last_traded_price = fetch_last_traded_price()
    db_handler.record_last_traded_price(last_traded_price)

def start_scheduler(db_handler):
    scheduler.add_job(schedule_last_traded_price_fetch, 'interval', hours=1, args=[db_handler])
    scheduler.add_job(print_time, 'interval', seconds=10)

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
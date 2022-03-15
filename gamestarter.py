
import json
import csv
import gate_api
from datetime import timedelta, datetime
from dateutil import relativedelta
from gate_api.exceptions import ApiException, GateApiException

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

end = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
start = end - relativedelta.relativedelta(months=1)

print(f"START: {str(start)} {int(start.timestamp())} | END: {str(end)} {int(end.timestamp())}")
api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)
currency_pair = 'GAME_USDT' # str | Currency pair
limit = 100 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
_from = int(start.timestamp()) # int | Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified (optional)
to = int(end.timestamp()) # int | End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time (optional)
interval = '1d' # str | Interval time between data points (optional) (default to '30m')

try:
    with open("GAMESTARTER_last_6months.csv", "w") as file:
        csv_writer = csv.writer(file)
        # Market candlesticks
        api_response = api_instance.list_candlesticks(currency_pair, _from=_from, to=to, interval=interval)
        csv_writer.writerows(api_response)
        for obj in api_response:
            '''
                - Unix timestamp in seconds
                - Trading volume, in quote currency
                - Close price
                - Highest price
                - Lowest price
                - Open price
            '''
            ts, vol, p_close, p_high, p_low, p_open = obj 
            data = {
                'datetime': str(datetime.fromtimestamp(float(ts))),
                'trading_vol': vol,
                'close_price': p_close,
                'high_price': p_high,
                'low_price': p_low,
                'open_price': p_open
            }
            print(json.dumps(data, indent=2))
except GateApiException as ex:
    print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
except ApiException as e:
    print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)
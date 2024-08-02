import requests
from datetime import datetime, timezone


def numDevices(statusQuery, threshold, dateStr):
    base_url = 'https://jsonmock.hackerrank.com/api/iot_devices/search'
    page = 1
    devices = []

    while True:
        params = {
            'status': statusQuery,
            'page': page
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)

        # Check if device matches the criteria
        for d in data['data']:
            # Convert the UTC milliseconds to a datetime object
            added_date = datetime.fromtimestamp(
                d['timestamp'] / 1000, tz=timezone.utc
            )
            added_month_year = added_date.strftime('%m-%Y')

            if (
                added_month_year == dateStr
                and d['operatingParams']['rootThreshold'] > threshold
            ):
                devices.append(d)

        if page >= data['total_pages']:
            break
        page += 1

    return len(devices)


# Example usage
statusQuery = 'RUNNING'
threshold = 10
dateStr = '05-2021'

total_devices = numDevices(statusQuery, threshold, dateStr)
print('Total number of devices:', total_devices)

# FINAL UPDATE 10-08-23
import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    messages = []
    dates = []
    lines = data.strip().split("\n")
    for line in lines:
        try:
            # Try to parse using 12-hour format first
            pattern_12hr = re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]', line)
            if pattern_12hr:
                date = datetime.strptime(pattern_12hr.group(0), '%d/%m/%y, %I:%M %p')
                message = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s', '', line)
            else:
                # If 12-hour format parsing fails, try 24-hour format
                pattern_24hr = re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', line)
                date = datetime.strptime(pattern_24hr.group(0), '%d/%m/%y, %H:%M - ')
                message = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', '', line)
            
            messages.append(message)
            dates.append(date)
        except (ValueError, AttributeError):
            # If date parsing fails or the pattern is not found, ignore the line
            continue

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'])

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

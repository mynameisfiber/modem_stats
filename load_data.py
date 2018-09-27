import pandas as pd
import json
from os.path import join as path_join


def load_file(fname):
    return [json.loads(line) for line in open(fname)]


def num_coerce(value):
    if ' ' in value:
        value = value.split(' ')[0]
    elif value == '----':
        value = 0
    return pd.to_numeric(value)


def field_map(data, fields, func):
    for f in fields:
        data[f] = func(data[f])
    return data


def parse_status_items(status, num_fields, table_name):
    for s in status:
        t = pd.to_datetime(s['t'], unit='s')
        for item in s[table_name]:
            item['id'] = int(item.pop('field_00').split(' ')[1])
            item = field_map(item, num_fields, num_coerce)
            yield {**item, 't': t}


def parse_status(status):
    down_num_fields = ['Correcteds', 'Uncorrectables', 'DCID',
                       'Freq', 'SNR', 'Octets', 'Power']
    up_num_fields = ['Freq', 'Power', 'Symbol Rate', 'UCID']

    downstreams = pd.DataFrame.from_dict(parse_status_items(
        status,
        down_num_fields,
        'table_00'
    ))
    upstreams = pd.DataFrame.from_dict(parse_status_items(
        status,
        up_num_fields,
        'table_01'
    ))
    downstreams.set_index('t', inplace=True)
    upstreams.set_index('t', inplace=True)
    return downstreams, upstreams


def parse_events_items(events):
    seen_events = set()
    for e in events:
        for item in e['table_00']:
            _id = item['field_00'] + item['field_01']
            if _id not in seen_events:
                seen_events.add(_id)
                yield {
                    't': pd.to_datetime(item['field_00']),
                    'id': int(item['field_01']),
                    'level': int(item['field_02']),
                    'desc': item['field_03'],
                }


def parse_events(events):
    e = pd.DataFrame.from_dict(parse_events_items(events))
    e.set_index('t', inplace=True)
    return e


def parse_speedtest(speedtest):
    s = pd.io.json.json_normalize(speedtest)
    s['timestamp'] = pd.to_datetime(s['timestamp'])
    s.set_index('timestamp', inplace=True)
    return s


def load_data(datadir='./data/'):
    events_raw = load_file(path_join(datadir, "events.json"))
    status_raw = load_file(path_join(datadir, "status.json"))
    speedtest_raw = load_file(path_join(datadir, "speedtest.json"))

    downstream, upstream = parse_status(status_raw)
    events = parse_events(events_raw)
    speedtest = parse_speedtest(speedtest_raw)

    return (downstream, upstream), events, speedtest

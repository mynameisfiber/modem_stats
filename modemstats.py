#!/usr/bin/env python
import requests
from lxml import html
import time
import json


def table_to_dict(table):
    rows = table.findall('.//tr')
    data = []
    fields = []
    unk_fields = 0
    for col in rows[0].findall('.//td'):
        name = col.text
        if name is None:
            name = "field_{0:02d}".format(unk_fields)
            unk_fields += 1
        fields.append(name)
    for row in rows[1:]:
        values = [c.text for c in row.findall('.//td')]
        row_data = dict(zip(fields, values))
        data.append(row_data)
    return data


def get_tables(url):
    data = requests.get(url)
    dom = html.fromstring(data.content)
    return dom.findall('.//table')


if __name__ == "__main__":
    import sys
    tables = get_tables(sys.argv[1])
    data = {}
    for table in tables:
        d = table_to_dict(table)
        if d:
            key = 'table_{:02d}'.format(len(data))
            data[key] = d
    data['t'] = time.time()
    print(json.dumps(data))

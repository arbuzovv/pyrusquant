import json
import datetime as dt
from collections.abc import Iterable

import requests
import pandas as pd

from ..async_parsing import async_get


DFLT_DT_FROM = (dt.datetime.now() - dt.timedelta(30))
DFLT_DT_TO = dt.datetime.now()
MASK_DATE = '%Y-%m-%d'


def get_fields(type_data=None):
    if type_data:
        type_ = f'?type={type_data}'
    else:
        type_ = ''

    url = f'https://api.rusquant.io/gigafields{type_}'
    data_raw = requests.get(url)
    fields = json.loads(data_raw.text)

    return fields


def _get_urls(symbols, field, type_data, fake, reps, trim):
    urls = {}

    for symbol in symbols:
        if type_data == 'candles':
            if fake:
                url = f'https://api.rusquant.io/altergiga?symbol={symbol}&field={field}&trim={trim}&reps={reps}'
            else:
                url = f'https://api.rusquant.io/gigacandles?symbol={symbol}&field={field}&orient=table'
        elif type_data == 'tech':
            if fake:
                url = f'https://api.rusquant.io/altertech?symbol={symbol}'
            else:
                url = f'https://api.rusquant.io/gigatech?symbol={symbol}&field={field}&orient=table'
        else:
            raise ValueError('Param type_data is incorrect')

        urls[symbol] = url

    return urls


def _get(urls):
    df = pd.DataFrame()

    for symbol, url in urls.items():
        try:
            data_raw = requests.get(url)
            if data_raw.status_code != 200:
                print(f'Err request (symbol - {symbol}): Status code - {data_raw.status_code}, URL - {url}')
                continue
            data = json.loads(data_raw.text)
            df = pd.concat([df, pd.DataFrame(data)])
        except Exception as err:
            print(f'Err parsing (symbol - {symbol}):', err)

    return df


def _get_async(urls):
    urls_rev = {v: k for k, v in urls.items()}
    df = pd.DataFrame()
    data = async_get(urls.values())

    for src in data:
        if src['status'] != 200:
            symbol = urls_rev[src["url"]]
            print(f'Err request (symbol - {symbol}): Status code - {src["status"]}, URL - {src["url"]}')
            continue
        data = json.loads(src['data'])
        df = pd.concat([df, pd.DataFrame(data)])

    return df


def get_symbols(symbols, dt_from=DFLT_DT_FROM, dt_to=DFLT_DT_TO, field='close',
                type_data='candles', fake=False, reps=1, trim=0.1, use_async=False):

    if isinstance(dt_from, str):
        dt_from = dt.datetime.strptime(dt_from, MASK_DATE)
    if isinstance(dt_to, str):
        dt_to = dt.datetime.strptime(dt_to, MASK_DATE)

    if isinstance(field, str):
        pass
    elif isinstance(field, Iterable):
        field = ','.join(str(val) for val in field)
    else:
        raise ValueError('Param field is incorrect')

    urls = _get_urls(symbols, field, type_data, fake, reps, trim)
    f_get = _get_async if use_async else _get  # TODO: check async
    df = f_get(urls)

    if df.shape[0] == 0:
        return df

    if dt_from:
        df = df[df['date'] >= dt_from.strftime(MASK_DATE)]
    if dt_to:
        df = df[df['date'] <= dt_to.strftime(MASK_DATE)]

    return df.sort_values(['date', 'symbol'])

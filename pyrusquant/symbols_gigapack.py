import json
import datetime as dt

import requests
import pandas as pd

DFLT_DT_FROM = (dt.datetime.now() - dt.timedelta(30))
DFLT_DT_TO = dt.datetime.now()
MASK_DATE = '%Y-%m-%d'


def get_symbols(symbols, dt_from=DFLT_DT_FROM, dt_to=DFLT_DT_TO, field='close',
                type_data='candles', fake=False, reps=1, trim=0.1):

    df = pd.DataFrame()

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
            raise ValueError('Param type_data is uncorrect')

        try:
            data_raw = requests.get(url)
            data = json.loads(data_raw.text)
            df = pd.concat([df, pd.DataFrame(data)])
        except Exception as err:
            print(f'Err parsing {symbol}:', err)

    if dt_from:
        df = df[df['date'] >= dt_from.strftime(MASK_DATE)]
    if dt_to:
        df = df[df['date'] <= dt_to.strftime(MASK_DATE)]

    return df.sort_values(['date', 'symbol'])

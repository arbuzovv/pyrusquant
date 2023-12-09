# rusquant

### Intro
Rusquant is a package for interaction with alternative data, trading API of different exchanges and brokers. Package provides access to market data for storage, analysis, algorithmic trading, strategy backtesting. Also this is data downloader from different data sources starting from close price to order book and tradelog.

### Installation

```r
pip install pyrusquant
```
### Getting Started

It is possible to import data from a variety of sources with one rusquant
function: `get_symbols()`. For example:

``` r
import pyrusquant
get_symbols(symbols=['SBER', 'LKOH'], fake=True, type_data='candles')
df1 = get_symbols(symbols=['SBER', 'LKOH'], fake=False, type_data='candles')
df2 = get_symbols(symbols=['SBER', 'LKOH'], fake=True, type_data='tech')
df3 = get_symbols(symbols=['SBER', 'LKOH'], fake=False, type_data='tech')
```

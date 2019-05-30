
## Installation 

### pip 

```
pip install PriceIndics
```
 ### From Source (Github)
 
 git clone https://github.com/dc-aichara/Price-Indices.git
 
 cd PriceIndices 
 
 python3 setup.py install
 
 ## Usages 
 
 ```python
from PriceIndices import price, indices

```
## Examples 

```python
>>> price = price()

>>> df = price.get_price('bitcoin', '20130428', '20190529')

>>>print(df.head())

        date    price
0 2019-05-29  8659.49
1 2019-05-28  8719.96
2 2019-05-27  8805.78
3 2019-05-26  8673.22
4 2019-05-25  8052.54

>>> df_bvol = indices.get_bvol_index(df)
>>> print(df_bvol.head())
        date    price  BVOL_Index
0 2019-05-28  8719.96    0.853529
1 2019-05-27  8805.78    0.853605
2 2019-05-26  8673.22    0.849727
3 2019-05-25  8052.54    0.852357
4 2019-05-24  7987.37    0.826548

>>> indices.get_bvol_graph(df_bvol)

"""This will return a plot of BVOL index against time."""

>>> df_rsi = indices.get_rsi(df)

>>> print(df_rsi.tail())
           date   price  price_change   gain   loss  gain_average  loss_average        RS      RSI_1  RS_Smooth      RSI_2
2217 2013-05-02  105.21          7.46   7.46   0.00      1.532143      2.500000  0.612857  37.998229   0.561117  35.943306
2218 2013-05-01  116.99         11.78  11.78   0.00      2.373571      2.175714  1.090939  52.174596   0.975319  49.375257
2219 2013-04-30  139.00         22.01  22.01   0.00      3.945714      1.981429  1.991348  66.570258   1.869110  65.145981
2220 2013-04-29  144.54          5.54   5.54   0.00      3.878571      1.981429  1.957462  66.187226   2.206422  68.812592
2221 2013-04-28  134.21        -10.33   0.00  10.33      3.878571      2.506429  1.547449  60.745050   1.397158  58.283931

>>> indices.get_rsi_graph(df_rsi)

"""This will return a plot of RSI against time."""
```

### License 
[MIT](https://choosealicense.com/licenses/mit/) © [Dayal Chand Aichara](https://github.com/dc-aichara)

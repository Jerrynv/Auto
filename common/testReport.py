# -*- coding: utf-8 -*-

from pandas import DataFrame

data = {'name' : ['A', 'B', 'C'],
        'age':[11,12,13],
        'sex':['man', 'femal', 'man']
}

df = DataFrame(data)
df.to_excel('new.xlsx')
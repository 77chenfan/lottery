# -*- coding: utf-8 -*-
"""
Created on Sun Sep 02 15:23:27 2018

@author: chen
"""






if __name__=="__main__":
    f1=open('mylo.csv')
    data=f1.readlines()
    result = {}
    target="3.18 3.06 2.05 1.62 3.75 4.07".split(' ')
    for ele in data:
        odds=ele.split(',')[6].split('|')
        if(len(odds)==1):
            continue
        tmp=0
        print odds
        for i in xrange(6):
            tmp=tmp + (float(odds[i])-float(target[i]))*(float(odds[i])-float(target[i]))
        if(tmp<1):
            result.update({ele:tmp})
    print result
        
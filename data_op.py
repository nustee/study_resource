# -*- coding:utf-8 -*-
import json
import os
import os.path

def read_total():
    file = open('C:/Users/eric/Desktop/test.csv')
    text = []
    while 1:
        line = file.readline()
        text.append(line)
        if not line:
            break
    print len(text)
    print unicode(text[2], "cp936")

def read_small():
    file = open('C:/Users/eric/Desktop/test.txt')
    context = []
    while 1:
        line = file.readline()
        context.append(line)
        if not line:
            break
    print context[0]
if __name__ == "__main__":
#    read_small()
     read_total()

import argparse
import os
import random
import dill

#Парсинг входа командной строки

parser = argparse.ArgumentParser(description='Data loading')
parser.add_argument('indir', type=str, help='Input dir for data')
parser.add_argument('outmodel', type=str, help='Output dir for model')
args = parser.parse_args()

#/Парсинг входа командной строки

#Считывание файлов

pth = args.indir
pth_to_model = args.outmodel
data = ''
try:
    for filename in os.listdir(pth):
        with open(os.path.join(pth, filename), 'r') as f:
            data += f.read()
except:
    with open(pth, 'r') as f:
        data += f.read()

#/Считывание файлов


#Описание класса модели

class n_gram_model():
    def __init__(self):
        self.data = list()
        self.model = dict()

    def __pre_prepare(self, s: list) -> str:
        i = 0
        while i < len(s):
            if (i > 0) and (s[i] in '!?,.') and (s[i-1] not in '!?,.'):
                s.insert(i, ' ')
                i += 1
            i += 1
        return ''.join(s)

    def __prepare(self, data) -> list:
        data = self.__pre_prepare(list(data))
        up_data = data.lower().split()
        for i in range(0, len(up_data)):
            wrd = up_data[i]
            up_data[i] = ''
            for j in range(0, len(wrd)):
                if (wrd[j] in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя') or (wrd[j] in '!?,.'):
                    up_data[i] += wrd[j]
        return up_data

    def fit(self, data: str):
        self.data = self.__prepare(data)
        strt = False
        prev = None
        for el in self.data:
            if el != '':
                if strt:
                    if prev not in self.model:
                        self.model[prev] = list()
                    self.model[prev].append(el)
                else:
                    strt = True
                prev = el
    
    def generate(self, length: int, pref: str = None) -> str:
        res = None
        sent_end_chance = float(0)
        strt_sent = False
        if pref:
            res = pref
            pref = self.__prepare(pref)[-1]
        else:
            pref = random.choice(list(self.model.keys()))
        while pref in '!?,.':
            pref = random.choice(list(self.model.keys()))
        if not res:
            res = pref.title()
        for _ in range(length):
            if pref in '!?.':
                strt_sent = True
            if (pref not in self.model) or (len(self.model[pref]) == 0):
                while (pref not in self.model) or len(self.model[pref]) == 0:
                    pref = random.choice(list(self.model.keys())) 
            wrd = random.choice(self.model[pref])
            pref = wrd
            if strt_sent:
                wrd = wrd.title()
                strt_sent = False
            if wrd in '!?.,':
                res = res + wrd
            else:
                res = res + ' ' + wrd
            sent_end = (random.random() < sent_end_chance)
            sent_end_chance += 0.05
            if sent_end:
                sent_end_chance = float(0)
                if res[-1] not in '!?.,':
                    wrd = random.choice(list('!?.'))
                    res += wrd
                pref = wrd
        if res[-1] not in '!?.,':
            res += random.choice(list('!?.'))
        return res

#/Описание класса модели

model = n_gram_model()
model.fit(data)

with open(pth_to_model, 'wb') as f:
    dill.dump(model, f)


#python C:/Users\X-Wing\Desktop\Felis\train.py
#python C:/Users/X-Wing/Desktop/Felis/train.py C:/Users/X-Wing/Desktop/dta C:/Users/X-Wing/Desktop/modl/yuki.data
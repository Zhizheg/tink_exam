import argparse
import os
import random
import dill
#Парсинг входа командной строки

parser = argparse.ArgumentParser(description='Model generate config')
parser.add_argument('model', type=str, help='Input dir for model')
parser.add_argument('--prefix', type=str, help='Input for prefix')
parser.add_argument('length', type=int, help='Input for generate length')
args = parser.parse_args()

#/Парсинг входа командной строки

pth_to_model = args.model
prefix = args.prefix
length = args.length

with open(pth_to_model, 'rb') as f:
    model = dill.load(f)

print(model.generate(length, prefix))

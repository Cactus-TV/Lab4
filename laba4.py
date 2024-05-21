#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from datetime import datetime, timedelta
import time
from math import log, sqrt

# # Лабораторная работа №4
# ## Вариант 15

# Используя паттерн Interpreter, реализовать перевод чисел из цифрового представления в текстовое в диапазоне не менее 1 миллиарда. Например, входное число 2381 должно на выходе иметь представление «две тысячи триста восемьдесят один».

# In[35]:


class Expression:
    def interpret(self, context):
        raise NotImplementedError


class TerminalExpression(Expression):
    def __init__(self, data):
        self.data = data

    def interpret(self, context):
        if self.data in context:
            return self.data
        return ""
    
class NonTerminalExpression(Expression):
    def __init__(self, expression1, expression2):
        self.expression1 = expression1
        self.expression2 = expression2

    def interpret(self, context):
        return self.expression1.interpret(context) and self.expression2.interpret(context)


class Interpreter:
    def __init__(self):
        self.units = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
        self.teens = ["", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
        self.tens = ["", "десять", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
        self.hundreds = ["", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]
        self.thousands = ["", "тысяча", "миллион", "миллиард"]

    def interpret(self, number):
        number = str(number)[::-1]
        words = []

        for i in range(0, len(number), 3):
            unit = TerminalExpression(self.units[int(number[i])])
            ten = TerminalExpression(self.tens[int(number[i+1])]) if i+1 < len(number) else TerminalExpression("")
            hundred = TerminalExpression(self.hundreds[int(number[i+2])]) if i+2 < len(number) else TerminalExpression("")
            
            if i // 3 < len(self.thousands):
                thousand = TerminalExpression(self.thousands[i // 3])
                words.append(thousand)
                
            if ten.data == "десять" and unit.data != "":
                teen = TerminalExpression(self.teens[int(number[i])])
                words.append(teen)
                ten = TerminalExpression("")
                unit = TerminalExpression("")

            words.append(unit)
            words.append(ten)
            words.append(hundred)

        return " ".join(word.interpret(word.data) for word in words[::-1] if word.data)
    
interpreter = Interpreter()


# In[36]:


print(interpreter.interpret(2381))


# In[37]:


import random

for i in range(100):
    temp = random.randint(0, 10000000000)
    print(temp, interpreter.interpret(temp))

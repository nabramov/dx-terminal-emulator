# -*- coding: utf-8 -*-

import plugins.base
import re

class plugin(plugins.base.baseplugin):
    header = """Адресные кнопки :
=================================
  Nk Порт      Под регистром
---------------------------------"""
    footer = "================================="
    helper = """Команда 'содержимое' адресных кнопок CD-линий пультов.
  Формат:

    dcdk <CD> <Nk/Nk от> [<Nk до]

  где: CD - для какой CD;
       <Nk/Nk от> - для какой кнопки, или 1-ой для перечисления;
       <Nk до>    - до какой для перечисления."""  
            
    number = 160
    number2 = 162
    name = 'dcdk'
    max_line = 18
    def_param = [{'name':'s0','default':0},
                 {'name':'s1','default':0},
                 {'name':'s2','default':0},
                 {'name':'s3','default':0}]
    
    add_param =  [{'name':'n0','default':' '},
                 {'name':'n1','default':' '},
                 {'name':'n2','default':' '},
                 {'name':'n3','default':' '}]
   # write_param = {1:'f',2:'p_tn',3:'p_ip',4:'d',5:'s',6:'pr',7:'qs',8:'ci',9:'al',10:'hf',11:'p1f',12:'def',13:'gr',14:'pf',15:'ps',16:'pc'}   
    format_line = " {0:>2} {1:<10} {2}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы DSS1. """
        try: 
            start_line = cmd[0]
            if start_line != '?':
                start_line = int(cmd[0])
                if start_line >= plugin.max_line: raise
                try:
                    end_line = int(cmd[1]) 
                except IndexError:
                    end_line = start_line      
        except: 
            start_line = 0
            end_line = plugin.max_line-1 # Всегда выводим все строки если не указан диапазон
               
        if start_line == '?': 
            print(plugin.helper)
            return
        print(plugin.header)
        param_count = len(plugin.def_param)
        # выводим 18 линий для каждой CD линии. 0 CD c 0 по 17 и т.д.
        line2 = start_line * 18
        key_cnt = 0
        for line in range(line2, line2+plugin.max_line):
            for i in range(param_count):
                p = []
                key_cnt += 1   
                p.append(key_cnt) # добавляем номер строки             
                key = plugin.def_param[i]['name']
                key2 = plugin.add_param[i]['name']
                try:
                    v = param[cl][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']                   
                try:
                    v2 = param[cl][plugin.number2][line][key2]
                except:
                    v2 = plugin.add_param[i]['default'] 
                # s -keys     
                if v > 0:
                    m1 = 0xFF
                    m2 = 0xF00
                    m3 = 0x7000
                    po = (v & m1)
                    ccl = (v & m2)>>8
                    dx = (v & m3)>>12
                    p.append('{}{},{:0>3}'.format(dx,ccl,po))
                else:
                    p.append('-');
                # n -keys
                if v2 != ' ':
                    d = re.sub('[FE0]','',v2)
                    d1 = re.sub('A','0',d)
                    d2 = re.sub('B','*',d1)
                    p.append(d2) 
                else:
                    p.append('-');                   
                print(plugin.format_line.format(*p))
        print(plugin.footer)
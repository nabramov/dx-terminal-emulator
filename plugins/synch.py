# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Внешняя синхронизация:
==========================================================================
    ---  1 ---  ---  2 ---  ---  3 ---  ---  4 ---  ---  5 ---  ---  6 ---
 DX Ф  П Кл. К  Ф  П Кл. К  Ф  П Кл. К  Ф  П Кл. К  Ф  П Кл. К  Ф  П Кл. К
--------------------------------------------------------------------------
  0 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
--------------------------------------------------------------------------"""
    footer = "=========================================================================="
    helper = """Таблица 'Внешняя синхронизация':
 Параметры:
   1,5,9,13,17,21   - флаги вкл./выкл. как источники синхронизации;
   2,6,10,14,18,22  - приоритет каналов в Кластерах.
   3,7,11,15,19,23  - номера Кластеров;
   4,8,12,16,20,24  - номера каналов в Кластерах.
                      (Clock = C)."""
      
    number = 58
    name = 'synch'
    max_line = 8
    def_param = [{'name':'f0','default':0,0:'-',1:'+'},
                 {'name':'p0','default':'0'},
                 {'name':'c0','default':'0'},
                 {'name':'n0','default':'0'},
                 {'name':'f1','default':0,0:'-',1:'+'},
                 {'name':'p1','default':'0'},
                 {'name':'c1','default':'0'},
                 {'name':'n1','default':'0'},
                 {'name':'f2','default':0,0:'-',1:'+'},
                 {'name':'p2','default':'0'},
                 {'name':'c2','default':'0'},
                 {'name':'n2','default':'0'},
                 {'name':'f3','default':0,0:'-',1:'+'},
                 {'name':'p3','default':'0'},
                 {'name':'c3','default':'0'},
                 {'name':'n3','default':'0'},
                 {'name':'f4','default':0,0:'-',1:'+'},
                 {'name':'p4','default':'0'},
                 {'name':'c4','default':'0'},
                 {'name':'n4','default':'0'},
                 {'name':'f5','default':0,0:'-',1:'+'},
                 {'name':'p5','default':'0'},
                 {'name':'c5','default':'0'},
                 {'name':'n5','default':'0'}]
    
    write_param = {1:'f0',2:'p0',3:'c0',4:'n0',5:'f1',6:'p1',7:'c1',8:'n1',9:'f2',10:'p2',11:'c2',12:'n2', \
                   13:'f3',14:'p3',15:'c3',16:'n3',17:'f4',18:'p4',19:'c4',20:'n4',21:'f5',22:'p5',23:'c5',24:'n5'}
    
    format_line = "{0:>3} {1}  {2}  {3}  {4}  {5}  {6}  {7}  {8}  {9}  {10}  {11}  {12}  {13}  {14}  {15}  {16}  {17}  {18}  {19}  {20}  {21}  {22}  {23}  {24}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """   """
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
        for line in range(start_line, end_line +1):
            p = []
            p.append(line) # добавляем номер строки
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
                if key.startswith('f'):    
                    p.append(plugin.def_param[i][v])
                else:
                    p.append(v) 
            print(plugin.format_line.format(*p))
        print(plugin.footer)
        
    def write(self, param, cl, cmd):
        tab = {}
        lines = {}
        p = {}
        line_number = cmd[0]
        param_number = cmd[1]
        param_count = len(plugin.def_param)
        try:
            value = cmd[2]
        except:
            print("Ошибка значения параметра")
        try:   
            ln = int(line_number)
            if ln >= plugin.max_line: raise ValueError("Ошибка параметра")
        except:
            print('Ошибка параметра Nпп(0) не может быть',line_number)
            return
        try:
            pn = int(param_number)
            if pn < 1 or pn > param_count : raise
        except:
            print('Ошибка параметра в диапазоне(1-8) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key.startswith('f'):
            if value == '-': 
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == '+':
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        elif key.startswith('p'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 6: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        elif key.startswith('c'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 10: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        elif key.startswith('n'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 4: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
            else:
                print("Недопустимое значение параметра:", param_number)
                return  
        print("Таблица 'Synch'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """CE в системе:
====================================================
     ---  Кластеры   --- -Центры- Типы конфиг.
 DX  0  1  2  3  4  5  6   8  9   CE в DX-ах
----------------------------------------------------
  0  1  2  3  4  5  6  7   8  9   10
----------------------------------------------------"""
    footer = '===================================================='
    helper = """Параметры:
  0. 'DX' - в каком DX;
  1,2,...9 '0,1,...6,8,9' - кластеры и центры;
  10. - типы конфигурации:
    'S' - стандартная (аfaaffa.cc);
    'D' - двойная     (a.a.......);
    'F' - коммутатор  (fffffff.cc)."""
      
    number = 48
    name = 'ce'
    max_line = 8
    def_param = [{'name':'cl0','default':0,0:'-',1:'+'},
                 {'name':'cl1','default':0,0:'-',1:'+'},
                 {'name':'cl2','default':0,0:'-',1:'+'},
                 {'name':'cl3','default':0,0:'-',1:'+'},
                 {'name':'cl4','default':0,0:'-',1:'+'},
                 {'name':'cl5','default':0,0:'-',1:'+'},
                 {'name':'cl6','default':0,0:'-',1:'+'},
                 {'name':'ce8','default':0,0:'-',1:'+'},
                 {'name':'ce9','default':0,0:'-',1:'+'}, 
                 {'name':'ct','default':0,0:'(S)Стандартная',1:'(D)Двойная',5:'(F)Коммутатор'}]
    
    write_param = {1:'cl0',2:'cl1',3:'cl2',4:'cl3',5:'cl4',6:'cl5',7:'cl6',8:'ce8',9:'ce9',10:'ct'}
    
    format_line = "{0:>3}{1:>3}{2:>3}{3:>3}{4:>3}{5:>3}{6:>3}{7:>3} {8:>3}{9:>3}   {10:<17}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы CE. Для данной таблицы параметр cl 
        игнорируется т.к таблица является глобальной"""
        try: 
            start_line = cmd[0]
            if start_line != '?':
                start_line = int(cmd[0])
        except: 
            start_line = 0
        try: 
            end_line = int(cmd[1])
        except IndexError: 
            end_line = start_line
            
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
                p.append(plugin.def_param[i][v])  
            print(plugin.format_line.format(*p))
        print(plugin.footer)
        
    def write(self, param, cl, cmd):
        tab = {}
        lines = {}
        p = {}
        line_number = cmd[0]
        param_number = cmd[1]
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
            if pn < 1 or pn > 10 : raise
        except:
            print('Ошибка параметра в диапазоне(1-10) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'ct':
            if value == 'd': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            elif value == 's':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == 'f': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 5
            else: 
                print("Ошибка параметра:", param_number)
                return
        else:
            if value == '-': 
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == '+': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            else:
                print("Ошибка параметра:", param_number)
                return
        #print(param)
        print("Таблица 'CE'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))

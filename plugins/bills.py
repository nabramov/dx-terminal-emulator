# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Тарификационные шаблоны:
============================
 Nпп  Шаблон
----------------------------
   0  1
----------------------------"""
    footer = "============================"
    helper = """Таблица 'Тарификационные шаблоны':
 Параметры:
   1. 'Шаблон' - значение (цифры,*,?)."""  
    number = 64
    name = 'bills'
    max_line = 32
    def_param = [{'name':'s','default':''}]
    
    write_param = {1:'s'}
    
    format_line = "{0:>4}  {1:<17}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы HLSPD."""
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
            print_line = False
            p.append(line) # добавляем номер строки
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                    print_line = True
                except:
                    v = plugin.def_param[i]['default']
                if v != '':
                    v = str(v)
                    s = ''
                    for c in range(0, len(v), 2):
                        s += '%02x' % (ord(v[c])) 
                    p.append(s)             
            if print_line: print(plugin.format_line.format(*p))
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
            if pn < 1 or pn > 5: raise
        except:
            print('Ошибка параметра в диапазоне(1-5) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 's':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                if value.isdigit():
                    s = ''
                    for c in range(len(value)):
                        s += str(ord(value[c]))
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = s
        else:
            print("Недопустимое значение параметра:", param_number)
            return    
       
        print(param)    
        print("Таблица 'BILLS'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
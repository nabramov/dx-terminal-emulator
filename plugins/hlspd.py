# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """'Логические каналы' УГС для динамических диспетчеров:
=============================
       Мастер   -Кластера-   
 Nпп   порт     1  2  3  4   
-----------------------------
   0   1        2  3  4  5   
-----------------------------"""
    footer = "============================="
    helper = """Таблица 'Аварийный порт' и вызовы:
 Параметры:
   1. 'Мастер порт' -  Мастер-порт (к,порт);
   2,3,4,5 - Кластера логического канала;"""  
    number = 19
    name = 'hlspd'
    max_line = 8
    def_param = [{'name':'mp','default':'-'},
                 {'name':'k1','default':'-'},
                 {'name':'k2','default':'-'},
                 {'name':'k3','default':'-'},
                 {'name':'k4','default':'-'}]
    
    write_param = {1:'mp',2:'k1',3:'k2',4:'k3',5:'k4'}
    
    format_line = "{0:>4}   {1:<6}  {2:>2} {3:>2} {4:>2} {5:>2}" 
     
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
            p.append(line) # добавляем номер строки
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
                if key == 'mp':
                    if v != '-':
                        port = (v & 0xFF)
                        cluster = (v & 0xF00)>>8
                        dx = (v & 0x7000)>>12 
                        p.append('{}{},{:0>3}'.format(dx,cluster,port))
                    else:
                        p.append(v)
                if key.startswith('k'):
                    if v != '-':
                        v -= 128
                        p.append('{:0>2}'.format(v))
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
        if key == 'mp':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                sep_pos = value.find(',')
                if sep_pos > 0:
                    port = int(value[sep_pos+1:])
                    cluster = int(value[1])<<8
                    dx = int(value[0])<<12
                    result = 0x8000 + dx + cluster + port
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = result
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return    
        elif key.startswith('k'):
            if value.isdigit():
                v = int(value)+128
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
            elif value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        print(param)    
        print("Таблица 'HLSPD'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
    
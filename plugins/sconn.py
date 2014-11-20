# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """============================================
         --- От кого ----  --- К кому -----
  N Вкл. Порт   Фр Резерв  Порт   Фр Резерв
--------------------------------------------
  0  1   2       3 4       5       6 7
--------------------------------------------"""
    footer = "============================================"
    helper = """Таблица 'Полупостоянные соединения':
 Параметры:
  0. 'N'    - номер;
  1. 'Вкл.' - включено или выключено;
    Для Ведущего/Ведомого:
  2,5 'Порт'   - порт (dk,nnn);
  3,6 'Фр'     - флаг резервa;
  4,7 'Резерв' - порт резерва;"""  
    number = 135
    name = 'sconn'
    max_line = 41
    def_param = [{'name':'f','default':0,0:'-',1:'+'},
                 {'name':'m','default':'-'},
                 {'name':'mf','default':0,0:'-',1:'+'},
                 {'name':'rm','default':'-'},
                 {'name':'s','default':'-'},
                 {'name':'sf','default':0,0:'-',1:'+'},
                 {'name':'rs','default':'-'}]
    
    write_param = {1:'f',2:'m',3:'mf',4:'rm',5:'s',6:'sf',7:'rs'}
    
    format_line = "{0:>3}  {1}   {2:<6}  {3} {4:<6}  {5:<6}  {6} {7:<6}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы sconn."""
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
                if key == 'm' or key == 'rm' or key == 's' or key == 'rs':
                    if v != '-':
                        port = (v & 0xFF)
                        cluster = (v & 0xF00)>>8
                        dx = (v & 0x7000)>>12 
                        p.append('{}{},{:0>3}'.format(dx,cluster,port))
                    else:
                        p.append(v)
                if key =='f' or key == 'mf' or key == 'sf':
                    p.append(plugin.def_param[i][v])                
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
            if pn < 1 or pn > 7: raise
        except:
            print('Ошибка параметра в диапазоне(1-7) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'm' or key == 'rm' or key == 's' or key == 'rs':
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
        elif  key =='f' or key == 'mf' or key == 'sf':
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
        #print(param)    
        print("Таблица 'SCONN'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
    
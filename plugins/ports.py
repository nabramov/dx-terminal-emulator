# -*- coding: utf-8 -*-

import plugins.base
import re

class plugin(plugins.base.baseplugin):
    header = """Статические Переходы:
======================================================
          --- Def_вызов  --  -- Виртуальный --
   Порт   Порт/G/D Донабор   Порт/G/D Донабор  ГПВ Зв
------------------------------------------------------
    0      1       2          3       4          5  6
------------------------------------------------------"""
    header1 = "- ИКМ-порты ------------------------------------------"
    footer = "======================================================"
    helper = """Таблица 'Статические Переходы':
  Параметры:
    0. 'Порт' - для какого порта;
    1. 'Порт/Группа/DECT_TA' - для вызова по умолчанию;
    2. 'Донабор'             - донабор для него;
    3. 'Порт/Группа/DECT_TA' - для виртуального вызова;
    4. 'Донабор'             - донабор для него;
    5. 'ГПВ' - группа 'перехвата вызова';
    6. 'Зв'  - флаг 'задержанного' вызова по умолчанию."""  
            
    number = 14
    name = 'ports'
    max_line = 320 #192
    def_param = [{'name':'ds','default':0,0:'-'},
                 {'name':'dn','default':0,0:'-'},
                 {'name':'vs','default':0,0:'-'},
                 {'name':'vn','default':0,0:'-'},
                 {'name':'rg','default':0,0:'-'},
                 {'name':'dd','default':0,0:'-',1:'+'}]
    
    write_param = {1:'ds',2:'dn',3:'vs',4:'vn',5:'rg',6:'dd'}   
    format_line = "{0:>9}  {1:<6}  {2:<8}   {3:<6}  {4:<8}   {5:<1}  {6}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы PORTS. """
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
        counter = 0
        for line in range(start_line, end_line +1):
            p = []
            if counter == 32 : counter = 0
            if line < 128:
                port_hi = line//32
                if (cl == '01') or (cl == '04') or (cl == '05'): # PCM-4                 
                    port_lo = counter
                else:
                    port_lo = counter//2
            if line == 128: 
                if (cl == '01') or (cl == '04') or (cl == '05'):
                    break # PCM-4
                print(plugin.header1)
            if line >= 192: break
            if line >= 128:
                port_hi = (line-128)//32
                port_lo = counter
            port_ = '{}-{:0>2}'.format(port_hi,port_lo)
            p.append('{},{}'.format(line, port_)) # добавляем номер строки и номер порта
            counter += 1
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param[cl][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
                if key == 'dd':     
                    p.append(plugin.def_param[i][v])
                elif key == 'ds' or key == 'vs':
                    t = int(v)
                    m1 = 0xFF
                    m2 = 0xF00
                    m3 = 0x7000
                    po = (t & m1)
                    ccl = (t & m2)>>8
                    dx = (t & m3)>>12
                    p.append('{}{},{:0>3}'.format(dx,ccl,po))
                else:
                    if v == 0:
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
        try:
            value = cmd[2]
        except:
            print("Ошибка значения параметра")
        try:   
            ln = int(line_number)
            if ln >= plugin.max_line: raise ValueError("Ошибка параметра")  
        except ValueError:
            print('Ошибка параметра Nпп(0) не может быть',line_number)
            return
        try:
            pn = int(param_number)
            if pn < 1 or pn > 6 : raise
        except:
            print('Ошибка параметра в диапазоне(1-6) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'dd':
            if value == '-':
                try:
                    del param[cl][plugin.number][ln][key]
                except:
                    pass
            elif value == '+': 
                param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1 
            else:
                print("Недопустимое значение параметра:", value)
                return 
        elif key == 'ds' or key == 'vs':
            if value == '-':
                try:
                    del param[cl][plugin.number][ln][key]
                except:
                    pass
            else:
                d = re.sub('[-]',',',value).split(',')           
                _value = 32768
                _value += int(d[0][0])<<12
                _value += int(d[0][1])<<8
                _value += int(d[1])
                param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = _value 
        elif key == 'dn' or key == 'vn':
            if value.isdigit():
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = '{:<8}'.param(value) 
            else:
                if value == '-':
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", value)
                    return 
        elif key == 'rg':
            if value.isdigit():
                v = int(value)
                if v >= 0 and v < 10:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return
            elif value == '-':
                try:
                    del param[cl][plugin.number][ln][key]
                except:
                    pass
            else:
                print("Недопустимое значение параметра:", value)
                return 
        print("Таблица 'PORTS'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))

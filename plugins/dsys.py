# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Тип и параметры DX_Net:
==============================================
 Nпп Тип Архитектуры DX_Net         DX для LL
----------------------------------------------
   0 1                                  2
----------------------------------------------"""
    footer = '=============================================='
    helper = """ Таблица 'Тип и параметры DX_Net':
 Параметры:
  1.'Тип' - тип Архитектуры Системы для DX_Net:
     - (S)  Без DX_NET (одиночная);
     - (L)  Большая (друг в друга);
     - (LL) Линейно-протяженная.

  2. 'DX для LL' - номер DX, как центра для LL."""  
    number = 52
    name = 'dsys'
    max_line = 1
    def_param = [{'name':'t','default':0,0:'Без DX_NET (одиночная)',1:'(L) Большая друг в друга',3:'(LL) Линейно-протяженная'},
                 {'name':'dx','default':'0'}]
    
    write_param = {1:'t',2:'dx'}
    
    format_line = "{0:>4} {1:<34} {2}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы DSYS. Для данной таблицы параметры cl и end_line
        игнорируются т.к таблица имеет всего одну стоку и является глобальной"""
        try: 
            start_line = cmd[0]
            if start_line != '?':
                start_line = int(cmd[0])
        except: 
            start_line = 0
            
        if start_line == '?': 
            print(plugin.helper)
            return
        print(plugin.header)
        param_count = len(plugin.def_param)
        p = []
        p.append('0') # добавляем номер строки
        for i in range(param_count):
            key = plugin.def_param[i]['name']
            try:
                v = param['g'][plugin.number][0][key]
            except:
                v = plugin.def_param[i]['default'] 
            if key == 't':
                p.append(plugin.def_param[i][v])
            else: p.append(v)  
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
            if pn < 1 or pn > 2 : raise
        except:
            print('Ошибка параметра в диапазоне(1-10) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 't':
            if value == 's':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == 'l': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            elif value == 'll': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 3 
            else:
                print("Недопустимый параметр:", value)
                return 
        else:                
            if value.isdigit():
                v = int(value)
                if v < 10 and v > 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Параметр {} не может иметь значение: {}".format(param_number,value))
                    return
            else:
                print("Параметр {} не может иметь значение: {}".format(param_number,value))
                return
        #print(param)
        print("Таблица 'DSYS'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
        
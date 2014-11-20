# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Связи в Большой конфигурации (L):
=============================
          Начало    Конец
 Nпп Вкл. DK Канал  DK Канал
-----------------------------
   0   1   2    3    4    5
-----------------------------"""
    footer = '============================='
    helper = """Таблица 'Связи в Большой конфигурации (L)':
 Параметры:
   1.  'Вкл.'  - флаг 'выкл./вкл.' связь;
   2.4 'DK'    - номер DX (D) и номер кластера (К), 'начала'/'конца';
   3.5 'Канал' - номер ИКМ-канала в кластере 'начала'/'конца'."""  
    number = 53
    name = 'llink'
    max_line = 30
    def_param = [{'name':'f','default':0,0:'-',1:'+'},
                 {'name':'dx1','default':'0'},
                 {'name':'cl1','default':'0'},
                 {'name':'ch1','default':'0'},
                 {'name':'dx2','default':'0'},
                 {'name':'cl2','default':'0'},
                 {'name':'ch2','default':'0'}]
    
    write_param = {1:'f',2:'dx1',3:'ch1',4:'dx2',5:'ch2'}
    
    format_line = "{0:>4}   {1}  {2:0>2}   {3:>2}   {4:0>2}   {5:>2}" 
     
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
            flag = False # Флаг, устанавливаемый, если в строке хоть один параметр не по умолчанию
            for i in range(param_count):
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                    flag = True
                except:
                    v = plugin.def_param[i]['default']
                if key == 'f': 
                    p.append(plugin.def_param[i][v])
                elif key.startswith('cl'):
                    z = str(v)
                    p[-1] += z
                elif key.startswith('dx'):
                    p.append(str(v)) 
                else: p.append(v)  
            if flag: print(plugin.format_line.format(*p)) # выводим строку, только в том случае если в ней есть измененые параметры
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
            if pn < 1 or pn > 5 : raise
        except:
            print('Ошибка параметра в диапазоне(1-5) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'f':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == '+': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1 
            else:
                print("Недопустимый параметр:", value)
                return 
        elif key.startswith('dx'):
            if value.isdigit():
                index = key[2]
                d_param = value[0]
                c_param = value[1]
                try:
                    if d_param < 8 and c_param < 7:
                        if d_param > 0:
                            param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = d_param
                        else:
                            try:
                                del param['g'][plugin.number][ln][key]
                            except:
                                pass
                        if c_param > 0:
                            param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)['cl'+index] = c_param
                        else:
                            try:
                                del param['g'][plugin.number][ln]['cl'+index]
                            except:
                                pass
                    else: raise NameError(value)
                except NameError:
                    print("DK задан в неверном формате:", value)
                    return
            else:
                print("Параметр {} не может иметь значение: {}".format(param_number,value))
                return
        elif key.startswith('ch'):
            if value.isdigit():
                v = int(value) 
                if v > 0 and v < 3: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:    
                    print("Недопустимый параметр:", value)
                    return   
            else:
                print("Параметр {} не может иметь значение: {}".format(param_number,value))
                return           
        else:                
            pass
        #print(param)
        print("Таблица 'LLINK'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
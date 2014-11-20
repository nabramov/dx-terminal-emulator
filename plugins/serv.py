# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Категории Сервисов:
=========================
 Nпп - Группы сервисов -
-------------------------
   0   1   2   3   4   5
-------------------------"""
    footer = "========================="
    helper = """Таблица 'Категории Сервисов':
 Параметры:
   1. Обратный вызов;
   2. Вмешательство;
   3. Об'единение, переключение;
   4. Переадресация;
   5. Категория 'Оператора';"""  
    number = 32
    name = 'serv'
    max_line = 1
    def_param = [{'name':'g1','default':'0'},
                 {'name':'g2','default':'0'},
                 {'name':'g3','default':'0'},
                 {'name':'g4','default':'0'},
                 {'name':'g5','default':'0'}]
    
    write_param = {1:'g1',2:'g2',3:'g3',4:'g4',5:'g5'}
    
    format_line = "{0:>4}{1:>4}{2:>4}{3:>4}{4:>4}{5:>4}" 
     
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
            if key.startswith('g'):
                if int(v) < 256 :
                    p.append(v)
            else:
                p.append('???') 
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
            if pn < 1 or pn > 5 : raise
        except:
            print('Ошибка параметра в диапазоне(1-10) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key.startswith('g'):                
            if value.isdigit():
                v = int(value)
                if v < 256 and v > 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = int(value)
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
            else:
                print("Параметр {} не может иметь значение: {}".format(param_number,value))
                return
        #print(param)
        print("Таблица 'SERV'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
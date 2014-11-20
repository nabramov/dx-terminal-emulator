# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Лимиты 'вывода из сервиса':
===========================================================
     Тип                  0 - 'Мягкие'       1- 'Жесткие'
  N  устройста  Набор   мин   час сутки    мин   час сутки
-----------------------------------------------------------
  0               1       2     3     4      5     6     7
-----------------------------------------------------------"""
    footer = " ==========================================================="
    helper = """Таблица 'Лимиты вывода из сервиса':
 Параметры:
  0. 'N'     - типы устройств;

  1. 'Набор' - используемый набор(0/1);
  2,3,4. 'Мягкие'  - набор мягких лимитов;
  5,6,7. 'Жесткие' - жесткие;"""
      
    number = 99
    name = 'limit'
    max_line = 23
    def_param = [{'name':'t','default':'0'},
                 {'name':'l00','default':'0'},
                 {'name':'l01','default':'0'},
                 {'name':'l02','default':'0'},
                 {'name':'l10','default':'0'},
                 {'name':'l11','default':'0'},
                 {'name':'l12','default':'0'}]
    
    write_param = {1:'t',2:'l00',3:'l01',4:'l02',5:'l10',6:'l11',7:'l12'}
    
    format_line = "  {0:>3}  {1:<7} {2:>4}   {3:>5} {4:>5} {5:>5}  {6:>5} {7:>5} {8:>5}" 
    
    add_param = {0:'не исп.',1:'Falc_1',2:'Falc_2',3:'Idec',4:'MUSAC',5:'MTSL',6:'не исп.',7:'не исп.',8:'Soft', \
                 9:'Board',10:'M51',11:'OBCI',12:'не исп.',13:'ExtS',14:'Ring',15:'ADSP',16:'TRing',17:'не исп.', \
                 18:'не исп.',19:'не исп.',20:'Pult',21:'не исп.',22:'duslic'}
    
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """   """
        try: 
            start_line = cmd[0]
            if start_line != '?':
                start_line = int(cmd[0])
        except: 
            start_line = 0
        try: 
            end_line = int(cmd[1])
        except IndexError: 
            end_line = plugin.max_line-1 #
            
        if start_line == '?': 
            print(plugin.helper)
            return
        print(plugin.header)
        param_count = len(plugin.def_param)
        for line in range(start_line, end_line +1):
            p = []
            p.append(line) # добавляем номер строки
            p.append(plugin.add_param[line]) # добавляем описание типа устройства для данной линии
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
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
            if pn < 1 or pn > 7: raise
        except:
            print('Ошибка параметра в диапазоне(1-7) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 't':
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 2: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                if v == 0:
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
        else: 
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 16960:
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
            
        print("Таблица 'Limit'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
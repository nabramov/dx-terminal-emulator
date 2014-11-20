# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Перевод времени зима/лето:
============================================================================
------------|--------Зимний перевод--------|----------Летний перевод--------
            |                              |
  N  Перевод Месяц День Час Мин Увел./Умен.  Месяц День Час Мин Увел./Умен.
----------------------------------------------------------------------------
  0     1       2    3    4   5      6          7    8    9  10     11
----------------------------------------------------------------------------"""
    footer = "============================================================================"
    helper = """Таблица 'Перевод времени зима/лето':
  Параметры:
  1. Перевод времени: (-) - выкл., (+) - американский стандарт,
                      RUS - российский стандарт;
---------------------------------------------------------
  Параметры со 2 оп 6 относятся к зимнему переводу 
  2. 'Месяц' - номер месяца (1-12);
  3. 'День'  - номер дня (1-31);
  4. 'Час'   - время в часах;
  5. 'Мин'   - время в минутах;
  6. 'Увел./Умен.' - направление перевода.
      Для увеличения/уменьшения времени.
---------------------------------------------------------
  Параметры со 7 оп 11 относятся к летнему переводу 
  7. 'Месяц' - номер месяца (1-12);
  8. 'День'  - номер дня (1-31);
  9. 'Час'   - время в часах;
  10.'Мин'   - время в минутах;
  11.'Увел./Умен.' - направление перевода.
      Для увеличения/уменьшения времени.
---------------------------------------------------------
      Внимание! Перевод времени должен отличаться 
      хотя бы  на один день."""
      
    number = 71
    name = 'zl'
    max_line = 1
    def_param = [{'name':'f1','default':0,0:'-',1:'+'},
                 {'name':'mz','default':'0'},
                 {'name':'dz','default':'0'},
                 {'name':'thz','default':'0'},
                 {'name':'tmz','default':'0'},
                 {'name':'f3','default':0,0:'-',1:' '},
                 {'name':'ml','default':'0'},
                 {'name':'dl','default':'0'},
                 {'name':'thl','default':'0'},
                 {'name':'tml','default':'0'},
                 {'name':'f4','default':0,0:'-',1:' '}]
    
    write_param = {1:'f1',2:'mz',3:'dz',4:'thz',5:'tmz',6:'f3',7:'ml',8:'dl',9:'thl',10:'tml',11:'f4'}
    
    format_line = "  {0}     {1} {2:>7} {3:>4} {4:>4} {5:>3}      {6} {7:>10} {8:>4} {9:>4} {10:>3}      {11}" 
    
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """   """
        try:
            start_line = cmd[0]
        except:
            start_line = 0  
            
        if start_line == '?': 
            print(plugin.helper)
            return
        print(plugin.header)
        param_count = len(plugin.def_param)
        p = []
        p.append(0) # добавляем номер строки
        for i in range(param_count):              
            key = plugin.def_param[i]['name']
            try:
                v = param['g'][plugin.number][0][key]
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
            if pn < 1 or pn > 11: raise
        except:
            print('Ошибка параметра в диапазоне(1-11) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key.startswith('f'):
            if value == '+':
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            elif value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        elif key.startswith('m'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 13:  # проверка на соответствие номеру месяца
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
        elif key.startswith('d'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 32:  # проверка на соответствие номеру дня
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
        elif key.startswith('th'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 24:  # проверка на соответствие часу
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
        elif key.startswith('tm'):
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 60:  # проверка на соответствие минуте
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
            
        print("Таблица 'ZL'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
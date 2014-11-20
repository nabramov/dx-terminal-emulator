# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Связи в Линейно-протяженной конфигурации (LL):
========================================================================
         DX-центра  К DX    Инф.Канал  Речевые: 10        20        30
 Nпп Вкл. К Канал DK Канал Вкл. Канал  .123456789012345.789012345678901
------------------------------------------------------------------------
   0   1  2   3    4   5     6    7   101234567890123456789012345678901
------------------------------------------------------------------------"""
    footer = "========================================================================"
    helper = """Таблица 'Связи в Линейно-протяженной конфигурации (LL):'
 Параметры:
   1. 'Вкл.'  - флаг 'выкл./вкл.' связь;
   2. 'K'     - номер кластера (К), в центральной DX;
   3. 'Канал' - номер ИКМ-канала в кластере центральной DX;
   4. 'DK'    - номер DX (D) и номер кластера (К), который подключен
                линейный DX;
   5. 'Канал' - номер ИКМ-канала в DK;
   6. 'Вкл.'  - флаг 'выключена/включена' связь;
   7. 'Канал' - номер ИКМ-канала в кластере;
   8,9        - не исп.;
   10-41. 'Речевые каналы' - отметки (+) для каналов"""
      
    number = 56
    name = 'll'
    max_line = 32
    def_param = [{'name':'f','default':0,0:'-',1:'+'},
                 {'name':'cl1','default':'0'},
                 {'name':'ch1','default':'0'},
                 {'name':'dx2','default':'0'},
                 {'name':'cl2','default':'0'},
                 {'name':'ch2','default':'0'},
                 {'name':'eif','default':0,0:'-',1:'+'},
                 {'name':'ich','default':'0'},
                 {'name':'unknown','default':''},
                 {'name':'unknown','default':''},
                 {'name':'001','default':0,0:'-',1:'+'},
                 {'name':'023','default':0,0:'-',1:'+'},
                 {'name':'045','default':0,0:'-',1:'+'},
                 {'name':'067','default':0,0:'-',1:'+'},
                 {'name':'089','default':0,0:'-',1:'+'},
                 {'name':'101','default':0,0:'-',1:'+'},
                 {'name':'123','default':0,0:'-',1:'+'},
                 {'name':'145','default':0,0:'-',1:'+'},
                 {'name':'167','default':0,0:'-',1:'+'},
                 {'name':'189','default':0,0:'-',1:'+'},
                 {'name':'201','default':0,0:'-',1:'+'},
                 {'name':'223','default':0,0:'-',1:'+'},
                 {'name':'245','default':0,0:'-',1:'+'},
                 {'name':'267','default':0,0:'-',1:'+'},
                 {'name':'289','default':0,0:'-',1:'+'},
                 {'name':'301','default':0,0:'-',1:'+'}]
    
    write_param = {1:'f',2:'cl1',3:'ch1',4:'dx2',5:'ch2',6:'eif',7:'ich',8:'unknown',9:'unknown',10:'001',11:'001',12:'023', \
                   13:'023',14:'045',15:'045',16:'067',17:'067',18:'089',19:'089',20:'101',21:'101',22:'123',23:'123',24:'145', \
                   25:'145',26:'167',27:'167',28:'189',29:'189',30:'201',31:'201',32:'223',33:'223',34:'245',35:'245',36:'267', \
                   37:'267',38:'289',39:'289',40:'301',41:'301'}
    
    format_line = "{0:>4}   {1}{2:>3} {3:>3} {4:>3}{5} {6:>3}     {7}    {8}{9}{10}    {11}{12}{13}{14}{15}{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}{30}{31}{32}{33}{34}{35}{36}{37}{38}{39}{40}{41}{42}" 
     
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
            end_line = start_line #
            
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
                if key == 'f' or key == 'eif':    
                    p.append(plugin.def_param[i][v])
                elif key.isdigit():
                    if v&16 == 16: p.append(plugin.def_param[i][1])
                    else: p.append(plugin.def_param[i][0]) 
                    if v&1 == 1: p.append(plugin.def_param[i][1])
                    else: p.append(plugin.def_param[i][0]) 
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
            if pn < 1 or pn > 41 : raise
        except:
            print('Ошибка параметра в диапазоне(1-41) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'f' or key == 'eif':
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
        elif key == 'unknown':
            pass
        elif key == 'cl1':
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 7: 
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
        elif key == 'ch1' or key == 'ch2':
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 4: 
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
        elif key == 'dx2':
            if value.isdigit():
                v = '{:0>2}'.format(value)
                d_param = int(v[0])
                c_param = int(v[1])
                if d_param >= 0 and d_param < 8 and c_param >= 0 and c_param < 7:
                    if d_param > 0: 
                        param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = d_param
                    else:
                        try:
                            del param['g'][plugin.number][ln][key]
                        except:
                            pass
                    if c_param > 0:
                        param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)['cl2'] = c_param
                    else:
                        try:
                            del param['g'][plugin.number][ln]['cl2']
                        except:
                            pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return   
            else:
                print("Недопустимое значение параметра:", param_number)
                return 
        elif key == 'ich':
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 8: 
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
        else:
            if key.isdigit():
                try:
                    v = param['g'][plugin.number][ln][key]
                except KeyError:
                    v = 0
                if pn % 2 == 0: # Если параметр четный
                    if value == '+': v |= 16
                    else: v &= 1       
                else:
                    if value == '+': v |= 1
                    else: v &= 16
                if v > 0:
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                else:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
            else:
                print("Недопустимое значение параметра:", param_number)
                return 
            
        print("Таблица 'LL'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
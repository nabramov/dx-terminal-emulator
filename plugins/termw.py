

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Терминальные направления:
======================================
      -Куда-   -- 1-ое --   -- 2-ое --
  N   oт  до   Ф DK Канал   Ф DK Канал
--------------------------------------
  0    1   2   3  4   5     6  7   8
--------------------------------------"""
    footer = '======================================'
    helper = """Таблица 'Терминальные направления':
 Параметры:
  0.  'N'    - номер пути;
  1,2 'Куда' - индексы системы DX (NТу в Sys) или индексы от и до;
     Для направлений:
  3,6  'Ф'     - флаг: '+' - включено, '-' - выкл.;
  4,7  'DK'    - через какой DX (D) и кластер (К);
  5,8  'Канал' - канал с DSS1."""
      
    number = 69
    name = 'termw'
    max_line = 30
    def_param = [{'name':'ti','default':'0'},
                 {'name':'te','default':'0'},
                 {'name':'y1','default':0,0:'-',1:'+'},
                 {'name':'d1','default':'0'},
                 {'name':'c1','default':'0'},
                 {'name':'f1','default':'0'},
                 {'name':'y2','default':0,0:'-',1:'+'},
                 {'name':'d2','default':'0'},
                 {'name':'c2','default':'0'},
                 {'name':'f2','default':'0'}]
    
    write_param = {1:'ti',2:'te',3:'y1',4:'d1',5:'f1',6:'y2',7:'d2',8:'f2'}
    
    format_line = "{0:>3}{1:>5}{2:>4}   {3} {4}{5}{6:>4}     {7} {8}{9}{10:>4}" 
     
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
            end_line = start_line
            
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
                if key == 'y1' or key == 'y2':    
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
            if pn < 1 or pn > 8 : raise
        except:
            print('Ошибка параметра в диапазоне(1-8) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'd1' or key == 'd2':
            if value.isdigit():
                d_param = int(value[0])
                c_param = int(value[1])
                if d_param < 8 and d_param > 0: # 8 макс значения для DX   7 макс значение для кластера где есть потоки
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = d_param
                elif d_param == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
                if c_param < 7 and c_param > 0:
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)['c'+key[1]] = c_param
                elif c_param == 0:
                    try:
                        del param['g'][plugin.number][ln]['c'+key[1]]
                    except:
                        pass
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
            else: 
                print("Недопустимое значение параметра:", param_number)
                return
        elif key == 'y1' or key =='y2':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == '+': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        elif key == 'ti' or key == 'te':
            if value.isdigit():
                v = int(value)
                if v < 255 and v > 0:  # Макс номер направления 254
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
        elif key == 'f1' or key == 'f2':
            if value.isdigit():
                v = int(value)
                if v < 4 and v > 0: # в кластере не может быть больше 4 каналов
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
                print("Недопустмое значение параметра:", param_number)
                return    
        print("Таблица 'TermW'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
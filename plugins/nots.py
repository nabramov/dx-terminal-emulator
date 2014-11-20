# -*- coding: utf-8 -*-


import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Запрещающие шаблоны:
==============================================
 Nпп Категория Порты/Группы         Шаблон
----------------------------------------------
   0     1     2      3      4      5
----------------------------------------------"""
    footer = "=============================================="
    helper = """Таблица 'Запрещающие шаблоны':
 Параметры:

   1. 'Категория' - категория;
   2-4. 'Порт/Группа' - порты и группы для которых
                        действует шаблон;
   5. 'Шаблон'    - значение (цифры,*,?)."""  
    number = 66
    name = 'nots'
    max_line = 32
    def_param = [{'name':'c','default':0},
                 {'name':'i1','default':'-'},
                 {'name':'i2','default':'-'},
                 {'name':'i3','default':'-'},
                 {'name':'s','default':''}]
    
    write_param = {1:'c',2:'i1',3:'i2',4:'i3',5:'s'}
    
    format_line = "{0:>4}     {1:<5} {2:<6} {3:<6} {4:<6} {5:<10}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы NOTS."""
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
                if key == 's':
                    if v != '':
                        v = str(v)
                        s = ''
                        for c in range(0, len(v), 2):
                            s += chr(int(v[c:c+2],16)) 
                        p.append(s)
                    else:
                        p.append(v)
                elif key == 'c':
                    p.append(v)
                elif key.startswith('i'):
                    if v != '-':
                        port = (v & 0xFF)
                        cluster = (v & 0xF00)>>8
                        dx = (v & 0x7000)>>12 
                        p.append('{}{},{:0>3}'.format(dx,cluster,port))
                    else:
                        p.append(v)
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
            if pn < 1 or pn > 5: raise
        except:
            print('Ошибка параметра в диапазоне(1-5) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'c':
            if value.isdigit():
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = int(value)
            else:
                print("Недопустимое значение параметра:", param_number)
                return 
        elif key == 's':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                if value.isdigit():
                    s = ''
                    for c in range(len(value)):
                        s += '%02x' % (ord(value[c]))
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = s
               
        elif key.startswith('i'):
            sep_pos = value.find(',')
            if sep_pos > 0:
                port = int(value[sep_pos+1:])
                cluster = int(value[1])<<8
                dx = int(value[0])<<12
                result = 0x8000 + dx + cluster + port
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = result
            elif value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        
        print(param)    
        print("Таблица 'NOTS'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
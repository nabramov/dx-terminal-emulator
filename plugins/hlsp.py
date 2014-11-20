# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """'Логические каналы' УГС:  
=====================================================================================
       Мастер  Порт   -Кластера-                         Режим входящего
 Nпп   порт    дисп.  1  2  3  4  АР OPp БРВ Рк ИрВ Оah  вызова от УГС         TA Пт
-------------------------------------------------------------------------------------
   0   1         2    3  4  5  6   7  8   9  10  11 12   13                    14 15
-------------------------------------------------------------------------------------"""
    footer = "====================================================================================="
    helper = """Таблица 'Аварийный порт' и вызовы:
 Параметры:
   1. 'Мастер порт' -  Мастер-порт (к,порт);
   2. 'Порт дисп.'  - порт диспетчера(в кластере мастер порта, только порт)'.
   3,4,5,6 - Кластера логического канала;
     Флажки:
   7. 'АР'  - всегда создавать разговор для оповещения;
   8. 'OPp' - 'базовый' режим оповещения 'Вау';
   9. 'БРВ' - нет авто-разрушения оповещения при входящем от УГС;
  10. 'Рк'  - с регистром УГСы (1P1P) на кнопках пульта;
  11. 'ИрВ' - индикация разговора в режиме 'Вау' на группу;
  12. 'Оah' - нет авто-reholda разговора оповещения;
  13. 'Режим входящего вызова от УГС':
         - (ct) 'текущим' разговором;
         - (pt) 'предыдущим' разговором;
         - (nc) 'конференция' новая с УГСами;
         - (lc) 'конф.оповещения' с УГСами;
  14. 'TA' - разрешение вызова УГС как TA;
  15. 'Пт' - приоритет диспетчера;"""
      
    number = 128
    name = 'hlsp'
    max_line = 16
    def_param = [{'name':'mp','default':'-'},
                 {'name':'dp','default':'0'},
                 {'name':'k1','default':'0'},
                 {'name':'k2','default':'0'},
                 {'name':'k3','default':'0'},
                 {'name':'k4','default':'0'},
                 {'name':'f1','default':0,0:'-',1:'+'},
                 {'name':'f2','default':0,0:'-',1:'+'},
                 {'name':'f3','default':0,0:'-',1:'+'},
                 {'name':'f4','default':0,0:'-',1:'+'},
                 {'name':'f5','default':0,0:'-',1:'+'},
                 {'name':'f6','default':0,0:'-',1:'+'},
                 {'name':'fm','default':0,0:"(ct) 'текущим'",1:"(pt) 'предыдущим'",2:"(nc) 'конференция'",3:"(lc) 'конф.оповещения'"},
                 {'name':'f7','default':0,0:'-',1:'+'},      
                 {'name':'pr','default':'0'}]
    
    write_param = {1:'mp',2:'dp',3:'k1',4:'k2',5:'k3',6:'k4',7:'f1',8:'f2',9:'f3',10:'f4',11:'f5',12:'f6',13:'fm',14:'f7',15:'pr'}
    
    format_line = "{0:>4}   {1:<8} {2:>2}   {3:>2} {4:>2} {5:>2} {6:>2}   {7}  {8}   {9}   {10}   {11}  {12}  {13:<22} {14} {15:>3}" 
    
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """   """
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
            p.append(line) # добавляем номер строки
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
                if key == 'mp':
                    if v != '-':
                        port = (v & 0xFF)
                        cluster = (v & 0xF00)>>8
                        dx = (v & 0x7000)>>12 
                        p.append('{}{},{:0>3}'.format(dx,cluster,port))
                    else:
                        p.append(v)
                elif key == 'dp' or key == 'pr':
                    p.append(v)  
                elif key.startswith('f'):
                    p.append(plugin.def_param[i][v])
                elif key.startswith('k'):
                    if v != '0':
                        m1 = 0x0F
                        m2 = 0x70
                        f2 = (v & m1)
                        f1 = (v & m2)>>4
                        p.append('{}{}'.format(f1,f2))
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
            if pn < 1 or pn > 15: raise
        except:
            print('Ошибка параметра в диапазоне(1-15) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key.startswith('f'):
            if key[1] == 'm':
                if value == 'ct': 
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                elif value == 'pt': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
                elif value == 'nc': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 2
                elif value == 'lc': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 3
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return    
            else:
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
        elif key.startswith('k'):
            if value.isdigit():
                #param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
                v = '{:0>2}'.format(value)
                f1 = int(v[0])<<4
                f1 += int(v[1])
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = f1
            elif value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        elif key =='mp':
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
        elif key == 'dp':
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 192:  # проверка на соответствие часу
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
        elif key == 'pr':
            if value.isdigit():
                v = int(value)
                if v > 0 and v < 32:  # проверка на соответствие минуте
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
        #print(param)    
        print("Таблица 'HLSP'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
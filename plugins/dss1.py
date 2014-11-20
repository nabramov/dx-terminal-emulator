# -*- coding: utf-8 -*-

import plugins.base


class plugin(plugins.base.baseplugin):
    header = """Параметры DSS1:
=====================================================================================
       Типы          Идентификатор
Nk Вкл.номера        плана        Префикс Номер Pm QSIG ChI Al HI P1 КН ГрР Мк Пс КА
-------------------------------------------------------------------------------------
 0  1  2               3             4      5   6    7   8   9 10 11 12  13 14 15 16
-------------------------------------------------------------------------------------"""
    footer = "====================================================================================="
    helper = """Таблица 'Параметры DSS1':
 Параметры:
  0. 'Nk'    - канал Falc (ИКМ);
  1. 'Вкл.'  - флаг вкл./выкл. использования параметров;
  2. 'Тип Плана' - тип номера:
        u - unknown     i-international
        n - national    t - network
        s - subscriber  a - abbreviated;
  3. 'Идентификатор плана' - по ETS300 102-1:
        u - unknown   i - ISDN/Telephony
        d - data      t - telex
        n - national  p - private;
  6. 'Pm'   - флаг не генерации сообщения PROGRESS;
  7. 'QSIG' - флаг QSIG-протокола;
  8. 'ChI'  - флаг обязательного включения 'Ch_ident info'
              в SETUP Slave;
  9. 'Al'   - флаг не посылки Alerting в 1-ом ответе на Setup;
 10. 'HI'   - флаг для Международной связи по QSIG для HARRISa
              (цифры 9810 преобразуются в *)
 11. 'P1'   - в PROGRESS 1, а не 8;
 12. 'КН' - конец набора '#';
 13. 'ГрР' - группа резервных ТЧ-каналов.
 14. 'Мк'  - 'Мастер' управления каналами.
 15. 'Пс'  - прямой счет каналов (1-30).
 16. 'КА'  - разрешить прием/передачу категории абонента в 'iDisplay'."""  
            
    number = 97
    name = 'dss1'
    max_line = 4
    def_param = [{'name':'f','default':0,0:'-',1:'+'},
                 {'name':'p','default':0},
                 {'name':'d','default':0},
                 {'name':'s','default':0},
                 {'name':'pr','default':0,0:'-',1:'+'},
                 {'name':'qs','default':0,0:'-',1:'+'},
                 {'name':'ci','default':0,0:'-',1:'+'},
                 {'name':'al','default':0,0:'-',1:'+'},
                 {'name':'hf','default':0,0:'-',1:'+'},
                 {'name':'p1f','default':0,0:'-',1:'+'},
                 {'name':'def','default':0,0:'-',1:'+'},
                 {'name':'gr','default':0}, # данные не точные, установить не удалось
                 {'name':'pf','default':0,0:'-',1:'+'},
                 {'name':'ps','default':0,0:'-',1:'+'},
                 {'name':'pc','default':0,0:'-',1:'+'}]
    
    p_tn = {0:'unknown',1:'international',2:'national',3:'network',4:'subscriber',6:'abbreviated'} #типы номера
    p_ip = {0:'unknown',1:'ISDN/Telephony',3:'data',4:'telex',8:'national',9:'private'} # идентификатор плана
    write_param = {1:'f',2:'p_tn',3:'p_ip',4:'d',5:'s',6:'pr',7:'qs',8:'ci',9:'al',10:'hf',11:'p1f',12:'def',13:'gr',14:'pf',15:'ps',16:'pc'}   
    format_line = " {0}  {1}  {2:<14}{3:<16}{4} {5:>6}   {6}    {7}   {8}   {9}  {10}  {11}  {12}  {13:>2}  {14}  {15}  {16}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы DSS1. """
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
                    v = param[cl][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
                if key == 'd' or key == 's' or key == 'gr':
                    if v >= 0 and v < 10:
                        p.append(v)
                    else:
                        p.append('???')    
                elif key == 'p':
                    tn = v // 16  # ключ от словаря p_tn    Типы номера
                    ip = v % 16   # ключ от словаря p_ip    Идентификатор плана
                    p.append(plugin.p_tn[tn])
                    p.append(plugin.p_ip[ip])  
                else:
                    p.append(plugin.def_param[i][v])                                   
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
            if pn < 1 or pn > 16 : raise
        except:
            print('Ошибка параметра в диапазоне(1-15) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'd' or key == 's' or key == 'gr':
            if value == '0':
                try:
                    del param[cl][plugin.number][ln][key]
                except:
                    pass
            elif value >=0 and value < 10: 
                param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = int(value) 
            else:
                print("Недопустимое значение параметра:", value)
                return 
        elif key == 'p_tn':
            if value == 'u':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                except:
                    print("Недопустимое значение параметра:", value)
                    return
                ip = temp % 16
                if ip > 0:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = ip
                else: 
                    try:
                        del param[cl][plugin.number][ln]['p']
                    except:
                        pass
            elif value == 'n':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    ip = temp % 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 32 + ip
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 32
            elif value == 'i':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    ip = temp % 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 16 + ip
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 16 
            elif value == 't':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    ip = temp % 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 48 + ip
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 48
            elif value == 's':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    ip = temp % 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 64 + ip
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 64
            elif value == 'a':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    ip = temp % 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 96 + ip
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 96
            else:
                print("Недопустимое значение параметра:", value)
                return

        elif key == 'p_ip':
            if value == 'u':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                except:
                    print("Недопустимое значение параметра:", value)
                    return
                tn = temp // 16
                if tn > 0:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = tn
                else: 
                    try:
                        del param[cl][plugin.number][ln]['p']
                    except:
                        pass
            elif value == 'i':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    tn = temp // 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = tn*16 + 1
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 1
            elif value == 'd':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    tn = temp // 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = tn*16 + 3
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 3 
            elif value == 't':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    tn = temp // 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = tn*16 + 4
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 4
            elif value == 'n':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    tn = temp // 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = tn*16 + 8
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 8
            elif value == 'p':
                try:
                    temp = param[cl][plugin.number][ln]['p']
                    tn = temp // 16
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = tn*16 + 9
                except: 
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)['p'] = 9
            else:
                print("Недопустимое значение параметра:", value)
                return
        else:
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
                        
        print("Таблица 'DSS1'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
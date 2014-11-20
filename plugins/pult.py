# -*- coding: utf-8 -*-

import plugins.base
import re

class plugin(plugins.base.baseplugin):
    header = """Конфигурация пультов:
=======================================================================
 Пульт Порт  Консоль      Мв Tпп Кн En Ик Маг/E1 ТА ГА Вг НД Adv Тп рС
-----------------------------------------------------------------------
  0       1     2          3  4   5  6  7 8       9 10 11 12  13 14 15
-----------------------------------------------------------------------"""
    footer = "======================================================================="
    helper = """Таблица 'CD линий' пультов:

 Параметры:

   0. 'CD'      - для какой CD-линии/UPN в кластере;
   1. 'Порт'    - порт (AB-линия пульта);
   2. 'Консоль' - (M)Главная консоль или Дополнительная (L) на
                  90-кнопок. Отсутствие кодируется как (-) или (0);
   3. 'Mв'   - флаг 'разрешение всех входящих';
   4. 'Tпп'  - флаг типа пульта: '-' - OpenStage, '+' - OptiSet,OptiPoint;
   5. 'Кн'   - кодовый набор кнопок: 0 - полный, 1-усеченный;
   6. 'En'   - английский язык;
   7. 'Ик'   - флаг спец. индикации (в ЖД-круге);
   8. 'Маг.' - идентификатор порта записи на магнитофон;
   9. 'ТА'   - флаг функционирования как ТА;
  10. 'ГА'   - флаг АОН из городских линий;
  11. 'Вг'   - флаг выкл.громкой по тангенте/флик в АДАСЭ.
  12. 'НД'   - флаг 'пульт не умеет генерить' DTMF.
  13. 'Adv'  - флаг 'пульт типа Optipoint Advance'.
  14. 'Тп'   - транзит сигнализации пульта в E1(ИКМ),
  15. 'Рс'   - рассылка состояния пульта."""  
            
    number = 80
    name = 'pult'
    max_line = 32
    def_param = [{'name':'p','default':'0'},
                 {'name':'t','default':0,0:'-',1:'(M)Главная',2:'(L)Приставка'},
                 {'name':'n','default':0,0:'-',1:'+'},
                 {'name':'a','default':0,0:'-',1:'+'},
                 {'name':'kk','default':'0'},
                 {'name':'en','default':0,0:'-',1:'+'},
                 {'name':'ri','default':0,0:'-',1:'+'},
                 {'name':'mp','default':0,0:'-'},
                 {'name':'ta','default':0,0:'-',1:'+'},
                 {'name':'ga','default':0,0:'-',1:'+'},
                 {'name':'hf','default':0,0:'-',1:'+'},
                 {'name':'nd','default':0,0:'-',1:'+'},
                 {'name':'ad','default':0,0:'-',1:'+'},
                 {'name':'e1','default':0,0:'-',1:'+'},
                 {'name':'stt','default':0,0:'-',1:'+'}]
    
    write_param = {1:'p',2:'t',3:'n',4:'a',5:'kk',6:'en',7:'ri',8:'mp',9:'ta',10:'ga',11:'hf',12:'nd',13:'ad',14:'e1',15:'stt'}   
    format_line = "{0:>3}     {1:>3}  {2:<14}{3}{4:>3}{5:>4}{6:>3}{7:>3} {8:<8}{9}  {10}  {11}  {12}   {13}  {14}  {15}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы PULT. """
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
                if key == 'p' or key == 'kk':        
                    p.append(v)
                elif key == 'e1':
                    if v == 1:
                        p[3] = '*'
                        p[4] = '** '
                        p[5] = 'тран'
                        p[6] = 'зит'
                        p[7] = ' в '
                        p[9] = ' '
                        p[10] = ' '
                        p[11] = ' '
                        p[12] = ' '
                        p[13] = ' '
                    p.append(plugin.def_param[i][v])  
                elif key == 'mp':
                    t = int(v)
                    if t == 0:
                        p.append(plugin.def_param[i][v])
                    else:
                        m1 = 0xFF
                        m2 = 0xF00
                        m3 = 0x7000
                        po = (t & m1)
                        ccl = (t & m2)>>8
                        dx = (t & m3)>>12
                        p.append('{}{},{:0>3}'.format(dx,ccl,po))
                elif key == 'stt':
                    if p[14] == '+':
                        p.append(' ')
                    else:
                        p.append(plugin.def_param[i][v])
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
            if pn < 1 or pn > 15 : raise
        except:
            print('Ошибка параметра в диапазоне(1-15) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'n' or key == 'a' or key == 'en' or key == 'ri' or key == 'ta' or key == 'ga'\
        or key == 'hf' or key == 'nd' or key == 'ad' or key == 'e1' or key == 'stt':
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
        elif key == 't':
            if value == '-':
                try:
                    del param[cl][plugin.number][ln][key]
                except:
                    pass
            elif value == 'l': 
                param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            elif value =='m':
                param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 2 
            else:
                print("Недопустимое значение параметра:", value)
                return
        elif key == 'mp':
            if value == '-':
                try:
                    del param[cl][plugin.number][ln][key]
                except:
                    pass
            else:
                d = re.sub('[-]',',',value).split(',')           
                _value = 32768
                _value += int(d[0][0])<<12
                _value += int(d[0][1])<<8
                _value += int(d[1])
                param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = _value 
        elif key == 'p' or key == 'kk':
            if value.isdigit():
                if value == '0':
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                else:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = int(value)
            else:
                print("Недопустимое значение параметра:", value)
                return 
        print("Таблица 'PULT'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
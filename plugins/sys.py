# -*- coding: utf-8 -*-

import plugins.base
import re

class plugin(plugins.base.baseplugin):
    header = """Системные Параметры:
============================================================
     DK Гл.  Префикс Код                       Жалобы
 Nпп Центра  АОН     зоны  Тарификация НФТ NТу NТу DK НМ иА
------------------------------------------------------------
   0    1    2       3     4             5   6   7  8  9 10
------------------------------------------------------------"""
    footer = "==============================================================="
    helper = """Таблица 'Системные параметры':
 Параметры:
   1. 'DK Гл.Центра' - номер DX (D) и номер кластера (К) Главного Центра/Кластера;
   2. 'Префикс AOH'  - префикс для АОН в городскую АТС;
   3. 'Код зоны'     - не исп.;
   4. 'Тарификация'  - сбор тарификационных записей:
         'e' - только для внешних разговоров;
         'a' - всех;
         '-' - без сбора.
   5. 'НФТ' - формат вывода тарификационной записи;
   6. 'NТу' - индекс системы для терминального управления;
   7. 'NТу' - индекс системы для выгрузки жалоб;
   8  'DK'  - DX (D) и кластер (K) для основных жалоб;
   9  'НМ'  - флаг для 'непрослушивания' абонентов на HOLDе;
  10. 'иА'  - индикация всех разговоров диспетчера;
  11. 'NТу' - индекс системы для выгрузки 'защиты';
  12  'DK'  - DX (D) и кластер (K) для 'защиты';"""  
    number = 57
    name = 'sys'
    max_line = 1
    def_param = [{'name':'gcl','default':'0'},
                 {'name':'a7','default':32},
                 {'name':'a6','default':32},
                 {'name':'a5','default':32},
                 {'name':'a4','default':32},
                 {'name':'a3','default':32},
                 {'name':'a2','default':32}, 
                 {'name':'a1','default':32},
                 {'name':'z','default':''},
                 {'name':'bf','default':0,0:'(e)Внешние',1:'(a)Все',2:'???',3:'-'},
                 {'name':'bfn','default':'0'},
                 {'name':'ti','default':'0'},
                 {'name':'wti','default':'0'},
                 {'name':'wce','default':'0'},
                 {'name':'mf','default':0,0:'-',1:'+'},
                 {'name':'af','default':0,0:'-',1:'+'}]
    
    write_param = {1:'gcl',2:'a',3:'z',4:'bf',5:'bfn',6:'ti',7:'wti',8:'wce',9:'mf',10:'af'}
    
    format_line = "{0:>4}   {1:0>2}    {2:<8}{3:<6}{4:<12}{5:>3}{6:>4}{7:>4} {8:0>2}  {9}  {10}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы SYS. Для данной таблицы параметры cl и end_line
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
            if re.match('a\d', key):
                z = chr(v)
                if key == 'a7': p.append(z)
                else: p[-1] += z
            elif key == 'bf' or key == 'af' or key == 'mf':
                p.append(plugin.def_param[i][v]) 
            else: p.append(v)  
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
            if pn < 1 or pn > 10 : raise
        except:
            print('Ошибка параметра в диапазоне(1-10) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'a':
            if value.isdigit():
                for i in range(len(value)):
                    if i > 7: return  # Если введено число длиной более 7 знаков, то выходим.
                    key_ = 'a'+str(7-i)
                    param.setdefault('g', tab).setdefault(plugin.number, lines). \
                        setdefault(ln,p)[key_] = ord(value[i])
            elif value == '-':
                for i in range(7):
                    key_ = 'a'+str(i+1)
                    try:
                        del param['g'][plugin.number][ln][key_]
                    except:
                        pass
            else : 
                print("Значение параметра должно содержать только цифры или '-'")
                return
        elif key == 'mf' or key == 'af':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == '+':
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            else:
                print('Ошибка параметра. Значение должно быть "+" или "-"',value)
        elif key == 'bf':
            if value == 'e':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == 'a': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            elif value == 'f': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 2
            elif value == '-': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 3 
        elif key == 'z':
            if value.isdigit():
                v = int(value)
                if v < 10000: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = int(value)
                else:
                    print("Недопустимое значение параметра:", param_number)
                    return
            elif value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            else:
                print("Недопустимое значение параметра:", param_number)
                return
        else:                 
            if value.isdigit():
                v = int(value)
                if v != 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = int(value)
                else:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
            else:
                print("Параметр {} не может иметь значение: {}".format(param_number,value))
                return
        print("Таблица 'SYS'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
        
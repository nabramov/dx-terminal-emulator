# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """План Нумерации:
========================================================
 Массив,Ц Тип         Значение      Переход  Nг О Гп Г'
--------------------------------------------------------
        0 1           2             3         4 5 6  7
--------------------------------------------------------"""
    footer = "========================================================"
    helper = """Таблица 'План Нумерации':
  Параметры:
    0. 'Массив,Ц' - номер массива и цифры в нем;
    1. 'Тип' - тип записи плана:
         '-' - отсутствует;
         's' - сервис;
         'c' - вызов порта/DECT_ТА/группы;
         'e' - префикс номеров для внешних линий;
    2. 'Значение' - для сервиса - 'сервисная функция', для вызова -
         номер порта/DECT_ТА/группа,
         для внешних - тип префикса;
    3. 'Переход'  - массив для следующей цифры;
    4. 'Nг'  - кол.во цифр донабора;
    5. 'О'   - флаг вызова оператора;
    6. 'Гп'  - флаг глобального префикса;"""  
    number = 37
    name = 'map'
    max_line = 250
    def_param = [{'name':'e','default':0},
                 {'name':'l','default':0},
                 {'name':'t','default':0},
                 {'name':'d','default':0},
                 {'name':'n','default':0}]
    
    format_line = """{0:>7},0 {1:<11} {2:<14}{3:<9} {4} {5} {6}  {7} {8}
        1 {9:<11} {10:<14}{11:<9} {12} {13} {14}  {15} {16}
        2 {17:<11} {18:<14}{19:<9} {20} {21} {22}  {23} {24}
        3 {25:<11} {26:<14}{27:<9} {28} {29} {30}  {31} {32}
        4 {33:<11} {34:<14}{35:<9} {36} {37} {38}  {39} {40}
        5 {41:<11} {42:<14}{43:<9} {44} {45} {46}  {47} {48}
        6 {49:<11} {50:<14}{51:<9} {52} {53} {54}  {55} {56}
        7 {57:<11} {58:<14}{59:<9} {60} {61} {62}  {63} {64}
        8 {65:<11} {66:<14}{67:<9} {68} {69} {70}  {71} {72}
        9 {73:<11} {74:<14}{75:<9} {76} {77} {78}  {79} {80}""" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd): # 
        """Функция выводит на экран содержимое таблицы DSYS. Для данной таблицы параметры cl и end_line
        игнорируются т.к таблица имеет всего одну стоку и является глобальной"""
        
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
        for line in range(start_line, end_line +1):
            flag = False # Флаг, устанавливаемый, если в строке хоть один параметр не по умолчанию
            p = []
            p.append(line)
            for i in range(10):
                t_param = False # флаг, определяющий как интерпритируется параметр t. если 0 то это типы, если 1 то это параметры
                l_param = False # флаг, определяющий как интерпритируется параметр d. если 0 то это порт, если 1 то это номер таблицы перехода
                group_type = 0 # параметр который определяет тип группы 1 - Tp; 2 - Td; 3 - Hg;
                p1 = ' -'
                p2 = ' '
                p3 = ' '
                p4 = ' ' # Параметр Nг (по умолчанию 0)
                p5 = ' '
                p6 = ' '
                p7 = ' '
                p8 = ' '
                for j in range(len(plugin.def_param)):
                    key = plugin.def_param[j]['name'] + str(i) # формируем имя параметра, из его имени, и номера (по факту набираемая цифра)
                    try:
                        v = param['g'][plugin.number][line][key]
                        flag = True
                    except:
                        v = plugin.def_param[j]['default']
                    if key[0] == 'e':
                        if v == 1: 
                            t_param = True
                            p1 = '(e) Донабор'      
                    elif key[0] == 't':
                        if t_param:
                            if v == 1:
                                p2 = 'AMTS_D'
                            elif v == 2:
                                p2 = 'AMTS_MFC'
                            elif v == 128:
                                p2 = 'ATS'  
                            else:
                                p2 = '???'  
                        else:
                            if v&1 == 1:
                                p1 = '(s) Сервис'
                            if v&2 == 2:
                                p1 = '(c) Вызов'
                                if v == 3:
                                    group_type = 1 #Tp
                                if v == 6:
                                    group_type = 3 #Hg
                                if v == 19:
                                    group_type = 2 #Td
                                if not l_param and group_type == 0:
                                    if v&8 == 8:
                                        p6 = '+'
                                    else: p6 = '-'
                                    if v&5 == 5:
                                        p5 = '+'
                                    else: p5 = '-'
                                    if v&33 == 33:
                                        p7 = '+'
                                    else: p7 = '-'
                                    if v&8192 == 8192:
                                        p8 = '+'
                                    else: p8 = '-'
                    elif key[0] == 'l':
                        l_param = bool(v)
                    elif key[0] == 'n':
                        if (t_param and p2 == 'ATS') or (p1 == '(c) Вызов' and group_type == 0 and not l_param):
                            p4 = v    
                    elif key[0] == 'd': 
                        if l_param: # если серви
                            p2 = '      ->'
                            p3 = v      
                        else:
                            if p1 == '(s) Сервис':
                                if v == 16: p2 = 'join' 
                                if v == 24: p2 = 'intervention'
                                if v == 32: p2 = 'join_incom'
                                if v == 40: p2 = 'get_call'
                                if v == 48: p2 = 'join_mark'
                                if v == 56: p2 = 'set_conf'
                                if v == 72: p2 = 'call_conf'
                                if v == 80: p2 = 'switch'
                                if v == 88: p2 = 'virtual'
                                if v == 96: p2 = 'switch_incom'
                                if v == 112: p2 = 'switch_mark'
                                if v == 129: p2 = 'gen_code'
                                if v == 136: p2 = 'set_night'
                                if v == 137: p2 = 'reset_night'
                                if v == 138: p2 = 'who_am_i'
                                if v == 144: p2 = 'mark'
                                if v == 160: p2 = 'exit'
                                if v == 176: p2 = 'call_back'
                                if v == 192: p2 = 'repeat'
                                if v == 224: p2 = 'go_if_busy'
                                if v == 240: p2 = 'go_if_no_req'
                            elif p1 == '(c) Вызов':
                                if group_type == 0:
                                    port = (v & 0xFF)
                                    cluster = (v & 0xF00)>>8
                                    dx = (v & 0x7000)>>12
                                    #ff = (v & 0x8000)>>15
                                    if cluster == 8:
                                        p2 = 'Gr,{:0>3}'.format(port) 
                                    elif cluster == 11:
                                        p2 = 'D0,{:0>3}'.format(port)
                                    else: p2 = '{}{},{:0>3}'.format(dx,cluster,port)
                                elif group_type == 1: # Tp
                                    p2 = 'Tp,{}'.format(v)
                                elif group_type == 2: # Td
                                    p2 = 'Td,{}'.format(v)
                                elif group_type == 3: # Hg
                                    p2 = 'Hg,{}'.format(v)
                p.append(p1)  
                p.append(p2)
                p.append(p3)
                p.append(p4)
                p.append(p5)
                p.append(p6)
                p.append(p7)
                p.append(p8)                      
                # print(p)           
            if flag: print(plugin.format_line.format(*p)) # выводим строку, только в том случае если в ней есть измененые параметры
        print(plugin.footer)
        
    def write(self, param, cl, cmd): #cmd [0] - line + index [1] - номер параметра [2] - значение
        tab = {}
        lines = {}
        p = {}
        try:   
            line_number = int(cmd[0][0])
            index_param = int(cmd[0][1])
            if line_number >= plugin.max_line: raise ValueError("Ошибка параметра")  
        except ValueError:
            print('Ошибка параметра Массив,Ц не может быть: ',cmd[0])
            return
        try:
            param_number = int(cmd[1])
            if param_number < 1 or param_number > 8 : raise
        except:
            print('Ошибка параметра в диапазоне(1-8)')
            return
        try:
            value = cmd[2]
        except:
            print("Ошибка значения параметра")

        if param_number == 1:
            if value == '-':
                for i in range(len(plugin.def_param)):
                    if param['g'][plugin.number][line_number].get(plugin.def_param[i]['name']+str(index_param)) != None: 
                            del param['g'][plugin.number][line_number][plugin.def_param[i]['name']+str(index_param)]
            elif value == 'e':
                param['g'][plugin.number][line_number]['e'+str(index_param)] = 1
            elif value == 's':
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = 1
            elif value == 'c':
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = 2
        if param_number == 2:
            sep_pos = value.find(',')
            if sep_pos > 0:
                # возвратим то, что находится в параметре t
                if param['g'][plugin.number][line_number].get('t'+str(index_param)) != None:
                    t_param = param['g'][plugin.number][line_number]['t'+str(index_param)]
                else: t_param = 0
                #
                if value == '-':  # Признак перехода
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['l'+str(index_param)] = 1
                else:
                    if param['g'][plugin.number][line_number].get('l'+str(index_param)) != None: 
                        del param['g'][plugin.number][line_number]['l'+str(index_param)]    
                if value[:2] == 'hg':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = int(value[sep_pos+1:])
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param + 6
                elif value[:2] == 'tp':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = int(value[sep_pos+1:])
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param + 3
                elif value[:2] == 'td':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = int(value[sep_pos+1:])
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param + 19
                else:
                    port = int(value[sep_pos+1:])
                    cluster = int(value[1])<<8
                    dx = int(value[0])<<12
                    result = 0x8000 + dx + cluster + port
                    if value[:2] == 'gr': result += 0x800 # Добавляем признак что это группа Gr 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = result
            else: # сервисы
                if param['g'][plugin.number][line_number].get('l'+str(index_param)) != None: 
                    del param['g'][plugin.number][line_number]['l'+str(index_param)]
                if value == 'join':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 16
                elif value == 'intervention':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 24
                elif value == 'join_incom':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 32
                elif value == 'get_call':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 40   
                elif value == 'join_mark':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 48  
                elif value == 'set_conf':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 56   
                elif value == 'call_conf':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 72
                elif value == 'switch':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 80
                elif value == 'virtual':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 88
                elif value == 'switch_incom':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 96
                elif value == 'switch_mark':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 112
                elif value == 'gen_code':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 129
                elif value == 'set_night':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 136
                elif value == 'reset_night':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 137
                elif value == 'who_am_i':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 138
                elif value == 'mark':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 144
                elif value == 'exit':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 160
                elif value == 'call_back':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 176
                elif value == 'repeat':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 192
                elif value == 'go_if_busy':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 224
                elif value == 'go_if_no_req':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['d'+str(index_param)] = 240
                elif value == 'ats':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['e'+str(index_param)] = 1
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = 128
                elif value == 'amts_mfc':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['e'+str(index_param)] = 1
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = 2
                elif value == 'amts_d':
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['e'+str(index_param)] = 1
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = 1                                    
        if param_number == 3:
            if value != '-':
                param['g'][plugin.number][line_number]['d'+str(index_param)] = int(value)
        if param_number == 4:
            param['g'][plugin.number][line_number]['n'+str(index_param)] = int(value)
        if param_number == 5:
            if param['g'][plugin.number][line_number].get('t'+str(index_param)) != None:
                t_param = param['g'][plugin.number][line_number]['t'+str(index_param)]
            else: t_param = 0 
            if value == '+': 
                t_param = t_param | 5
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param
            if value == '-':
                t_param = t_param ^ 5
                if t_param > 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param  
        if param_number == 6: 
            if param['g'][plugin.number][line_number].get('t'+str(index_param)) != None:
                t_param = param['g'][plugin.number][line_number]['t'+str(index_param)]
            else: t_param = 0 
            if value == '+': 
                t_param = t_param | 8
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param
            if value == '-':
                t_param = t_param ^ 8
                if t_param > 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param 
        if param_number == 7: 
            if param['g'][plugin.number][line_number].get('t'+str(index_param)) != None:
                t_param = param['g'][plugin.number][line_number]['t'+str(index_param)]
            else: t_param = 0 
            if value == '+': 
                t_param = t_param | 33
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param
            if value == '-':
                t_param = t_param ^ 33
                if t_param > 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param
        if param_number == 8: 
            if param['g'][plugin.number][line_number].get('t'+str(index_param)) != None:
                t_param = param['g'][plugin.number][line_number]['t'+str(index_param)]
            else: t_param = 0 
            if value == '+': 
                t_param = t_param | 8192
                param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param
            if value == '-':
                t_param = t_param ^ 8192
                if t_param > 0: 
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p)['t'+str(index_param)] = t_param
        #print(param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(line_number,p))
        print("Таблица 'MAP'. Запись значения {} в массив {} для цифры {} параметр {} произведена".format(value, line_number, index_param, param_number))
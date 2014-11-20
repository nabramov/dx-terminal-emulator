# -*- coding: utf-8 -*-

import plugins.base
import re

class plugin(plugins.base.baseplugin):
    header = """ Группы:
============================================================================
 Nг Тип   Ц Кат.пЦпЦпЦпЦ Ср Гпн Порты (DECT_TA)
----------------------------------------------------------------------------
  0 1     2   3 4         5   6 7/11       8/12       9/13/15    10/14/16
---------------------------------------------------------------------------- """
    footer = "============================================================================"
    helper = """Таблица 'Группы':
 Параметры:
   0. 'Nг'  - номер;
   1. 'Тип' - тип вызова:
        ca - (Пар.)  параллельная из портов-линий в одном кластере,
                     последовательная по 1-му свободному;
        ff - (1_Св.) по 1-му свободному;
        fa - (1_От.) по 1-му ответившему;
        t  - (Trunk) транковая из параллельных групп;
        cr - паралельная для звонков своим абонентам (одновременно всем);
   2. 'Ц'    - флаг циклического вызова;
   3. 'Кат.' - входящая категория;
   4. 'пЦпЦпЦ' - цифры с паузами префикса донабора;
   5. 'Ср'  - флаг 'сбора цифр в региcтр';
   6. 'Гпн' - вход во внешний план;
   7-14. 'Порты (DECT_ТА)' - состав группы;"""  
    number = 36
    name = 'group'
    max_line = 100
    def_param = [{'name':'l','default':''},
                 {'name':'t','default':0,0:'-',1:'Пар.',2:'1_Св.',3:'1_От.',4:'Trunk',5:'cr'},
                 {'name':'m','default':0,0:'-',1:'+'},
                 {'name':'c','default':'0'},
                 {'name':'d','default':''}, # Если отсутствует цифра после паузы то цифра добавляется равная 0
                 {'name':'cf','default':0,0:'-',1:'+'},
                 {'name':'s15','default':'0'},
                 {'name':'s0','default':0,0:'-'},
                 {'name':'s1','default':0,0:'-'},
                 {'name':'s2','default':0,0:'-'},
                 {'name':'s3','default':0,0:'-'},
                 {'name':'s4','default':0,0:'-'},
                 {'name':'s5','default':0,0:'-'},
                 {'name':'s6','default':0,0:'-'},
                 {'name':'s7','default':0,0:'-'},
                 {'name':'s8','default':0,0:'-'},
                 {'name':'s9','default':0,0:'-'},
                 {'name':'s10','default':0,0:'-'},
                 {'name':'s11','default':0,0:'-'},
                 {'name':'s12','default':0,0:'-'},
                 {'name':'s13','default':0,0:'-'},
                 {'name':'la','default':0,0:'',1:"лАОН='+'"},
                 {'name':'s14','default':0,0:'',1:"Тц= "}, # к строке прибавляется значение старшего байта. Младший байт ???
                 {'name':'lfa','default':0,0:'',1:"Fac='+'"},
                 {'name':'icm','default':0,0:'',1:"Инт='+'"}]
    
    write_param = {1:'t',2:'m',3:'c',4:'d',5:'cf',6:'s15',7:'s',8:'s',9:'s',10:'s',11:'s',12:'s',13:'s',14:'s',15:'s',16:'s',17:'la',18:'s14',19:'lfa',20:'icm'}
    
    format_line = """{0:>3} {1:<6}{2} {3:>3} {4:<8}  {5}{6:>4} {7:<11}{8:<11}{9:<11}{10:<11}     
                                {11:<11}{12:<11}{13:<11}{14:<11}
     {22:<6}         {21:<8}      {23:<7}    {24:<7}  {15:<11}{16:<11}""" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd): #cmd [0] - startline [1] - end_line
        """Функция выводит на экран содержимое таблицы group."""
        try: 
            start_line = cmd[0]
            if start_line != '?':
                start_line = int(cmd[0])
        except: 
            start_line = 0
        try: 
            end_line = int(cmd[1])
        except IndexError: 
            end_line = plugin.max_line -1
            
        if start_line == '?': 
            print(plugin.helper)
            return
        print(plugin.header)
        param_count = len(plugin.def_param)
        for line in range(start_line, end_line +1):
            p = []
            p.append(line) # добавляем номер строки
            flag = False # Флаг, устанавливаемый, если в строке хоть один параметр не по умолчанию
            port_count = 0 # Количество портов для вывода (макс 10) может быть выведено. Поскольку параметров портов 14, 
            # нужно контролировать количество выведенных портов
            range_flag = False  # Флаг, определяющий является ли значение началом диапазона
            for i in range(param_count):
                key = plugin.def_param[i]['name']
                try:
                    v = param['g'][plugin.number][line][key]
                    flag = True
                except:
                    v = plugin.def_param[i]['default']
                if key == 't' or key == 'm' or key == 'cf' or key == 'lfa' or key == 'icm':
                    p.append(plugin.def_param[i][v])
                elif key == 'la':
                    """добавляем элементы если у нас в списке меньше значений, ситуация возникает
                    когда выводим диапазоны значений в портах (параметры 7 - 16)"""
                    for k in range(len(p),21): 
                        p.append('-') 
                    p.append(plugin.def_param[i][v])
                elif key == 's14':
                    if v == 0:
                        p.append(plugin.def_param[i][v])
                    else:
                        p.append(plugin.def_param[i][1] + str(v))                    
                elif key == 'c' or key == 'd' or key == 's15' :
                    p.append(v)
                elif key == 'l': 
                    pass
                elif key.startswith('s'):
                    num_str = ''
                    for j in range(1,len(key)): num_str += key[j]
                    num = int(num_str)
                    if num < 14:
                        t = int(v)
                        if t == 0: p.append(plugin.def_param[i][v])
                        else:
                            m1 = 0xFF
                            m2 = 0xF00
                            m3 = 0x7000
                            m4 = 0x8000
                            po = (t & m1)
                            cl = (t & m2)>>8
                            dx = (t & m3)>>12
                            ff = (t & m4)>>15
                            pre_flag = range_flag   # Определяем что предыдущий параметр мог быть началом диапазона
                            range_flag = bool(ff)   # Определяем что текущий параметр может быть началом диапазона
                            if range_flag: 
                                p.append('{}{},{:0>3}'.format(dx,cl,po))
                            else: 
                                if pre_flag : 
                                    p[-1] += '-{:0>3}'.format(po)
                                else:
                                    if port_count < 10: 
                                        p.append('{}{},{:0>3}'.format(dx,cl,po))
                                        port_count += 1
                else: 
                    print("Ошибка")
                    return
            if flag: print(plugin.format_line.format(*p)) # выводим строку, только в том случае если в ней есть измененые параметры
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
            if pn < 1 or pn > 20 : raise
        except:
            print('Ошибка параметра в диапазоне(1-20) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'm' or key == 'cf' or key == 'la' or key == 'lfa' or key == 'icm':
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == '+': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1 
            else:
                print("Недопустимый параметр:", value)
                return 
        elif key == 't':
            #{'name':'t','default':0,0:'-',1:'Пар.',2:'1_Св.',3:'1_От.',4:'Trunk',5:'cr'},
            if value == '-':
                try:
                    del param['g'][plugin.number][ln][key]
                except:
                    pass
            elif value == 'ca': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 1
            elif value == 'ff': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 2
            elif value == 'fa': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 3
            elif value == 't': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 4
            elif value == 'cr': param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = 5
            else:
                print("Недопустимый параметр:", value)
                return  
        elif key =='s15':
            if value.isdigit():
                v = int(value)    
                if v < 250 and v > 0:
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимый параметр:", value)
                    return
            else:
                print("Недопустимый параметр:", value)
                return 
        elif key == 'c':
            if value.isdigit():
                v = int(value)
                if v < 250 and v > 0:
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимый параметр:", value)
                    return
            else:
                print("Недопустимый параметр:", value)
                return 
        elif key == 'd':
            if value.isdigit():
                v = int(value)
                if v < 9 and v > 0:
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
                else:
                    print("Недопустимый параметр:", value)
                    return    
            else:
                print("Недопустимый параметр:", value)
                return 
        elif key == 's14':
            if value.isdigit():
                v = int(value)
                if v < 20 and v > 0:
                    param.setdefault('g', tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v
                elif v == 0:
                    try:
                        del param['g'][plugin.number][ln][key]
                    except:
                        pass
            else:
                print("Недопустимый параметр:", value)
                return                        
        elif key =='s': # цифры опущены
            keys_ = []
            sorted_keys = sorted(param['g'][plugin.number][ln]) 
            for k in sorted_keys:
                if re.match('s\d',k):
                    if int(k[1:]) < 14: # диапазон нужных ключей
                        keys_.append(param['g'][plugin.number][ln][k]) # в результате получаем список значений портов
            for i in range(14): 
                if param['g'][plugin.number][ln].get('s'+str(i)) != None:
                    del param['g'][plugin.number][ln]['s'+str(i)] # удаляем все  ключи портов из списка
            len_keys = len(keys_)
            param_index = pn -7 # определяем прописываемый виртуальный индекс
            p_ = 0
            a_ = 0
            while p_ < param_index and p_+ a_< len_keys: #походим по списку до виртуального параметра.
                if keys_[p_+ a_] < 0x8000:
                    a_ += 1
                else:
                    p_ += 1
            if p_ == param_index and p_+a_ < len_keys: # добавляем еще один дополн. индекс если в последнем параметре записан диапазон
                if keys_[p_+ a_] < 0x8000:
                    a_ += 1
            index = p_+a_ # действительный индекс изменяемого параметра
            if index < len_keys: # если мы в диапазоне уже запрограммированных портов
                if value == '-': # если удаляем параметр
                    keys_.pop(index) # теперь индекс указывает на следующий элемент                   
                    if index < len(keys_) and keys_[index] < 0x8000: keys_.pop(index) # если следующий параметр конец диапазона удаляем и его                  
                else: # если изменяем параметр
                    d = re.sub('[-]',',',value).split(',')           
                    _value = 32768
                    _value += int(d[0][0])<<12
                    _value += int(d[0][1])<<8
                    _value += int(d[1])
                    keys_[index] = _value
                    index += 1
                    if len(d) > 2: # если прописываем диапазон
                        _value = 0
                        _value += int(d[0][0])<<12
                        _value += int(d[0][1])<<8
                        _value += int(d[2])
                        if index < len(keys_):
                            if keys_[index] < 0x8000: # если был диапазон
                                keys_[index] = _value
                            else: # иначе надо вставить элемент в список с индексом index
                                keys_.insert(index, _value)
                    else: # иначе удаляем диапазно если он был ранее тут прописан
                        if index < len(keys_):
                            if keys_[index] < 0x8000: # если был диапазон
                                keys_.pop(index)
                        
                        
            else: # если мы вне диапазона, значит добавляем значение в параметр если оно не рано '-'
                if value != '-':
                    d = re.sub('[-]',',',value).split(',')           
                    _value = 32768
                    _value += int(d[0][0])<<12
                    _value += int(d[0][1])<<8
                    _value += int(d[1])
                    keys_.append(_value)
                    if len(d) > 2: # если прописываем диапазон
                        _value = 0
                        _value += int(d[0][0])<<12
                        _value += int(d[0][1])<<8
                        _value += int(d[2])
                        keys_.append(_value)
        # записываем список обратно в структуру
        for i in range(len(keys_)):
            param['g'][plugin.number][ln]['s'+str(i)] = keys_[i]
        if len(keys_) > 0:
            param['g'][plugin.number][ln]['l'] = len(keys_) # записываем длину массива в параметр 'l'
        else:
            if param['g'][plugin.number][ln].has_key('l'): del param['g'][plugin.number][ln]['l'] # удаляем парамет 'l' если он 0 
                       
        #print(param['g'][plugin.number][line_number])
        print("Таблица 'GROUP'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
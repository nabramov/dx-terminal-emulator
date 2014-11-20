# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Дополнительные параметры портов:
========================================================================================
             - (сек) -
   Порт   НА Сер. Разг. НТ РА Бк Сз ТР Пр Г8 B1 ДО Дп Зв Ао ТА ПС EА ТдП B3  T cA пЗ ЗА
----------------------------------------------------------------------------------------
    0      1   2     3   4  5  6  7  8  9 10 11 12 13 14 15 16 17 18  19 20 21 22 23 24
----------------------------------------------------------------------------------------"""
    header1 = "- ИКМ-порты ------------------------------------------------------------------"
    footer = "========================================================================================"
    helper = """Таблица 'Дополнительные параметры портов':
 Параметры:
   0. 'Порт'- порт;
   1. 'НА'  - флаг возможного отсутствия сигнала 'ОТВЕТ Абонента',
              но переход в разговор необходим по таймауту 'Разговор';
              (Для пультов: 'нет ответа на входщий под'ьемом трубки');
   2. 'Сервис'- таймаут (<32) для перехода в сервис после набора
              последней цифры, когда неизвестно их кол-во.
              При установленном флаге 'НА' открывается тракт передачи;
   3. 'Разговор' - таймаут для ожидания сигнала 'ОТВЕТ Абонента'.
              При установленном флаге 'НА' и отсутствии 'ОТВЕТА'
              осуществляется переход в разговор.
              Для TA_BN/МБ и ПГС - время выдачи КПВ;
   4. 'НТ'  - флаг отказа от учета транзита для сигналов 'ОТВЕТ' и
              'Разьединение/Освобождение' в однотиповых ТЧ сигнализациях;
   5. 'РА'  - флаг запрос кодограммы АОН до ответа абонента
              (только сигнализации городская и SLI);
   6. 'Бк'  - флаг блокировки канала ТЧ в неработоспособном состоянии
              при установленном 'контроле', блокировка H320 для S0;
   7. 'Сз'  - флаг включения 'занято' в порты ТЧ,УСЛ2,E&M при входящей связи
              на занятого (если не хватает категории для вмешательства);
   8. 'ТнР' - флаг разрешения DTMF набора в разговоре для
              создания следующего разговора или сервиса;
   9. 'Пр'  - флаг 'наличия промрегистра', 64K для S0;
  10. 'Г8'  - флаг 'генерации 8' во встречную AТС;
  11. 'B1'  - флаг 'запроса 1-ой цифры в МЧК' c B1, иначе с B2;
              для сигнализации R2 флаг является флагом запрета перехода
              на сигналы группы II;
  12. 'ДО'  - флаг 'двухстороннего отбоя';
  13. 'Дп'  - дополнительный параметр. (Задержка перед выдачей B1/B2 в МЧК,
              кол-во цифр собственного номера в префиксе для E&M);
  14. 'Зв'  - флаг контроля входящих вызовов;
  15. 'Ао'  - флаг 'авто-ответа';
  16. 'ТА'  - флаг ожидания ответа абонента DTMF-цифрой 'D' в местном
              порту с донабором;
  17. 'ПС'  - флаг вызова по 'виртуальному' при установленом 'по умолчанию'
              для входящей по автоматике АДАСЭ (режим ПС);
  18. 'EA'  - флаг генерации АОН в E&M сигнализациях;
            - флаг выдачи 'отбой B' в R1.5 при установленном флаге ДО
              без ожидания отбоя своего абонента;
            - флаг автоматического входа в разговор для выделенных каналов DSS1
              (для связи-совещаний);
            - флаг наличия коммутатора для местного порта (переполюсовка);
            - флаг наличия телефонистки для пульта;
  20. 'B3'  - флаг 'запроса 1-ой цифры в МЧК' c B3;
            - флаг 'включать сигнал вызова' для УГС;
  21. 'Т'   - флаг 'тарификации' в R.15 после второго 'ответа'.
  22. 'cA'  - АОН в своем входе в план нумерации.
  23. 'пЗ'  - выделенный порт для звонка на пульт.
  24. 'ЗА'  - запрет демонстрации АОН при звонке на DSS1."""  
    number = 18
    name = 'paddp'
    max_line = 320
    def_param = [{'name':'na','default':0,0:'-',1:'+'},
                 {'name':'st','default':15},
                 {'name':'tt1','default':120},
                 {'name':'nt','default':0,0:'-',1:'+'},
                 {'name':'kk','default':0,0:'-',1:'+'},
                 {'name':'bk','default':0,0:'-',1:'+'},
                 {'name':'bs','default':0,0:'-',1:'+'}, 
                 {'name':'tt','default':0,0:'-',1:'+'},
                 {'name':'pr','default':0,0:'-',1:'+'},
                 {'name':'a8f','default':0,0:'+',1:'-'},
                 {'name':'fb1f','default':0,0:'-',1:'+'},
                 {'name':'do','default':0,0:'-',1:'+'},
                 {'name':'bd','default':0},
                 {'name':'zv','default':0,0:'-',1:'+'},
                 {'name':'aa','default':0,0:'-',1:'+'},
                 {'name':'dd','default':0,0:'-',1:'+'},
                 {'name':'ps','default':0,0:'-',1:'+'},
                 {'name':'ea','default':0,0:'-',1:'+'},
                 {'name':'tdp','default':0},
                 {'name':'b3','default':0,0:'-',1:'+'},
                 {'name':'daf','default':0,0:'-',1:'+'},
                 {'name':'oa','default':0,0:'-',1:'+'},
                 {'name':'rpr','default':0,0:'-',1:'+'},
                 {'name':'rf','default':0,0:'-',1:'+'}]
    
    write_param = {1:'na',2:'st',3:'tt1',4:'nt',5:'kk',6:'bk',7:'bs',8:'tt',9:'pr',10:'a8f',11:'fb1f',12:'do',13:'bd',14:'zv',\
                   15:'aa',16:'dd',17:'ps',18:'ea',19:'tdp',20:'b3',21:'daf',22:'oa',23:'rpr',24:'rf'}
    
    format_line = "{0:>9}  {1}  {2:>2} {3:>5}   {4}  {5}  {6}  {7}  {8}  {9}  {10}  {11}  {12}  {13}  {14}  {15}  {16}  {17}  {18} {19:>3}  {20}  {21}  {22}  {23}  {24}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы PADDP. """
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
        counter = 0
        for line in range(start_line, end_line +1):
            p = []
            if counter == 32 : counter = 0
            if line < 128:
                port_hi = line//32
                port_lo = counter//2
            if line == 128: 
                print(plugin.header1)
            if line >= 192: break
            if line >= 128:
                port_hi = (line-128)//32
                port_lo = counter
            port_ = '{}-{:0>2}'.format(port_hi,port_lo)
            p.append('{},{}'.format(line, port_)) # добавляем номер строки и номер порта
            counter += 1
            for i in range(param_count):              
                key = plugin.def_param[i]['name']
                try:
                    v = param[cl][plugin.number][line][key]
                except:
                    v = plugin.def_param[i]['default']
                if key == 'st' or key == 'tt1' or key == 'bd' or key == 'tdp':      
                    p.append(v)
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
            if pn < 1 or pn > 24 : raise
        except:
            print('Ошибка параметра в диапазоне(1-24) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'na' or key == 'nt' or key == 'kk' or key == 'bk' or key == 'bs' or key == 'tt' or key == 'pr' or key == 'a8f'\
        or key == 'fb1f' or key == 'do' or key == 'zv' or key == 'aa' or key == 'dd' or key == 'ps' or key == 'ea' or key == 'b3'\
        or key == 'daf' or key == 'oa' or key == 'rpr' or key == 'rf':
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
        elif key == 'st' or key == 'bd':
            if value.isdigit():
                v = int(value)
                if v == 0:
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                elif v > 0 and v < 32:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return 
            else:
                print("Недопустимое значение параметра:", value)
                return
        elif key == 'tt1':
            if value.isdigit():
                v = int(value)
                if v == 0:
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                elif v > 0 and v < 250:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return 
            else:
                print("Недопустимое значение параметра:", value)
                return
        elif  key == 'tdp':
            if value.isdigit():
                v = int(value)
                if v == 0:
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                elif v > 0 and v < 128:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return 
            else:
                print("Недопустимое значение параметра:", value)
                return 
        print("Таблица 'PADDP'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
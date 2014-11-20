# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Кластеры с Пультами:
=========================
     ---  Кластеры   ---
 DX  0  1  2  3  4  5  6
-------------------------
  0  1  2  3  4  5  6  7
-------------------------"""
    footer = "========================="
    helper = """Таблица 'Кластеры с пультами':
 Параметры:
   0. 'DX' - в кластерах каких DX;
   1,2,...7 '0,1,...6' - для каких кластеров;"""
      
    number = 81
    name = 'pultf'
    max_line = 8
    def_param = [{'name':'c0','default':0,0:'-',1:'+'},
                 {'name':'c1','default':0,0:'-',1:'+'},
                 {'name':'c2','default':0,0:'-',1:'+'},
                 {'name':'c3','default':0,0:'-',1:'+'},
                 {'name':'c4','default':0,0:'-',1:'+'},
                 {'name':'c5','default':0,0:'-',1:'+'},
                 {'name':'c6','default':0,0:'-',1:'+'}]
    
    write_param = {1:'c0',2:'c1',3:'c2',4:'c3',5:'c4',6:'c5',7:'c6'}
    
    format_line = "{0:>3}  {1}  {2}  {3}  {4}  {5}  {6}  {7}" 
     
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
        except:
            print('Ошибка параметра Nпп(0) не может быть',line_number)
            return
        try:
            pn = int(param_number)
            if pn < 1 or pn > 7: raise
        except:
            print('Ошибка параметра в диапазоне(1-41) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
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
            
        print("Таблица 'PultF'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
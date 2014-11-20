# -*- coding: utf-8 -*-
import json
import re
import plugins.base
import os
import inspect

class Error(Exception):
    """Base class for exceptions in this module.
    Базовый класс для исключений в этом модуле."""
    pass
 
class InputError(Error):
    """Exception raised for errors in the input.
    Исключение возбуждается для ошибок в вводе.
 
    Attributes:
        expression -- input expression in which the error occurred
                   -- входное выражение, в котором произошла ошибка
        message -- explanation of the error
                -- объяснение ошибки
    """
    def __init__(self, message, expression):
        self.expression = expression
        self.message = message

class term_core():
    """ Класс определяет базовые функции терминала. Формирует командную строку, производить анализ команд и 
    вызов соответствующих внешних модулей обработки (plugins) находящихся в соответствующей папке. """
    def __init__(self):
        super().__init__()
        self.tabs = {}
        self.current_cluster = 0
        self.current_dx = 0
        self.base_cluster = 0
        self.base_dx = 0
        self.gc = 0 # Кластер, установленный главным       
        self.prompt = ['','','','','',''] # формат приглашения командной строки - [base_dx, base_cluster, ',', current_dx, current_cluster, '>']
        
        ############################ Загрузка конфигурации ###########################
        try:
            f = open("config.json")
            self.config = json.load(f)
            f.close()
        except:                            
            print("Ошибка загрузки файла: config.json")
        self.debug = self.config["debug"]
        self.plugins_directory = self.config["plugins_directory"]
        if self.debug: print(self.config)
        
        ########################### Загрузка модулей ###########################
        self.modules = {}
        self.max_lines = {}
        for fname in os.listdir(self.plugins_directory):
            if fname.endswith(".py"):
                module_name = fname[:-3]
                if module_name != 'base' and module_name != '__init__':
                    if self.debug: print("Загрузка модуля %s" % module_name)
                    package_obj = __import__(self.plugins_directory + '.'+ module_name)
                    self.modules[module_name] = 0
                    if self.debug: print(dir(package_obj))
                    if self.debug: print(self.modules)
        for modulename in self.modules.keys():
            module_obj = getattr(package_obj, modulename)
            if self.debug: print(modulename)
            if self.debug: print(dir(module_obj))
            for elem in dir(module_obj):   
                obj = getattr(module_obj, elem)
                if inspect.isclass (obj):
                    if issubclass (obj, plugins.base.baseplugin):
                        a = obj()
                        self.modules[modulename] = a.number
                        self.max_lines[modulename] = a.max_line
        if self.debug: print(self.modules)
        
        ###########################
        
        
    def set_debug(self, value):
        if value == "on": 
            self.debug = True
            print("Режим отладки включен")
        elif value == "off": 
            self.debug = False 
            print("Режим отладки выключен")
        else: raise InputError("Ошибка - параметр может быть 'on' или 'off', а не", value)  
          
    def set_prompt(self): 
        """Функция формирует формат приглашения к вводу команды"""
        if self.current_cluster == self.base_cluster and self.current_dx == self.base_dx:
            self.prompt[0] = str(self.current_dx)
            self.prompt[1] = str(self.current_cluster)
            self.prompt[2] = '>'
            self.prompt[3] = ''
            self.prompt[4] = ''
            self.prompt[5] = ''
        else:
            self.prompt[0] = str(self.base_dx)
            self.prompt[1] = str(self.base_cluster)
            self.prompt[2] = ','
            self.prompt[3] = str(self.current_dx)
            self.prompt[4] = str(self.current_cluster)
            self.prompt[5] = '>'
            
    def show_tab(self, tab_name, cmd_line):
        """ Функция загружает одноименный с именем таблицы модуль (tab_name) 
        и вызывает его метод Show для вывода таблицы на экран"""

        package_obj = __import__(self.plugins_directory + '.'+ tab_name)
        if self.debug: print(dir(package_obj))
        module_obj = getattr(package_obj, tab_name)
        if self.debug: print(dir(module_obj))
        obj = getattr(module_obj, 'plugin')
        if issubclass (obj, plugins.base.baseplugin):
            a = obj()
            cl = str(self.current_dx)+str(self.current_cluster)
            a.show(self.tabs, cl, cmd_line)
    
    def get_tabname(self, number):
        """Функция возвращает имя таблицы по ее десятичному номеру"""
        for key in self.modules.keys():
            if self.modules[key] == number:
                if self.debug: print("Функция 'get_tabname' вернула значение", key)
                return key
        raise InputError("Не найдена таблица с номером", number) 
       
    def write_param(self,tab_name,cmd_list):
        """ Функция загружает модуль соответствующий имени таблицы в параметре tab_name
        и вызывает функцию модуля write передавая ей параметры line_number - номер строки куда производиться запись
        param_number - номер перезаписываемого параметра, value -  новое значение параметра"""
        package_obj = __import__(self.plugins_directory + '.'+ tab_name)
        if self.debug: print(dir(package_obj))
        module_obj = getattr(package_obj, tab_name)
        if self.debug: print(dir(module_obj))
        obj = getattr(module_obj, 'plugin')
        if issubclass (obj, plugins.base.baseplugin):
            a = obj()
            cl = '{:0>2}'.format(self.current_dx*10+self.current_cluster)
            a.write(self.tabs, cl, cmd_list) 
                    
    def parse(self, cmd):  
        """Функция осуществляет разбор команды пользователя """  
        if cmd[0] == "db":
            if cmd[1] == 'load':
                try:
                    self.load_config(cmd[2]) # имя файла
                except: raise InputError("Ошибка параметра", 2)
            elif cmd[1] == 'save':
                try:
                    self.save_config(cmd[2], cmd[3], cmd[4], cmd[5]) # файл, тип данных, номер DX, флаг
                except: raise InputError("Ошибка параметров:", cmd)
            else: raise InputError("Ошибка параметра", 1)
            return 
        elif cmd[0] == "t":
            try:
                if cmd[1].isdigit(): tab_name = self.get_tabname(int(cmd[1]))
                else: tab_name = cmd[1]
            except InputError: 
                raise
            if tab_name in self.modules.keys():
                cmd_= cmd[2:]
                self.show_tab(tab_name, cmd_)
            else:
                print("Не найдена таблица с именем '%s'" % tab_name)
        elif cmd[0] == "debug":
            try:
                self.set_debug(cmd[1])
            except InputError:
                raise 
        elif cmd[0] == 'wp':
            try:
                if cmd[1].isdigit(): tab_name = self.get_tabname(int(cmd[1]))
                else: tab_name = cmd[1]
            except InputError: 
                raise
            if tab_name in self.modules.keys():
                cmd_= cmd[2:]
                self.write_param(tab_name,cmd_) 
            else:
                print("Не найдена таблица с именем '%s'" % tab_name) 
        elif cmd[0].find('\\') >= 0:
            n = cmd[0].find('\\')
            if cmd[0][:n].isdigit:
                xx = '{:0>2}'.format(cmd[0][:n])    
                self.current_cluster = int(xx[1])
                self.current_dx = int(xx[0]) 
            else:
                print("Ошибка значения параметра", cmd)       
        else: 
            if cmd[0] == '':
                pass
            else: print("Нет такой команды", cmd)
    
    def save_config(self, filename, type_data = 'g',cluster = '0', flag = '1'):
        if not filename.isdigit: 
            print('Имя файла имеет не верный формат')
            return
        fn = 'dx{0:0>6}.cfn'.format(filename)
        try:
            f = open(fn, 'w')
        except IOError:
            print("Ошибка открытия файла: ", filename)
        if not cluster.isdigit:
            print('параметр DX имеет неизвестный формат')
            return
        if type_data == 'g':
            _cluster = 'Cgc'
            cl = 'g'
        else: 
            _cluster = 'C{0:0>2}'.format(cluster)
            cl = '{0:0>2}'.format(cluster)
        en_line = 0
        if cl in self.tabs.keys():
            for tab_key in self.tabs[cl].keys():
                try:
                    tab_name = self.get_tabname(tab_key) # Возвращаем имя таблицы
                    print("Выгрузка: Таблица '{}' -".format(tab_name), end='')
                except: 
                    continue
                flag = False
                #if not self.max_lines.has_key(tab_name): continue
                for line_num in range(self.max_lines[tab_name]): # Определяем цикл с макс. возможным кол-вом строк в таблице
                    if not flag: f.write('{0},{1:0>2X},{2:0>3X}'.format(_cluster,tab_key,line_num))
                    if line_num in self.tabs[cl][tab_key].keys() and len(self.tabs[cl][tab_key][line_num]) > 0:
                        if flag:
                            f.write('-{0:0>3X}:\n'.format(en_line))
                            #f.write('\n') # пустая строка
                            flag = False
                            f.write('{0},{1:0>2X},{2:0>3X}'.format(_cluster,tab_key,line_num))    
                        f.write(':')
                        for param_key in self.tabs[cl][tab_key][line_num]:          
                            value = self.tabs[cl][tab_key][line_num][param_key]
                            if value != 0:
                                f.write(' {0}={1}'.format(param_key,value))
                        f.write('\n')
                        #f.write('\n') # пустая строка
                    else:
                        en_line = line_num
                        flag = True                   
                if flag:
                    f.write('-{0:0>3X}:\n'.format(en_line))
                    #f.write('\n') # пустая строка
                    flag = False
                print(' Ок')
        f.close()        #if param_name in self.tabs['cluster'][tab_key] 
             
    def load_config(self, filename):
        """ Функция загружает данные в структуру self.tabs из файла, имя которого указано в параметре filename"""
        try:
            f = open(filename, 'r')
        except IOError:
            print("Ошибка открытия файла", filename)
        old_tab_name = ''    
        for line in f:
            if line.startswith('\n'): continue
            _params = {}
            tab = {}
            lines = {} 
            n = line.find(' ')
            if n < 0: continue  
            """ Массив с номерами [кластер, таблица, линия] """               
            q = re.sub('[c:\n]','',line[:n]).split(',')
            if '-' in q[2]: continue 
            """ Массив с параметрами """
            c = line[n:].strip(' \n').split(' ') 
            if q[0] != 'Cg': 
                cluster = '{0:0>2}'.format(str(int(q[0][1:])))
            else: cluster = 'g'                        
            line_start = int(q[2], 16)
            tab_num = int(q[1], 16)
            try:
                tab_name = self.get_tabname(tab_num) # Возвращаем имя таблицы 
            except: # Если имя таблицы не найдено то продолжаем цикл со следующей строки
                continue                                 
            for i in range(len(c)):
                p = ''.join(c[i]).split("=") 
                try:
                    _params[p[0]] = int(p[1])
                    
                except:
                    try:
                        _params[p[0]] = p[1]
                    except:    
                        print('Ошибка присвоения параметра ',p[1],' ключу', p[0])
            self.tabs.setdefault(cluster, tab).setdefault(tab_num, lines).setdefault(line_start,_params)
            if old_tab_name != tab_name: print("Загрузка: Таблица '{}' - Ок".format(tab_name))
            old_tab_name = tab_name
        if self.debug: print(self.tabs) # Вывод отладочной информации.                    
        f.close()
            
def main():
    terminal = term_core()
    print('dx-terminal-emulator версия 1.0 распространятея по лицензии GNU GPL v3')
    print('разработчик Маргорин А.С.')
    while True:
        terminal.set_prompt()
        cmd = input(''.join(terminal.prompt)).strip(" \n").lower().split(" ")
        if len(cmd)>0:
            try:
                if cmd[0] == "exit": break
                else: 
                    terminal.parse(cmd)           
            except InputError as e:  
                print(e.message, e.expression)
                    
    return 0

if __name__ == '__main__':
    main()
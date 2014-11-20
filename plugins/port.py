# -*- coding: utf-8 -*-

import plugins.base

class plugin(plugins.base.baseplugin):
    header = """Конфигурация Портов:
===================================================================
  Порт    Тип сигн.   C Д Тн OC Исх. Вх.  ПH Шт ТнО Cр Гпн кАОН Вк 
-------------------------------------------------------------------
   0        1         2 3  4  5   6    7   8  9  10 11  12  13  14 
-------------------------------------------------------------------"""
    header1 = "- ИКМ-порты -------------------------------------------------------"
    footer = "==================================================================="
    helper = """Таблица 'Конфигурация портов':
  Параметры:
    0. 'Порт' - для какого порта;
    1. 'Тип сигнализации' - из списка по 'типу портов';
    2. 'C'  - флаг, в сервисе (+) или вне сервиса (-);
    3. 'Д'  - флаг 'донабора'.
    4. 'Тн' - флаг генерации цифр в DTMF, если возможно;
    5. 'ОС' - флаг генерации сигнала ОС в порты с донабором;
    6. 'Исх.'  - исходящая категория порта;
    7. 'Вход.' - входящая категория порта;
    8. 'ПН'  - вход в план нумерации;
    9. 'Шт'  - тарификационный шаблон;
   10. 'ТнО' - время ожидания ответа (сек);
   11. 'Ср'  - флаг 'сбора цифр в региcтр';
   12. 'Гпн' - вход в городской план нумерации;
   13. 'кАОН'- категория АОН;
   14. 'Вк'  - 'выделенный канал' в ИКМ с DSS1."""  
    number = 35
    name = 'port'
    max_line = 320 #192
    def_param = [{'name':'pt','default':0,0:'(L)Местный',1:'(T)Город',2:'(S)Спикер',3:'(MB)МБ',4:'UPN  (DSS1)',5:'Modem',6:'RS232',\
                  8:'S0   (DSS1)',9:'dx_arman',11:'T0_SL(DSS1)',12:'S0_SL(DSS1)',13:'caller_id',23:'IKM_R2_DTMF',24:'dx_sensor',\
                  25:'A3_SLI',26:'A3_SLO',27:'A4_RKS',31:'IKM_SLo_D',32:'IKM_SLo_MFC',33:'IKM_SLi_D',34:'IKM_SLi_MFC',35:'IKM_USL_D',\
                  36:'IKM_USL_1_D',37:'IKM_R2',38:'IKM_SLM_D',39:'IKM_SLM_MFC',41:'A4_SLo_MFC',42:'A4_SLi_MFC',43:'A4_SLio_MFC',\
                  44:'A4_600',45:'A4_SLM_D',46:'A4_SLM_MFC',47:'A4_2600',48:'A4_2100',49:'A4_600_750',50:'A4_ADASE',51:'A4_TDNV',\
                  52:'A4_TDNI',53:'A4_TA_BN',68:'IKM_USLM_D',69:'IKM_USL1M_D',72:'A4_SLo_D',73:'A4_SLi_D',74:'A4_SLio_D',79:'IKM_SLO_1_D',\
                  80:'A_E&M',81:'A_E&M_A',82:'A_E&M_WA',83:'A_E&M_NWA',87:'A6_USL_i',88:'A6_USL_s',89:'IKM_SLI_1_D',92:'DX_test',\
                  94:'IKM_DECT',97:'IKM_DSS1',98:'IKM_DSS1',100:'IKM_SS7'},
                 {'name':'genf','default':0,0:'-',1:'+'},
                 {'name':'wdft','default':0,0:'-',1:'+'},
                 {'name':'osf','default':0,0:'-',1:'+'},
                 {'name':'oc','default':'0'},
                 {'name':'ic','default':'0'},
                 {'name':'pa','default':'0'}, 
                 {'name':'tn','default':'0'},
                 {'name':'gt','default':'0'},
                 {'name':'colf','default':0,0:'-',1:'+'},
                 {'name':'ap','default':'0'},
                 {'name':'ka','default':'0'},
                 {'name':'d1i','default':0,0:'-',1:'+'}]
    
    write_param = {1:'pt',3:'genf',4:'wdft',5:'osf',6:'oc',7:'ic',8:'pa',9:'tn',10:'gt',11:'colf',12:'ap',13:'ka',14:'d1i'}
    value_pt = {'l':0,'t':1,'s':2,'mb':3,'upn':4,'modem':5,'rs232':6,\
                  's0':8,'dx_arman':9,'t0_sl':11,'s0_sl':12,'caller_id':13,'ikm_r2_dtmf':23,'dx_sensor':24,\
                  'a3_sli':25,'a3_slo':26,'a4_rks':27,'ikm_slo_d':31,'ikm_slo_mfc':32,'ikm_sli_d':33,'ikm_sli_mfc':34,'ikm_usl_d':35,\
                  'ikm_usl_1_d':36,'ikm_r2':37,'ikm_slm_d':38,'ikm_slm_mfc':39,'a4_slo_mfc':41,'a4_sli_mfc':42,'a4_slio_mfc':43,\
                  'a4_600':44,'a4_slm_d':45,'a4_slm_mfc':46,'a4_2600':47,'a4_2100':48,'a4_600_750':49,'a4_adase':50,'a4_tdnv':51,\
                  'a4_tdni':52,'a4_ta_bn':53,'ikm_uslm_d':68,'ikm_usl1m_d':69,'a4_slo_d':72,'a4_sli_d':73,'a4_slio_d':74,'ikm_slo_1_d':79,\
                  'a_e&m':80,'a_e&m_a':81,'a_e&m_wa':82,'a_e&m_nwa':83,'a6_usl_i':87,'a6_usl_s':88,'ikm_sli_1_d':89,'dx_test':92,\
                  'ikm_dect':94,'ikm_dss1':97,'ikm_dss1':98,'ikm_ss7':100}
    
    format_line = "{0:>9} {1:<11} + {2}  {3}  {4} {5:>3}  {6:>3} {7:>3} {8:>2} {9:>3} {10:>2} {11:>3} {12:>3} {13:>3}" 
     
    def __init__(self):
        pass
                
    def show(self, param, cl, cmd):
        """Функция выводит на экран содержимое таблицы PORT. """
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
                if (cl == '01') or (cl == '04') or (cl == '05'): # PCM-4                 
                    port_lo = counter
                else:
                    port_lo = counter//2
            if line == 128: 
                if (cl == '01') or (cl == '04') or (cl == '05'):
                    break # PCM-4
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
                if key == 'pt' or key == 'genf' or key == 'wdft' or key == 'osf' or key == 'colf' or key == 'd1i':     
                    p.append(plugin.def_param[i][v]) 
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
        except ValueError:
            print('Ошибка параметра Nпп(0) не может быть',line_number)
            return
        try:
            pn = int(param_number)
            if pn < 1 or pn > 14 : raise
        except:
            print('Ошибка параметра в диапазоне(1-14) не может быть',param_number)
            return
        key = plugin.write_param[pn] # Определяем имя параметра в который производим запись
        if key == 'genf' or key == 'wdft' or key == 'osf' or key == 'colf' or key == 'd1i':
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
        elif key == 'oc' or key == 'ic' or key == 'gt' or key == 'ka':
            if value.isdigit():
                v = int(value)
                if v == 0:
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                elif v > 0 and v < 255:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return 
            else:
                print("Недопустимое значение параметра:", value)
                return 
        elif key == 'pa' or key == 'ap':
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
        elif key == 'tn':
            if value.isdigit():
                v = int(value)
                if v == 0:
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                elif v > 0 and v < 33:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return 
            else:
                print("Недопустимое значение параметра:", value)
                return 
        elif key == 'pt':
            if value in plugin.value_pt:    
                v = plugin.value_pt.get(value)
                if v == 0:
                    try:
                        del param[cl][plugin.number][ln][key]
                    except:
                        pass
                elif v > 0 and v < 101:
                    param.setdefault(cl, tab).setdefault(plugin.number, lines).setdefault(ln,p)[key] = v 
                else:
                    print("Недопустимое значение параметра:", value)
                    return
            else:
                print("Недопустимое значение параметра:", value)
                return 
        print("Таблица 'PORT'. Запись значения {} в строку {} параметр {} произведена".format(value, line_number, param_number))
        #print(param)
import os,urllib2,urllib   
import time
import math
import sys
import re
import socket 

stock_folder = '.\\stock_data\\'

def get_stock_data(stock_code):
    count = 0
    while 1:
        try:
            #urllib.urlretrieve('http://table.finance.yahoo.com/table.csv?s=600795.ss','600795.csv')
            socket.setdefaulttimeout(15.0)
            if '0' == stock_code[0] or '3' == stock_code[0]:
                stock_name_info = stock_code + '.sz'
            elif '6' == stock_code[0] or '9' == stock_code[0] or '5' == stock_code[0]:
                stock_name_info = stock_code + '.ss'
            else:
                break
            url_string = 'http://table.finance.yahoo.com/table.csv?s=' + stock_name_info
            file_name = stock_folder + stock_code + '.csv'
            print 'try ' + str(count) + ': ' + url_string
            urllib.urlretrieve(url_string,file_name)
            break
            #time.sleep(1)
        except:
            count = count + 1
            #time.sleep(1)
            if count < 3:
                continue
            else:
                return stock_code
    #print stock_code
    return 'success'

#use yahoo web interface to get stock history data and store into xxx.csv file, xxx is stock number
def update_stock_data_main(argv):
    if 2 > len(argv) and 4 < len(argv):
        print 'input parameter invalid'
        print argv
        print 'e.g. python update_stock_data.py all_stock_code_list.txt  [start line number] [line number]'
        exit(0)
    
    try:
        stock_list = open(argv[1], 'rb')
    except:
        print 'open stock list failed %s' %(argv[1])
        print 'e.g. python update_stock_data.py all_stock_code_list.txt'
        exit(0)
    
    start_line = 0
    end_line = 0
    if 3 <=len(argv):
       start_line = int(argv[2])
    
    if 4 == len(argv):
        end_line = int(argv[3])
    
    if 0 != end_line:
        updatedstocklist = stock_list.readlines()[start_line:start_line + end_line]
    else:
        updatedstocklist = stock_list.readlines()[start_line:]

    update_succuss_list = []
    update_failed_list = []
    for each_stock in updatedstocklist:
        res = re.match('^(\d{6})\s*\r\n', each_stock)
        if res is not None:
            stock_code = res.group(1)
            status = get_stock_data(stock_code)
            if status  != 'success':
                update_failed_list.append(stock_code)
            else:
                update_succuss_list.append(stock_code)
    
    final_failed_list = []
    #try again for failed updated stock
    for failed_stock in update_failed_list:
        status = get_stock_data(stock_code)
        if status  == 'success':
            update_succuss_list.append(stock_code)
        else:
            final_failed_list.append(stock_code)
            
    stock_list.close()
    print 'Update stock finished  succuss:%d failed:%d' %(len(update_succuss_list), len(final_failed_list))
    return update_succuss_list
    
if __name__ == "__main__":
    print '''e.g. python update_stock_data.py all_stock_code_list.txt  [start line number] [line number]'''
    update_stock_data_main(sys.argv)
    
import cx_Oracle
import sys
import os
import time

#executing a shell command
def clear():
    #this is for linux
    #os.system('clear' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')


def format_date(date):
    return '%04d%02d%02d' % (date.tm_year, date.tm_mon, date.tm_mday)


def exists(conn, table, field, value):
    if type(value) == int:
        value = str(value)
    elif type(value) == str:
        value = "'" + value + "'"
    else:
        value = str(value)
        print('Warning: Unknown value type for \'exists\'')
    curs = conn.cursor()
    curs.execute('select count(*) from ' + table + 
        ' where ' + field + ' = ' + value)
    i = curs.fetchone()[0]
    curs.close()
    return i != 0


def exists2(conn, table, fvpairs):
    spairs = []
    for p in fvpairs:
        value = p[1]
        if type(value) == int:
            value = str(value)
        elif type(value) == str:
            value = "'" + value + "'"
        else:
            value = str(value)
            print('Warning: Unknown value type for \'exists\'')
        spairs.append(p[0]+'='+value)
    spairs = ' and '.join(spairs)

    curs = conn.cursor()
    curs.execute('select count(*) from ' + 
    table + ' where ' + spairs)
    i = curs.fetchone()[0]
    curs.close()
    return i != 0


def print_sql_result(curs):
    metadata = curs.description
    width = 0
    for column in metadata:
        print(column[0].ljust(column[2]),end=' ')
        width = width + column[2]
    print('')
    print('-'*width)

    i = 0
    rows = curs.fetchall()
    for row in rows:
        for column in row:
            print(str(column).ljust(metadata[i][2]),end=' ')
            i = i + 1
        print('')


def read_string_exact(message, maxchars = 0):
    if maxchars > 0:
        message = message + ' (Max ' + str(maxchars) + '):'
    else:
        message = message + ':'
    while True:
        print(message)
        l = sys.stdin.readline().rstrip()
        if len(l) == 0:
            return None
        if maxchars <= 0 or len(l) <= maxchars:
            return l
        print('Maximum limit of characters exceeded!')


def read_string(message, maxchars = 0):
    s = read_string_exact(message, maxchars)
    if s != None: 
        s = s.lower()
    return s


def read_date(message):
    message = message + ' (MM/DD/YYYY):'
    while True:
        print(message)
        l = sys.stdin.readline().rstrip()
        if len(l) == 0:
            return None
        try:
            i = time.strptime(l,'%d/%m/%Y')
            return i
        except ValueError:
            print('The value entered is not a date in the format MM/DD/YYYY!')


def read_int(message, llimit = None, ulimit = None):
    if llimit != None and ulimit != None:
        message = message + ' (' + str(llimit) + ' - ' + str(ulimit) + '):'
    elif llimit != None:
        message = message + ' ( > ' + str(llimit) + ' ):'
    elif ulimit != None:
        message = message + ' ( < ' + str(ulimit) + ' ):'
    else:
        message = message + ':'
    while True:
        print(message)
        l = sys.stdin.readline()
        if len(l) == 0:
            return None
        try:
            i = int(l)
            if llimit != None and i < llimit:
                print('The value entered is smaller than the minimum!')
                continue
            if ulimit != None and i > ulimit:
                print('The value entered is larger than the maximum!')
                continue
            return i
        except ValueError:
            print('The value entered is not an integer!')
            

def read_float(message, llimit = None, ulimit = None):
    if llimit != None and ulimit != None:
        message = message + ' (' + str(llimit) + ' - ' + str(ulimit) + '):'
    elif llimit != None:
        message = message + ' ( > ' + str(llimit) + ' ):'
    elif ulimit != None:
        message = message + ' ( < ' + str(ulimit) + ' ):'
    else:
        message = message + ':'
    while True:
        print(message)
        l = sys.stdin.readline()
        if len(l) == 0:
            return None
        try:
            i = float(l)
            if llimit != None and i < llimit:
                print('The value entered is smaller than the minimum!')
                continue
            if ulimit != None and i > ulimit:
                print('The value entered is larger than the maximum!')
                continue
            return i
        except ValueError:
            print('The value entered is not an integer!')



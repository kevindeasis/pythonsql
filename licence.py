import cx_Oracle
import sys
import common
import os.path
from vehicle import register_person

def print_opts():
    print('Select one of the options:')
    print('(1) Register a new person.')
    print('(2) Create a licence for a person.')
    print('    Or type \'exit\' to go back.')


def register_licence(conn):
    
    while True:
        licenceno = common.read_string('Licence Number', 15)
        if licenceno == None:
            return None
        if not common.exists(conn, 'drive_licence', 'licence_no', licenceno):
            break
        print('The licence number already exists!')

    while True:
        sin = common.read_string('SIN', 15)
        if sin == None:
            return None
        if common.exists(conn, 'drive_licence', 'sin', sin):
            print('The selected person already has a licence!')
            continue
        if common.exists(conn, 'people', 'sin', sin):
            break
        print('No person with this social insurance number exists!')

    lclass = common.read_string('Class', 10)
    if lclass == None:
        return None

    while True:
        upload = common.read_string('Upload Picture (y/n)')
        if upload == None:
            return None
        if upload == 'y':
            break
        if upload == 'n':
            image_data = None
            break
        print('Please select either \'y\' for yes or \'n\' for no!')

    if upload == 'y':
        while True:
            fimage = common.read_string_exact('Picture File')
            if fimage == None:
                return None
            if not os.path.isfile(fimage):
                print('File not found!')
                continue
            try:
                pimage = open(fimage, 'rb')
                image_data = pimage.read()
                pimage.close()
                break
            except:
                print('Failed to read image file!')
                continue
    
    issuing_date = common.read_date('Issuing Date')
    if issuing_date == None:
        return None
    issuing_date = common.format_date(issuing_date)
    expiring_date = common.read_date('Expiring Date')
    if expiring_date == None:
        return None
    expiring_date = common.format_date(expiring_date)

    try:
        curs = conn.cursor()
        curs.bindarraysize = 1
        #curs.setinputsizes(15,15,cx_Oracle.LONG_BINARY,8,8)
        #curs.executemany('insert into drive_licence values (:1,:2,:3,:4,:5)',
        #    [(licenceno,sin,lclass,image_data,issuing_date,expiring_date)])
        curs.setinputsizes(15,15,10,cx_Oracle.LONG_BINARY,8,8)
        curs.executemany('insert into drive_licence values (:1,:2,:3,:4,to_date(:5,\'yyyymmdd\'),to_date(:6,\'yyyymmdd\'))',
            [(licenceno,sin,lclass,image_data,issuing_date,expiring_date)])
        curs.close()
        conn.commit()
        return True
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if type(error) == str:
            print('Unknown error', error,'!')
        elif error.code == 1:
            print('Error: The licence number already exists or the person already has a licence!')
        elif error.code == 2291:
            print('Error: No person with this social insurance number exists!')
        else:
            print('Unknown error', error.code,'!')
        return False


def driver_licence_registration(conn):
    while True:
        common.clear()
        print_opts()

        line = sys.stdin.readline()
        if not line:
           return
        line = line.rstrip()
        if line == 'exit':
            return
        
        common.clear()

        try:
            r = None
            if line == '1':
                r = register_person(conn)
            elif line == '2':
                r = register_licence(conn)
            else:
                print('Invalid option!')
            
            if r == None:
                print('Operation cancelled.')
            elif r == True:
                print('Operation succeeded.')
            elif r == False:
                print('Operation failed.')
            
        except cx_Oracle.DatabaseError as e:
            print('Untreated exception...')
            error, = e.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Offset:", error.offset)
            print("Oracle-Error-Message:", error.message)
        sys.stdin.readline()


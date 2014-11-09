import cx_Oracle
import sys
import common
from common import print_sql_result
from common import format_date

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


def find_string(message, maxchars = 0):
    s = read_string_exact(message, maxchars)
    if s != None: 
        return s
    return s

def print_opts():
    print('Select one of the options:')
    print('(1) Issue a traffic ticket and record the violation given the "violator number", SIN.')
    print('(2) Issue a traffic ticket and record the violation given the Vehicle Number.')
    print('	 Or type \'exit\' to go back.')

	
def add_ticket(conn):
	
    while True:
        print("Enter the SIN of the violator")
        violator_no = common.read_string('SIN', 15)
        if violator_no == None:
            return None
        if common.exists(conn, 'people', 'sin', violator_no):
            break
        print('A violator with this social insurance number does not exists!')
		
    while True:
        print("Enter the SIN of the Police Officer")
        office_no = common.read_string('SIN', 15)
        if office_no == None:
            return None
        if common.exists(conn, 'people', 'sin', office_no):
            break
        print('A police officer with this social insurance number does not exists!')

    while True:
        print("Enter the Vehicle ID of the automobile used by the violator")
        vehicle_id = common.read_string('serial_no', 15)
        if vehicle_id == None:
            return None
        if common.exists(conn, 'vehicle', 'serial_no', vehicle_id):
            break
        print('A vehicle with that serial number does not exist!')
        
    while True:
        vtype = find_string('Type',10)
        if vtype == None:
            return None
        if common.exists(conn, 'ticket_type', 'vtype', vtype):
            break
        print('The selected ticket type does not exists!')
        
    vdate = common.read_date('Date of violation')
    if vdate== None:
        return None
        
    descriptions = common.read_string('Descriptions', 1024)
    if descriptions == None:
        return None
        
    place = common.read_string('Place', 20)
    if place == None:
        return None
    
       
    ticket_no = common.latest_int_key(conn,'ticket','ticket_no')
    ticket_no = (ticket_no)+1
    
    try:
        curs = conn.cursor()
        curs.bindarraysize = 1
        curs.setinputsizes(int,15,15,15,10,8,20,1024)
        curs.executemany('insert into ticket values (:1,:2,:3,:4,:5,to_date(:6,\'yyyymmdd\'),:7,:8)',[(ticket_no,violator_no,vehicle_id,office_no,vtype,format_date(vdate),place,descriptions)])
        curs.execute('select * from ticket')
        curs.close()
        conn.commit()
        return True
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 1:
            print('Error: A person with this social insurance number already exists!')
        else:
            print('Unknown error', error.code,'!')
        return False    


def violation_record(conn):

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
                r = add_ticket(conn)
            
            if line == '2':
                r = primary_owner_ticket(conn)
                
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


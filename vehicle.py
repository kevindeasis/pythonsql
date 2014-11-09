import cx_Oracle
import sys
import common
from common import print_sql_result
from common import format_date

def print_opts():
    print('Select one of the options:')
    print('(1) Register a new vehicle.')
    print('(2) Register a new owner.')
    print('(3) Assign an owner to a vehicle.')
    print('(4) View the available vehicle types.')
    print('    Or type \'exit\' to go back.')


def register_vehicle(conn):

    while True:
        serialno = common.read_string('Serial Number', 15)
        if serialno == None:
            return None
        if not common.exists(conn, 'vehicle', 'serial_no', serialno):
            break
        print('The serial number of the vehicle already exists!')

    maker = common.read_string('Maker', 20)
    if maker == None:
        return None
    model = common.read_string('Model', 20)
    if model == None:
        return None
    year = common.read_int('Year', 0, 9999)
    if year == None:
        return None
    color = common.read_string('Color', 10)
    if color == None:
        return None

    while True:
        vtype = common.read_string('Type')
        if vtype == None:
            return None
        if common.exists(conn, 'vehicle_type', 'type_id', vtype):
            break
        print('The selected vehicle type does not exists!')

    try:
        curs = conn.cursor()
        curs.bindarraysize = 1
        curs.setinputsizes(15,20,20,int,10,int)
        curs.executemany('insert into vehicle values (:1,:2,:3,:4,:5,:6)',
            [(serialno,maker,model,year,color,vtype)])
        curs.close()
        conn.commit()
        return True
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 1:
            print('Error: The serial number of the vehicle already exists!')
        elif error.code == 2291:
            print('Error: The selected vehicle type does not exists!')
        else:
            print('Unknown error', error.code,'!')
        return False


def register_person(conn):
    
    while True:
        sin = common.read_string('SIN', 15)
        if sin == None:
            return None
        if not common.exists(conn, 'people', 'sin', sin):
            break
        print('A person with this social insurance number already exists!')
    
    name = common.read_string('Name', 20)
    if name == None:
        return None
    height = common.read_float('Height', 0)
    if height == None:
        return None
    weight = common.read_float('Weight', 0)
    if weight == None:
        return None
    eyecolor = common.read_string('Eye Color', 10)
    if eyecolor == None:
        return None
    haircolor = common.read_string('Hair Color', 10)
    if haircolor == None:
        return None
    addr = common.read_string('Address', 50)
    if addr == None:
        return None

    while True:
        gender = common.read_string('Gender (m/f)')
        if gender == None:
            return None
        if gender == 'm' or gender == 'f':
            break
        print('Please select either \'m\' for male or \'f\' for female!')

    if gender == None:
        return None
    birthday = common.read_date('Birthday')
    if birthday == None:
        return None
    
    try:
        curs = conn.cursor()
        curs.bindarraysize = 1
        curs.setinputsizes(15,40,float,float,10,10,50,1,8)
        curs.executemany('insert into people values (:1,:2,:3,:4,:5,:6,:7,:8,to_date(:9,\'yyyymmdd\'))',
            [(sin,name,height,weight,eyecolor,haircolor,addr,gender,format_date(birthday))])
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


def add_owner(conn):
    
    while True:
        oid = common.read_string('Owner SIN', 15)
        if oid == None:
            return None
        if common.exists(conn, 'people', 'sin', oid):
            break
        print('The social insurance number does not exists!')
    
    while True:
        vid = common.read_string('Vehicle Serial Number', 15)
        if vid == None:
            return None
        if common.exists(conn, 'vehicle', 'serial_no', vid):
            break
        print('The serial number of the vehicle does not exists!')
    
    if not common.exists2(conn, 'owner', [('vehicle_id',vid),('is_primary_owner', 'y')]):
        print('This is the first owner of the selected vehicle and will automatically be set as primary.')
        powner = 'y'
        sys.stdin.readline()
    else:
        while True:
            powner = common.read_string('Primary Owner (y/n)')
            if powner == None:
                return None
            if powner == 'n':
                break
            if powner == 'y':
                if common.exists2(conn, 'owner', [('vehicle_id',vid),('is_primary_owner', 'y')]):
                    print('There is already a primary owner for the vehicle.')
                    while True:
                        change = common.read_string('Change primary owner (y/n)')
                        if change == None:
                            return None
                        if change == 'y':
                            break
                        if change == 'n':
                            powner == 'n'
                            break
                        print('Please select either \'y\' for yes or \'n\' for no!')
                break
            print('Please select either \'y\' for yes or \'n\' for no!')
    
    try:
        curs = conn.cursor()
        conn.begin()
        if powner == 'y':
            #curs.execute('begin update owner set is_primary_owner=\'n\' where vehicle_id=?; insert into owner values (?,?,?); end',(vid,oid,vid,powner))
            curs.execute('begin update owner set is_primary_owner=\'n\' where vehicle_id=\''+vid+'\'; insert into owner values (\''+oid+'\',\''+vid+'\',\''+powner+'\'); end;')
        else:
            curs.bindarraysize = 1
            curs.setinputsizes(15,15,1)
            curs.executemany('insert into owner values (:1,:2,:3)',
                [(oid,vid,powner)])
        curs.close()
        conn.commit()
        return True
    except cx_Oracle.DatabaseError as e:
        conn.rollback()
        error, = e.args
        if error.code == 1:
            print('Error: The selected person is already an owner of this vehicle!')
        else:
            print('Unknown error', error.code,'!')
        return False


def view_vehicle_types(conn):
    curs = conn.cursor()
    curs.execute('select * from vehicle_type')
    print_sql_result(curs)
    curs.close()
    return True


def new_vehicle_registration(conn):
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
                r = register_vehicle(conn)
            elif line == '2':
                r = register_person(conn)
            elif line == '3':
                r = add_owner(conn)
            elif line == '4':
                r = view_vehicle_types(conn)
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


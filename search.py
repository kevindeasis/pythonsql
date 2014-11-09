import cx_Oracle
import sys
import common
from common import print_sql_result
from common import format_date


def print_opts():
    print('Enter Licence number or SIN')
    print('	 Or type \'exit\' to go back.')

def search(conn,line): 
    while True:
        # you are given SIN
        if common.exists(conn, 'people', 'sin', line):
            x = 1
            break
        
        #you are give licence_no
        if common.exists(conn, 'drive_licence', 'licence_no', line):    		
            x = 2
            break
        return "No";
    if x == 1:
        print('SIN entered \n')
        string = "select  t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions from people p, ticket t where t.violator_no = p.sin and p.sin = " + str(line)
    	
        try:
            curs = conn.cursor()
            curs.execute(string)
            rows = curs.fetchall()
            for row in rows:
                print(row)
            curs.close()
            conn.commit()
            return True	

        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1:
                print('Error: Unable to print ticket information!')
            else:
                print('Unknown error', error.code,'!')
            return False
    if x == 2:
        print('Licence number entered')
        string2= "select  t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype, t.vdate, t.place, t.descriptions from people p, drive_licence d, ticket t where t.violator_no = p.sin and p.sin = d.sin and d.licence_no = " + str(line)
        try:
            curs = conn.cursor()
            curs.execute(string2)
            rows = curs.fetchall()
            for row in rows:
                print(row)
            curs.close()
            conn.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 1:
                print('Error: Unable to print ticket information!')
            else:
                print('Unknown error', error.code,'!')
            return False 

    else:
        return None


def search_engine(conn):
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
            r = search(conn,line)
            
            if r == "No":
                print("The licence number or SIN does not exist")
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
 

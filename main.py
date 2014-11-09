#!/usr/bin/python3
import cx_Oracle
import sys
import getpass
import common


from vehicle import new_vehicle_registration
from transaction import auto_transaction
from licence import driver_licence_registration
from violation import violation_record
from search import search_engine




#conn is our connection

def oracle_connect(username, password):
    conString=''+username+'/'+password+'@gwynne.cs.ualberta.ca:1521/CRS'
    return cx_Oracle.connect(conString)

def print_opts():
    print('Select one of the options:')
    print('(1) New Vehicle Registration.')
    print('(2) Auto transaction.')
    print('(3) Driver Licence Registration.')
    print('(4) Violation Record.')
    print('(5) Search Engine.')
    print('    Or type \'exit\' to exit the application.')

def main():

    print('Auto Registration System')

    conn = None
    while (conn == None):

        # Login
        username = input("Username [%s]: " % getpass.getuser())
        if not username:
            username = getpass.getuser()
        password = getpass.getpass()

        # Connection
        try:
        	#conString=''+username+'/' + password +'@gwynne.cs.ualberta.ca:1521/CRS'
        	#conn=cx_Oracle.connect(conString)
        	
##############oracle_connect????
           conn = oracle_connect(username, password)
        except cx_Oracle.DatabaseError as e:
        	#
        	#	error, = e.args
			#print( sys.stderr, "Oracle code:", error.code)
			#print( sys.stderr, "Oracle message:", error.message)
           print('Login failed!')
    print('Connected')

    while True:
    
    	#clears the command prompt
        common.clear()
        
        #print option
        print_opts()
	
		
		#read a one line string
		#stream from command line
        line = sys.stdin.readline()
        if not line:
           break
        line = line.rstrip()
        if line == 'exit':
            break

        try:
			#new vehicle registration
            if line == '1':
                new_vehicle_registration(conn)
                
        	#
            elif line == '2':
                auto_transaction(conn)
            elif line == '3':
                driver_licence_registration(conn)
            elif line == '4':
                violation_record(conn)
            elif line == '5':
                search_engine(conn)
            else:
                print('Invalid option!')
            
        except cx_Oracle.DatabaseError as e:
            print('Untreated exception...')
            error, = e.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Message:", error.message)

    print('Disconnecting...')
    
    #cursors closed???
    conn.close()

if __name__ == "__main__":
    main()


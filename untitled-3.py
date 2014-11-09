import cx_Oracle
import getpass

user = input("Username [%s]: " % getpass.getuser())
if not user:
    user=getpass.getuser()
pw = getpass.getpass()

conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
connection = cx_Oracle.connect(conString) 

cursor = connection.cursor()
pid=101
title="Window"
place="Utah" 
f_image  = open('window-sm.jpg','rb')
image  = f_image.read()

# prepare memory for operation parameters
cursor.setinputsizes(image=cx_Oracle.LONG_BINARY)
 
insert = """insert into pictures (photo_id, title, place, image)
   values (:photo_id, :title, :place, :image)"""
cursor.execute(insert,{'photo_id':pid, 'title':title,
                           'place':place, 'image':image})



connection.commit()
    # Housekeeping...
f_image.close()
cursor.close()
connection.close()


tutorial.py
	try:
		connection = cx_Oracle.connect(connStr)
		curs = connection.cursor()
		curs.execute(createStr)
		
		data = [('Quadbury', 101, 7.99, 0, 0),
			('Almond roca', 102, 8.99, 0, 0),
			('Golden Key', 103, 3.99, 0, 0)]

		cursInsert = connection.cursor()
		cursInsert.bindarraysize = 3
		cursInsert.setinputsizes(32, int, float, int, int)
		cursInsert.executemany("INSERT INTO TOFFEES(T_NAME, SUP_ID, PRICE, SALES, TOTAL) " 
			"VALUES (:1, :2, :3, :4, :5)", data)
		connection.commit()
		
		
		curs.execute("SELECT * from TOFFEES")
		rows = curs.fetchall()
		for row in rows:
			print(row)
		
		curs.close()
		cursInsert.close()
		connection.close()
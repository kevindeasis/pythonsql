

import cx_Oracle
import getpass

user = input("Username [%s]:" % getpass.getuser())
if not user: 
    user=getpass.getuser()

pw=getpass.getpass()

conString=''+user+'/'+pw+'@gwynne.cs.ualberta.ca:1521/CRS'
con = cx_Oracle.connect(conString)

curs = con.cursor()

statement=("DROP TABLE MOVIE")
curs.execute(statement)

statement=("CREATE TABLE MOVIE(title char(20),movie_number integer, primary key(movie_number))")
curs.execute(statement)

statement=("INSERT INTO MOVIE VALUES('Chicago',1)")
curs.execute(statement)

query=("SELECT Title, movie_number FROM Movie")
curs.execute(query)

rows = curs.fetchall()
for row in rows:
    print(row)
    
#rows = curs.fetchone()
#while (rows):
#print rows
#rows = curs.fetchone()

#rows = curs.fetchmany(numRows=3)
#for row in rows:
#print row
#

curs.close()

con.close()



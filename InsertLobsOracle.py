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

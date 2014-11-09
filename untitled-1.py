import sys
import time

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
            
print(read_date('Date of Violation'))
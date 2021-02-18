import serial, time, csv, os
from datetime import date
from datetime import datetime
import psycopg2
from psycopg2 import Error

# đăng nhập Skype
userSkype = 'asuzac-it.iot@outlook.com'# user, password skype
passSkype = 'iot@123987'
idChat = 'live:a697b99abc2b9460'
pathglobal = ''
#khai báo cổng serial
port = 'COM6'

# biến đếm gửi data
cout = 0
def connectSerial():
    # kết nối serial đọc dữ liệu
    try:
        
        ser = serial.Serial(port, 9600)
        values = ser.readline()
        valueString = str(values)
        valSensor =  valueString[2:6]
        # cout = 0
        # print(valSensor)
        return(valSensor)
    except:
        # bật function báo lỗi mất kết nối thiết bị
        warning = '-'
        # sendWarning()
        time.sleep(1)
        return (warning)

def writaData():
    global cout
    value = connectSerial()
    # ngày giờ hiện tại
    current_day = date.today()
    current_time = datetime.now().strftime("%H:%M:%S")

    # filenow là file hiện tại
    file_now = str(current_day) +'.csv' 
    new_code_path = os.path.join(os.getcwd(),'csv', file_now)
    fp = os.path.exists(new_code_path)
    # đường dẫn đến các file csv
    path = 'csv/'+file_now
    #kiểm tra file hiện tại
    if(fp == True):
        file_csv = open(path, 'a+', newline='') 
        wr = csv.writer(file_csv)
        wr.writerow([current_day, current_time, value])
        file_csv.close()
        
    else:
        # cread write
        file_csv = open(path, 'a+', newline='') 
        wr = csv.writer(file_csv)
        wr.writerow([current_day, current_time, value])
        file_csv.close()
        
    
    cout += 1
    print (cout)
    if (cout == 900):
        try:
            # Connect to an existing database
            connection = psycopg2.connect(user="vn_sensor",
                                        password="password",
                                        host="192.168.10.203",
                                        port="5432",
                                        database="vn_sensor")

            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server connecting")
            
            with open(new_code_path, 'r') as f:
                # Notice that we don't need the `csv` module.
                next(f) # Skip the header row.
                cursor.copy_from(f, 'acm01_imp_pf', sep=',')

            connection.commit()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                cout = 0
      

if __name__ == "__main__":
    while True:
        writaData()
        

# while True:



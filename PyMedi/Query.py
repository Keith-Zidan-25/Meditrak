from PyMedi import DBConnect
import sys
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

db = DBConnect.connect_to_database()
cursor = db.cursor()

#Check/Data Verification Functions
def check_email_exist_already(email):
    try:
        cursor.execute('SELECT PATIENT_ID FROM PATIENT WHERE USERNAME = %s',(email,))
        flag = cursor.fetchall()
        
        if flag:
            return False
        else:
            cursor.execute('SELECT DOCTOR_ID FROM DOCTORS WHERE EMAIL = %s',(email,))
            flag = cursor.fetchall()
            
            if flag:
                return False
            
            return True
    except Exception as error:
        print(error)

def login_user_check(username: str,passwrd: str):
    try:
        cursor.execute("SELECT PASSWORD FROM PATIENT WHERE USERNAME = %s",(username,))
        DBpasswrd = cursor.fetchone()

        if DBpasswrd is not None:
            DBpasswrd = DBpasswrd[0]
            user_type = 'patient'
            cursor.execute("SELECT PATIENT_ID FROM PATIENT WHERE USERNAME = %s",(username,))
            patient_id = cursor.fetchone()[0]
            return check_password(passwrd, DBpasswrd), user_type, patient_id
        else:
            cursor.execute('SELECT PASSWORD FROM DOCTORS WHERE EMAIL = %s',(username,))
            DBpasswrd =  cursor.fetchone()

            if DBpasswrd is not None:
                DBpasswrd = DBpasswrd[0]
                user_type = 'doctor'
                cursor.execute('SELECT DOCTOR_ID FROM DOCTORS WHERE EMAIL = %s',(username,))
                doctor_id = cursor.fetchone()[0]
                return check_password(passwrd, DBpasswrd), user_type, doctor_id
            else:
                return False, 'NONE', 'NONE'
    except Exception as e:
        print(e)
        
def check_password(given_password,original_password):
    if given_password == original_password:
        return True
    else:
        return False  
    
def check_schedule(date,time,doctor_ID):
    try:
        cursor.execute('''SELECT COUNT(*) FROM schedule 
                   WHERE doctor_id = %s AND 
                   ((CAST(%s AS TIME) < arrival_time OR 
                   CAST(%s AS TIME) >= leaving_time) 
                   OR HOLIDAY = %s)''', (doctor_ID, time, time, date))
        data = cursor.fetchone()[0]
        
        if data:
            return False
        else:
            return True
        
    except Exception as error:
        print(error) 

#Insert/Data Entry Functions
def insert_report(report_data, patient_id):
    cursor.execute("SELECT MAX(REPORT_NO) FROM REPORTS")
    report_no = cursor.fetchone()[0]
    if report_no:
        report_no += 1
    else:
        report_no = 1
    filename = patient_id + str(report_no)
    cursor.execute("INSERT INTO REPORTS (REPORT_FILE,PATIENT_ID,REPORT_NO,TYPE) VALUES (%s, %s, %s, %s)", (psycopg2.Binary(report_data),patient_id,report_no,filename))
    db.commit()
    
def insert_data_patients(data: list):
    try:
        cursor.execute("INSERT INTO PATIENT(PATIENT_ID,FIRST_NAME,LAST_NAME,USERNAME,DOB,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s)"
                       ,(data[0],data[1],data[2],data[3],data[4],data[5]))
        db.commit()
        
        return 'Success'
    except Exception as e:
        print(e)
    
def insert_data_doctor(data: list):
    try:
        cursor.execute("INSERT INTO DOCTORS(DOCTOR_ID,FIRST_NAME,LAST_NAME,EMAIL,EXPERIENCE,WORKPLACE) VALUES (%s,%s,%s,%s,%s,%s)"
                       ,(data[0],data[1],data[2],data[3],data[4],data[5]))
        db.commit()
        
        return 'Success'
    except Exception as e:
        print(e)
        
def book_appointment(patient_id,doctor_id,time,date):
    query = "INSERT INTO APPOINTMENT(PATIENT_ID,DOCTOR_ID,APPOINTED_TIME,APPOINTED_DATE) VALUES(%s,%s,%s,%s)"
    try:
        cursor.execute(query,(patient_id,doctor_id,time,date))
        db.commit()
    except Exception as error:
        print(error)
        
def change_password(new_password,user_id,user_type):
    try:
        if user_type == 'patient':
            cursor.execute("UPDATE TABLE PATIENT SET PASSWORD = %s WHERE PATIENT_ID = %s",(new_password,user_id))
            db.commit()
        else:
            cursor.execute("UPDATE TABLE DOCTORS SET PASSWORD = %s WHERE DOCTOR_ID = %s",(new_password,user_id))
            db.commit()
    except Exception as errors:
        print(errors)
    
    
#Get/Data Retrieval Functions
def get_email(doctor_id):
    cursor.execute("SELECT EMAIL FROM DOCTORS WHERE DOCTOR_ID = %s",(doctor_id,))
    data = cursor.fetchone()[0]
    return data

def get_patients_under_doctor(doctor_id):
    try:
        cursor.execute('''SELECT PATIENT_ID, FIRST_NAME, LAST_NAME FROM PATIENT
                       WHERE DOCTOR_ID = %s''', (doctor_id,))
        patients = cursor.fetchall()
        
        if patients:
            return patients
        else:
            return None
    except Exception as e:
        print(e)
        return None
        
def get_doctor_data(doctor_id):
    try:
        cursor.execute('''SELECT d.DOCTOR_ID, d.FIRST_NAME, d.LAST_NAME, d.EXPERIENCE, d.SPECIALISATION, 
                   d.WORKPLACE_NAME, wp.STREET, wp.AREA, wp.CONTACT_NO
                   FROM DOCTORS d
                   JOIN WORKPLACE wp ON d.WORKPLACE_NAME = wp.WORKPLACE_NAME
                   WHERE d.DOCTOR_ID = %s''',(doctor_id,))
        doctor_info = cursor.fetchone()
        return doctor_info
    except Exception as error:
        print(error)
        
def get_all_doctors():
    try:
        cursor.execute('''SELECT FIRST_NAME, LAST_NAME, SPECIALISATION, EXPERIENCE, DOCTOR_ID FROM DOCTORS''')
        doctors = cursor.fetchall()
        return doctors
    except Exception as errors:
        print(errors)
        
def get_doctor_profile_picture(doctor_id):
    try:
        cursor.execute("SELECT IMAGE FROM PROFILE_PICTURE WHERE DOCTOR_ID = %s",(doctor_id,))
        data = cursor.fetchone()[0]
        return data
    except Exception as errors:
        print(errors)

def get_user_data(username: str,type: str):
    try:
        if type == 'patient':
            cursor.execute('''SELECT FIRST_NAME,LAST_NAME, USERNAME, DOB  FROM PATIENT
                       WHERE PATIENT_ID = %s''',(username,))
            data = cursor.fetchone()[0:]
        else:
            cursor.execute('''SELECT FIRST_NAME, LAST_NAME, EMAIL, SPECIALISATION FROM DOCTORS
                           WHERE DOCTOR_ID = %s''',(username,))
            data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
        
def get_patient_appointment(patient_id):
    try:
        cursor.execute("SELECT APPOINTMENT_NO, APPOINTED_DATE, APPOINTED_TIME FROM APPOINTMENT WHERE PATIENT_ID = %s",(patient_id,))
        data = cursor.fetchall()
        return data
    except Exception as error:
        print(error)
        
def get_patient_meds(user_id):
    query = "SELECT MEDICINE_NAME, DOSAGE FROM MEDICINES WHERE PATIENT_ID = %s"
    try:
        cursor.execute(query, (user_id,))
        patient_meds = cursor.fetchall()
        return patient_meds
    except Exception as e:
        print("Error fetching patient medications:", e)
        return None
    
def get_patient_report(user_id):
    query = "SELECT REPORT_NO, REPORT_FILE,TYPE, DATE_OF_ISSUE FROM REPORTS WHERE PATIENT_ID = %s"
    try:
        cursor.execute(query,(user_id,))
        reports = cursor.fetchall()
        return reports
    except Exception as error:
        print(error)
    
def get_appointment_under_doctor(user_id):
    query = "SELECT APPOINTMENT_NO, APPOINTED_TIME, APPOINTED_DATE FROM APPOINTMENT WHERE DOCTOR_ID = %s"
    try:
        cursor.execute(query,(user_id,))
        data = cursor.fetchone()
        return data
    except Exception as error:
        print(error)
        
def get_medicine_from_database():
    try:
        cursor.execute("SELECT ")
    except Exception as errors:
        print(errors)
        
def get_report(file_no):
    cursor.execute("SELECT REPORT_FILE FROM REPORTS WHERE REPORT_NO = %s",(file_no,))
    data = cursor.fetchone()
    return data

def get_file_name(file_no):
    cursor.execute("SELECT TYPE FROM REPORTS WHERE REPORT_NO = %s",(file_no,))
    data = cursor.fetchone()[0]
    return data
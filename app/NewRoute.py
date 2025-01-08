from flask import Flask, render_template, request, redirect, url_for, session, send_file, send_from_directory
from PyMedi import AlphaNumericID as alphaID, Query, EmailVerification
import io
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'PyMedi')))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
            template_folder="../templates", 
            static_folder="../static")

app.secret_key = 'MediTrakJKL@2024SE'

@app.route('/medicines')
def medicines():
    medicine = [['Crocin','64','Pain-killer'],['Dolo','35','Paracetomol'],['Combiflam','45','Paracetomol'],
                ['Allegra','223','Antihistamines'],['Volini','243','Pain Relief Gel']]
    return render_template('medicine.html',medicines = medicine)

@app.route('/information')
def information():
    return render_template('AboutUsFAQpage.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_login')
def user_login():
    error = request.args.get('error')
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        return redirect(url_for('profile', username = username))
    else:
        return render_template('LoginPageNew.html',error = error)

@app.route('/patient_registration')
def patient_registration():
    email_exists = request.args.get('email_exists')
    return render_template('PatientRegistration.html',email_exists = email_exists)

@app.route('/verification')
def verification():
    wrong_code = request.args.get('wrong_code')
    return render_template('UserVerification.html',wrong_code = wrong_code)

@app.route('/patient_list/<doctorID>')
def patient_list(doctorID):
    data = Query.get_patients_under_doctor(doctorID)
    return render_template('PatientList.html',data)

@app.route('/doctor_list')
def doctor_list():
    doctorsList = Query.get_all_doctors()
    return render_template('DoctorListTemp.html',doctors = doctorsList)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    session['password'] = password
    flag, user_type, user_id = Query.login_user_check(username, password)
    
    if flag:
        session['username'] = username
        session['user_type'] = user_type
        session['user_id'] = user_id
        session['logged_in'] = True
        return redirect(url_for('profile', username = username))
    else:
        return redirect(url_for('user_login',error = True))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/show_report')
def show_report():
    type = 'display'
    report = Query.get_patient_report(user_id = 'PAAA0090')
    return render_template('reports.html',report = report, type = type)

@app.route('/report')
def report():
    type = 'Upload'
    return render_template('reports.html',report = None,type = type)

@app.route('/download/<file_no>')
def download_file(file_no):
    file_row = Query.get_report(file_no)
    file_content = file_row[0]
    filename = Query.get_file_name(file_no)
    return send_file(io.BytesIO(file_content),mimetype='application/octet-stream',as_attachment=True,download_name=filename)

@app.route('/upload', methods=['POST'])
def upload():
    report = request.files['report']
    if report:
        report_data = report.read()
    Query.insert_report(report_data, patient_id = 'PAAA0090')
    return redirect(url_for('index'))

@app.route('/register_patient',methods = ['POST'])
def register_patient():
    firstName = request.form['firstname']
    lastName = request.form['lastname']
    email = request.form['email']
    dateOfBirth = request.form['DOB']
    passwrd = request.form['password']
    
    patientID = alphaID.generate_id('patient')
    flag = Query.check_email_exist_already(email)
    
    if flag:
        verification_code = EmailVerification.send_verification_email(email)
        
        session['verification_code'] = verification_code
        data = [patientID,firstName,lastName,email,dateOfBirth,passwrd]
        session['user_data'] = data
        return redirect(url_for('verification'))
    else:
        return render_template('PatientRegistration.html',email_exists = True)
    
@app.route('/verify', methods = ['POST'])
def verify():
    verify_code = int(request.form['verification_code'])
    data = session.get('user_data')
    if 'verification_code' in session and session['verification_code'] == verify_code:
        Query.insert_data_patients(data)
        session.pop('verification_code')
        return redirect(url_for('user_login'))
    else:
        return redirect(url_for('verification',wrong_code = True))
    
@app.route('/profile/<username>')
def profile(username):
    if 'username' in session and session['username'] == username:
        user_type = session['user_type']
        user_id = session['user_id']
        data = Query.get_user_data(user_id,user_type)
        
        if user_type == 'patient':
            appointment = Query.get_patient_appointment(user_id)
            medicine = Query.get_patient_meds(user_id)
            reports = Query.get_patient_report(user_id)
            return render_template('Profile.html',title = 'Profile',user = data, user_type = user_type,
                                   appointments = appointment, medicines = medicine, medical_reports = reports)
        else:
            patients = Query.get_patients_under_doctor(user_id)
            appointments = Query.get_appointment_under_doctor(user_id)
            return render_template('Profile.html',title = 'Profile',user = data,user_type = user_type, 
                                   patients = patients, appointments = appointments)
    else:
        return redirect(url_for('index'))
    
@app.route('/change_password')
def change_password():
    return render_template('ChangePassword.html')

@app.route('/edit_password', methods = ['POST'])
def edit_password():
    old_pass_input = request.form['old-password']
    new_password = request.form['new-password']
    if 'password' in session and old_pass_input == session['password']:
        user_id = session['user_id']
        user_type = session['user_type']
        Query.change_password(new_password,user_id,user_type)
    username = session['username']
    return redirect(url_for('profile',username = username))
        
@app.route('/book_appointment', methods = ['POST'])
def book_appointment():
    if 'logged_in' in session and session['logged_in']:
        doctor = eval(request.form['username'])
        doctor_id = doctor[-1]
        session['doctor_id'] = doctor_id
        return redirect(url_for('selected_doctor_appointment'))
    else:
        return redirect(url_for('user_login'))
    
@app.route('/schedule_appointment', methods = ['POST'])
def schedule_appointment():
    date = request.form['date']
    time = request.form['time']
    doctor_id = session['doctor_id']
    
    flag = Query.check_schedule(date,time,doctor_id)
    data = Query.get_user_data(session['user_id'],session['user_type'])
    
    if flag:
        Query.book_appointment(session['user_id'],doctor_id,time,date)
        doc_email = Query.get_email(doctor_id)
        EmailVerification.send_appointment_notif(doc_email,data[0],data[1],date,time)
        session.pop('doctor_data')
        return redirect(url_for('selected_doctor_appointment',appointment_result = "success"))
    else:
        return redirect(url_for('selected_doctor_appointment',appointment_result = "unavailable"))
    
@app.route('/selected_doctor_appointment')
def selected_doctor_appointment():
    doctor_id = session['doctor_id']
    doctor = Query.get_doctor_data(doctor_id)
    session['doctor_data'] = doctor
    appointment_result = request.args.get('appointment_result')
    
    if appointment_result == 'success':
        message = 'Appointment booked successfully!'
    elif appointment_result == 'unavailable':
        message = 'Doctor unavailable at the selected date and time.'
    else:
        message = None
    return render_template('appointment.html',doctor = doctor, message = message)

@app.route('/image/<doctor_id>')
def profile_image(doctor_id):
    picture = Query.get_doctor_profile_picture(doctor_id)
    image_bytes = bytes(picture)
    return send_file(io.BytesIO(image_bytes), mimetype='image/png/jpg')
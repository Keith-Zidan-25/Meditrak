import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from PyMedi import DBConnect
def generate_id(type: str):
    db = DBConnect.connect_to_database()
    cursor = db.cursor()
    
    if type == 'doctor':
        cursor.execute("SELECT MAX(DOCTOR_ID) FROM DOCTORS")
    else:
        cursor.execute("SELECT MAX(PATIENT_ID) FROM PATIENT")
        
    last_id = cursor.fetchone()[0]
    
    if last_id:
        last_numeric = int(last_id[4:])
        last_alpha = last_id[0:4]

        if last_numeric < 9999:
            new_numeric = last_numeric + 1
            new_alpha = last_alpha

        else:
            new_numeric = 1
            new_alpha = increment_alpha(last_alpha)
            
        new_id = f"{new_alpha}{str(new_numeric).zfill(4)}"
        
        if len(new_id) > 8:
            return "Error"
        
    else:
        if type == 'doctor':
            new_id = 'DAAA0001'
        else:
            new_id = 'PAAA0001'
    
    return new_id

    
def increment_alpha(last_alpha: str):
    alphabet_part = last_alpha[1:]
    first_alpha = last_alpha[0]
    index = 0
    
    for char in alphabet_part:
        index = index * 26 + (ord(char) - ord('A') + 1)
    
    index += 1
    new_alphabet_part = ""
    
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        new_alphabet_part = chr(remainder + ord('A')) + new_alphabet_part
    
    new_alphabet_part = new_alphabet_part.zfill(3)
    
    return first_alpha + new_alphabet_part

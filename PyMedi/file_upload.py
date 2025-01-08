import imaplib
import email
import psycopg2
import DBConnect

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('rohitreddy9812@gmail', 'rohit@1234')
mail.select('inbox')

result, data = mail.search(None, 'ALL')
for num in data[0].split():
    result, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        file_data = part.get_payload(decode=True)

        conn = DBConnect.connect_to_database()
        cur = conn.cursor()
        cur.execute("INSERT INTO REPORTS (REPORT_FILE) VALUES (%s)", (psycopg2.Binary(file_data),))
        conn.commit()

        cur.close()
        conn.close()

# Logout from the email server
mail.logout()
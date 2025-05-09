import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Correo de prueba desde script Python.')
msg['Subject'] = 'Prueba SMTP'
msg['From'] = 'noreplyvirttob@gmail.com'
msg['To'] = 'juanjoseromerogomez0@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('noreplyvirttob@gmail.com', 'uiae txko tbon hbgf')
server.send_message(msg)
server.quit()

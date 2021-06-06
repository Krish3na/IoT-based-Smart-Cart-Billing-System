

import smtplib

from email.message import EmailMessage
from email.utils import make_msgid

def sendInvoice(emailCustomer):
	print(emailCustomer)
	#invoiceId, nameCustomer, phoneCustomer, )
	msg = EmailMessage()

	asparagus_cid = make_msgid()
	msg.set_content('This is an important message')
	msg.add_alternative('''\
	<html>
	<head></head>
	<body>
		<p>Dear Smart Kart Customer,</p>
		<p>
			Here is your Invoice, Please Check !!!        
		</p>
		</br>
		<img src="cid:{asparagus_cid}" />
		</br>
	</body>
	</html>
	'''.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

	with open("images/thanks.jpg", 'rb') as img:
		msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg', cid=asparagus_cid)
		
	with open("invoice.pdf", 'rb') as fp:
		pdf_data = fp.read()
		ctype = 'application/octet-stream'
		maintype, subtype = ctype.split('/', 1)
		msg.add_attachment(pdf_data, maintype=maintype, subtype=subtype, filename='invoice.pdf')

	fromEmail = 'Your mail'
	toEmail = emailCustomer

	msg['Subject'] = 'SMART KART sent you a Mail. Please check !'
	msg['From'] = fromEmail
	msg['To'] = toEmail

	s = smtplib.SMTP('smtp.gmail.com', 587)

	s.starttls()

	s.login(fromEmail,'Your Password')
	s.send_message(msg)
	s.quit()


import email, smtplib, ssl, base64;
import sys

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

smtp_server = "smtp.gmail.com"
port = 587  # For starttls

PART_SIZE = 100

class SMTP_Connection:



	# CONSTRUCTOR
	#email : the email to be logged in with
	#password : the password 
	def __init__(self, email, password):
		self.email = email;
		self.password = password;



	# TRY TO LOG IN
	def login(self):
	
		self.context = ssl.create_default_context();
		
		try:
			# Trying to connect
			self.connection = smtplib.SMTP(smtp_server,port)
			self.connection.ehlo() # Can be omitted
			self.connection.starttls(context=self.context) # Secure the connection
			self.connection.ehlo() # Can be omitted
			self.connection.login(self.email, self.password)
			return True;
			
		except Exception as e:
			print(e)
			return False;

		return False;
	


	# SEND EMAIL WITH SUBJECT AND BODY
	# subj : the subject of the mail 
	# msg : the body of the mail
	def send(self, receiver_email, subj, msg):

		if('\n' in subj):
			 raise ValueError("Custom Exception : Subject cannot have new-lines \\n");

		final_msg = "Subject: " + subj + "\n";
		final_msg += msg;
		self.connection.sendmail(self.email, receiver_email, final_msg);



	# SEND EMAIL WITH ONLY ONE ATTACHMENT
	# receiver_mail : the mail of the recipient
	# subj : the subject of the mail
	# finename : the name of the file
	# byte_data : tupe byte ex byte_data = open("test.txt", "rb").read();
	def send2(self, receiver_email, subj, filename, byte_data):
		# TODO: Multiple attachments (replacing filename with filename_list)
		if('\n' in subj):
			
			 raise ValueError("Custom Exception : Subject cannot have new-lines \\n");

		final_msg = MIMEMultipart()

		# Not sure if these are needed
		#final_msg['From'] = self.email
		#final_msg['To'] = receiver_email
		#final_msg['Date'] = formatdate(localtime=True)

		final_msg['Subject'] = subj

		# Email body
		#final_msg.attach(MIMEText("this is the body text"))

		# Split in parts of PART_SIZE bytes
		part_list = []
		i = 0
		while len(byte_data[i:]) > PART_SIZE:
			part = MIMEBase("application", "octet-stream")
			part.set_payload(byte_data[i:i+PART_SIZE])
			encoders.encode_base64(part)
			part_name = '{0:04d}'.format(int(i/PART_SIZE)) + filename + ".part"
			part_list.append(part_name)
			part.add_header(
				"Content-Disposition",
				f"attachment; filename= {part_name}",
			);
			#final_msg += part.as_string()
			final_msg.attach(part)
			i += PART_SIZE
			print("iteration number: " + str(i/PART_SIZE))

		# Add the last part
		part = MIMEBase("application", "octet-stream")
		part.set_payload(byte_data[i:])
		encoders.encode_base64(part)
		part_name = '{0:04d}'.format(int(i/PART_SIZE)) + filename + ".part"
		part_list.append(part_name)
		part.add_header(
			"Content-Disposition",
			f"attachment; filename= {part_name}",
		);
		final_msg.attach(part)


		lst_str = "0000" + '{0:04d}'.format(int(i/PART_SIZE)) + filename

		final_msg['Attachments'] = lst_str

		
		print(final_msg.as_string())
		input()
		

		self.connection.sendmail(self.email, receiver_email, final_msg.as_string());



	# CLOSE CONNETION
	def close(self):
		self.connection.quit();






import email, smtplib, ssl, base64;

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os import path

smtp_server = "smtp.gmail.com"
port = 587  # For starttls

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
	# byte_data : type byte ex byte_data = open("test.txt", "rb").read();
	def send2(self, receiver_email, subj, filename, byte_data):

		if('\n' in subj):
			 raise ValueError("Custom Exception : Subject cannot have new-lines \\n");


		# encode file and add hedaers
		part = MIMEBase("application", "octet-stream")
		part.set_payload(byte_data);
		encoders.encode_base64(part);
		part.add_header(
			"Content-Disposition",
			f"attachment; filename= {filename}",
		);


		final_msg = "Subject: " + subj + "\n";
		final_msg += part.as_string();

		self.connection.sendmail(self.email, receiver_email, final_msg);



	# CLOSE CONNETION
	def close(self):
		self.connection.quit();


	# SEND EMAIL WITH ONLY ONE ATTACHMENT
	# receiver_mail : the mail of the recipient
	# subj : the subject of the mail
	# file_path : path to the file we wish to send
	def send3(self, receiver_email, subj, file_path):

		if('\n' in subj):
			 raise ValueError("Custom Exception : Subject cannot have new-lines \\n");

		with open(file_path, 'rb') as f:
			file_data = f.read()
			file_name = path.split(file_path)[1]

			# encode file and add hedaers
			part = MIMEBase("application", "octet-stream")
			part.set_payload(file_data);
			encoders.encode_base64(part);
			part.add_header(
				"Content-Disposition",
				f"attachment; filename={file_name};"
			);


			final_msg = "Subject: " + subj + "\n";
			final_msg += part.as_string();

			self.connection.sendmail(self.email, receiver_email, final_msg);

		return

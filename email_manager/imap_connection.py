import os
import imaplib, email
import base64
import pprint


imap_addr = "imap.gmail.com"
imap_port = "993"

# This function needs refinement
def extract_info(raw_header):
	mail_header = raw_header.decode('utf-8')
	mailinfo = {
		"ID": mail_header.split("Message-ID: ", 1)[1].split("\r\n", 1)[0],
		"Sender": mail_header.split("From: ", 1)[1].split("\r\n", 1)[0],
		
	# TODO
	# "AttachmentList": mail_header.split("\nContent-Disposition: attachment; filename= ")[1:]
	}
	if len(mail_header.split("Subject: ", 1)) == 2:
		mailinfo["Subject"] = mail_header.split("Subject: ", 1)[1].split("\r\n", 1)[0]
	return mailinfo

class IMAP_Connection:

	def __init__(self, email, password):
		self.email = email
		self.password = password

	def login(self):
		try:
			self.mail = imaplib.IMAP4_SSL(imap_addr, imap_port)
			self.mail.login(self.email, self.password)
			return True
		
		except Exception as e:
			print(e)
			return False

		return False

	def get_email_list(self):
		self.mail.select()

		rv, data = self.mail.search(None, 'ALL')
		mail_ids = data[0]
		id_list = mail_ids.split()
		return id_list

	def get_specific_email_header_info(self, num):
	#Returns a dictionary with Number, ID, Sender, Subject
		rv, data = self.mail.fetch(num, '(BODY[HEADER])')
		raw_header = data[0][1]
		mailinfo = extract_info(raw_header)
		mailinfo["Number"] = num
		return mailinfo
		
	def get_email_headers_info(self):
	#Returns a list of dictionaries with Number, ID, Sender, Subject
		header_list = []

		id_list = self.get_email_list()
		for num in id_list:
			mailinfo = self.get_specific_email_header_info(num)
			header_list.append(mailinfo)
		return header_list

	def get_specific_email_attachments(self, num):
	#Saves email attachments to ./temporary/ if not already there
		rv, data = self.mail.fetch(num, '(RFC822)')
		raw_email = data[0][1]
		
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)
		
		for part in email_message.walk():
			if part.get_content_maintype() == 'multipart':
				continue
			if part.get('Content-Disposition') is None:
				continue
			fileName = part.get_filename()

			if bool(fileName):
				filePath = os.path.join('temporary/', fileName)
				if not os.path.isfile(filePath):
					fp = open(filePath, 'wb')
					fp.write(part.get_payload(decode=True))
					fp.close()
		return True

	def close(self):
		self.mail.logout();			

import getpass
import core.g as g 

from email_manager.smtp_connection import SMTP_Connection
from email_manager.imap_connection import IMAP_Connection

def run():
	while try_to_login() == False:
		continue;

def try_to_login():

	g.sender_email = input('Email : ');
	g.password = getpass.getpass();


	g.smtp_conn = SMTP_Connection(g.sender_email, g.password);
	print ("Trying to establish SMTP connection...")
	if(g.smtp_conn.login() == False):
		print("Error while trying to log in")
		return False;

	print("SMTP connection established!")


	g.imap_conn = IMAP_Connection(g.sender_email, g.password)
	print ("Trying to establish IMAP connection...")
	if g.imap_conn.login() == False:
		print("Error while trying to log in")
		return False;
	
	print("IMAP connection established!")

	return True;
	

	
		


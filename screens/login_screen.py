import getpass
from os import path
import core.g as g 

from email_manager.smtp_connection import SMTP_Connection
from email_manager.imap_connection import IMAP_Connection


def run():

	print("Trying to 'Easy Login'...");
	if(try_easy_login()):
		return;
	print("\n\n\n");
	print("Could not 'Easy Login'");

	print("Enter your credentials");
	while try_to_login() == False:
		continue;


# prompt the user to enter his credentials and try to log in
def try_to_login():

	g.sender_email = input('Email : ');
	g.password = getpass.getpass();

	return login(g.sender_email, g.password);
	


# try to login faster using the credetials.txt file
# fisrt line email
# second line password
def try_easy_login():

	file_name = "credentials.txt";
	exists = path.exists(file_name);
	isfile = path.isfile(file_name);

	if(exists and isfile):
		f = open(file_name, "r");
		lines = f.readlines();
		
		if(len(lines) != 2):
			print("The " + file_name + " sould have exactly 2 lines.");
			print("eg.");
			print("example@mail.com");
			print("password123");
			return False;
	
		# remove the \n from the end
		g.sender_email = lines[0][:-1];
		g.password = lines[1][:-1];

		return login(g.sender_email, g.password);

	return False;
	


# this function handles the login logic
def login(email, password):

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







import getpass;
from email_manager.connection import Connection
from email_manager.imap_connection import IMAP_Connection

# TMP test function

def test():

	email = input("Enter email : ");
	password = getpass.getpass();
	filename = input("Enter filename : ");

	print(email, password, filename)

	c = Connection(email, password);

	print("Trying to log in");
	if c.login() == False:
		print("Error while trying to log in");
		return;

	print("Logged in!!!");

	# send to yourself
	c.send2(email, ":)", filename, open(filename, "rb").read());

	print("Email sent");


	imap_con = IMAP_Connection(email, password)
	print ("Trying to establish IMAP connection...")
	if imap_con.login() == False:
		print("Error while trying to log in")
		return
	
	print("Connection established!")

	print("Getting email headers...")
	header_list = imap_con.get_email_headers_info()

	print("Checking last received email:")
	print(header_list[-1])

	if header_list[-1]["Subject"] == ":)":
		print("Getting files from happy email...")
		
		imap_con.get_specific_email_attachments(header_list[-1]["Number"])
		print("File(s) received!")


def run():
	print("Running ... ")
	
	test();
	
	print("Ended.")


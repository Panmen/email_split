
import getpass;
from email_manager.connection import Connection

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


def run():
	print("Running ... ")
	
	test();
	
	print("Ended.")


import getpass
from core.utilities import *;


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

	sender_email = input('Email : ');
	password = getpass.getpass();

	return login(sender_email, password);
	


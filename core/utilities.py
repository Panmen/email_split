from os import path
import core.g as g 


from email_manager.smtp_connection import SMTP_Connection
from email_manager.imap_connection import IMAP_Connection



#-------------------------------------- LOGIN STUFF ------------------------------------------

# try to login automatically using the credetials.txt file
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
		sender_email = lines[0][:-1];
		password = lines[1][:-1];

		return login(sender_email, password);

	return False;
	



# this function handles the login logic
# if connection was successful it returns True; False otherwise
def login(email, password):


	g.sender_email = email;
	g.password = password;

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







#---------------------------------------- DOWNLOAD / UPLOAD / LIST -------------------------------------

#this function downloads the specified file
# parameter name is the name of the file you want to download
#destination the folder in which the file will be saved; default " temporary/
# if it was successful it returns True; False otherwise
def download_file(name, destination = 'temporary/'):

	count = 0;
	print("%04d%s" % (count, name));
	l = g.imap_conn.get_email_list_by_subject("%04d%s" % (count, name));

	if(len(l) == 0):
		print("File " + name + " not found!");
		return False;

	if(not path.exists(destination)):
		print("Destimation path does not exist!");
		return False;

	f = open(destination + name, 'wb');
	
	while(len(l) > 0):
		print("Reading block : #%d" % count);
		data = g.imap_conn.get_specific_email_attachments_data(l[0]);
		print('got it');
		f.write(data);
		
		count = count + 1;	
		print("searching");
		l = g.imap_conn.get_email_list_by_subject("%04d%s" % (count, name));
		print("searched");

	f.close();
	print("Done");

	return True


def upload(filename, destination_email):
	# TODO
	pass

def list_available():
	# TODO
	pass


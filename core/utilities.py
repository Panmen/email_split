from os import path
from datetime import datetime;
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

		return login(sender_email, password), sender_email;

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


	if(g.imap_conn is None):
		print("There is no IMAP connection");
		return False;

	if(not path.exists(destination)):
		print("Destimation path does not exist!");
		return False;

	count = 0;
	print("Searching for" + "ES_%04d%s" % (count, name));
	l = g.imap_conn.get_email_list_by_subject("ES_%04d%s" % (count, name));

	if(len(l) == 0):
		print("File " + name + " not found in inbox!");
		return False;


	f = open(destination + name, 'wb');
	
	while(len(l) > 0):
		print("Reading block : #%d" % count);
		data = g.imap_conn.get_specific_email_attachments_data(l[0]);
		print('got it');
		f.write(data);
		
		count = count + 1;	
		print("searching");
		l = g.imap_conn.get_email_list_by_subject("ES_%04d%s" % (count, name));
		print("searched");

	f.close();
	print("Done");

	return True


#send file to destination_email
# returns True if successful
def send_file(file_path, destination_email):
	CHUNK_SIZE = 14000000; # ~ 14MB


	if(g.smtp_conn is None):
		print("There is no SMTP connection");
		return False;
	
	if(not path.exists(file_path)):
		print("Path " + file_path +  " does not exist!");
		return False;

	if(not path.isfile(file_path)):
		print(file_path + " is not a file!");
		return False;

	f = open(file_path, 'rb');


	file_full_name = path.basename(file_path);
	file_name_parts = file_full_name.rsplit(".", 1); # split at last occurrence
	time_stamp = datetime.now().strftime("_%d-%m-%Y_%H-%M-%S"); 
	file_name = file_name_parts[0] + time_stamp + "." + file_name_parts[1];


	# SEND beacon email to be used by list function
	subject = "ES_BEACON";
	body = file_name;
	g.smtp_conn.send(destination_email, subject, body);	

	i = 0;
	chunk = f.read(CHUNK_SIZE);
	
	while(len(chunk) > 0): # while there are still data

		print("Sending chunk #%d, len(chunk)=%d" % (i, len(chunk)));

		#send data
		filename = "data";
		subject = "ES_%04d%s" % (i, file_name);
		g.smtp_conn.send2(destination_email, subject, filename, chunk);	

		# read next chunck and i++
		i = i + 1;
		chunk = f.read(CHUNK_SIZE);



	f.close();
	print("Uploaded successfully.")
	return True;

def list_available():

	print("Searching for available files");

	
	id_list = g.imap_conn.get_email_list_by_subject("ES_BEACON");

	files = [];

	for num in id_list:
		files.append(g.imap_conn.get_email_body(num).rstrip());

	print(files);

	return files;


from os import path
from os import remove
from core import g
from split_manager import splitter

def run():

	while True:
		file_path = input('File path : ');

		exists = path.exists(file_path);
		isfile = path.isfile(file_path);

		if(exists and isfile):
			print("Sending : " + file_path);
			send_file(file_path, g.sender_email)
			print("File sent!")
			break;

		elif(exists == False):
			print("File does not exist");

		elif(isfile == False):
			print("It is not a file");

def send_file(file_path, receiver_email):
	filename_list = splitter.split(file_path)
	for filename in filename_list:
		g.smtp_conn.send3(receiver_email, filename, "temporary/" + filename)
		# Delete temp file as it is no longer needed
		remove("temporary/" + filename)
	return



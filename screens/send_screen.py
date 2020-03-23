from os import path


def run():

	while True:
		file_path = input('File path : ');

		exists = path.exists(file_path);
		isfile = path.isfile(file_path);

		if(exists and isfile):
			print('Sending : ' + file_path);
			# TODO - add sending functionality
			break;

		elif(exists == False):
			print("File does not exist");

		elif(isfile == False):
			print("It is not a file");


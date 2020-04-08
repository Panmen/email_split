from core import g


def run():
	
	name = input("Enter the filename : ")
	fetch_file(name);



def fetch_file(name):

	count = 0;
	print("%04d%s" % (count, name));
	l = g.imap_conn.get_email_list_by_subject("%04d%s" % (count, name));

	if(len(l) == 0):
		print("File " + name + " not found!");
		return;

	f = open("temporary/" + name, 'wb');
	
	while(len(l) > 0):
		print("Reading block : #%d" % count);
		data = g.imap_conn.get_specific_email_attachments_data(l[0]);
		f.write(data);
		
		count = count + 1;	
		l = g.imap_conn.get_email_list_by_subject("%04d%s" % (count, name));

	f.close();
	print("Done");

	pass

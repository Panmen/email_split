import screens.send_screen as send_screen
import screens.receive_screen as receive_screen
from core.utilities import *;


def run():

	while True:
		ans = input('(S)Send, (R)Receive, (L)List, (E)Exit : ');

		if(ans.upper() == 'S'): # send
			send_screen.run();
			continue;

		elif(ans.upper() == 'R'): #receive
			receive_screen.run();
			continue;

		elif(ans.upper() == "L"):
			list_available();
			continue;

		elif(ans.upper() == 'E'): #exit
			break;
		

import screens.send_screen as send_screen
import screens.receive_screen as receive_screen


def run():

	while True:
		ans = input('(S)Send, (R)Receive, (E)Exit : ');

		if(ans.upper() == 'S'): # send
			send_screen.run();
			continue;

		elif(ans.upper() == 'R'): #receive
			receive_screen.run();
			continue;

		elif(ans.upper() == 'E'): #exit
			break;
		

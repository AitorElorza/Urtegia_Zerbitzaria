#!/usr/bin/env python3

import socket, os, signal, select, random
from time import sleep
PORT = 50000
MAX_WAIT = 120

idak = ['GI317','NA071','HU119','ZO547','QE865']
izenak = ['GI317Urkulu','NA071Esa','HU119Mediano','ZO547Seto','QE865Fagna']
irekiera = [456,789,123,654,864]
betetzea = [165,498,135,498,653]

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

s.bind( ('', PORT) )


signal.signal( signal.SIGCHLD, signal.SIG_IGN )
while True:
	buf, bez_helb = s.recvfrom( 1024 )
	
	
	if not os.fork():

		s.close()
		elkarrizketa = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		elkarrizketa.connect(bez_helb)
		elkarrizketa.send(buf)
		while True:
			message= ''			
			mezua = elkarrizketa.recv( 1024 )
			agin = mezua.decode()
			
			if not agin:
				break
			elif (len(agin)<4):
				message = 'ER-01'
			else:	
				if (agin[:4] == 'GATE'):
					if (len(agin)!=12):
						message = 'ER-03'
					else:
						aux=False
						for i in range(0,len(idak)):
							if(idak[i]==agin[4:9]):
								aux=True
								irekiera[i]=agin[9:]
								break
						if not aux:
							message = 'ER-11'
						else:
							message = 'OK+'

				if (agin[:4] == 'STAT'):
					if (len(agin)!=9):
						message = 'ER-03'
					else:
						aux=False
						print(agin[4:9])
						for i in range(0,len(idak)):

							if(idak[i]==agin[4:9]):
								aux=True
								break
						if not aux:
							message = 'ER-12'
						else:
							message = 'OK+'+ str(irekiera[i])



				if (agin[:4] == 'LEVE'):
					if (len(agin)>9):
						message = 'ER-02'
					else:
						rand = random.randint(0,999)
						if rand <750: ##Ez dago arazorik
							if (len(agin)==4):
								message = 'OK+'
								for i in range(0,len(betetzea)):
									if i==len(betetzea)-1:
										message = message + str(betetzea[i])
									else:
										message = message + str(betetzea[i]) +':'
							elif (len(agin)==9):
								aux= False
								for i in range(0,len(idak)):
									if(idak[i]==agin[4:9]):
										aux=True
										break
								if not aux:	
									message = 'ER-14'
								else:
									message = 'OK+'+ str(betetzea[i])
							else:
								message = 'ER-04'

						else:##Arazoren bat egon da
							message= 'ER-14'


				if (agin[:4] == 'NAME'):
					if (len(agin)>4):
						message = 'ER-02'
					else:
						rand = random.randint(0,999)
						if rand <750: ##Ez dago arazorik
							message = 'OK+'
							for i in range(0,len(izenak)):
								if i==len(izenak)-1:
									message = message + izenak[i]
								else:
									message = message + izenak[i] +':'
						else:##Arazoren bat egon da
							message = 'ER-13'
					
			elkarrizketa.send(message.encode())
		print( "Konexioa ixteko eskaera jasota." )
		elkarrizketa.close()
		exit(0)


	
s.close()
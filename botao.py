import os
from datetime import datetime
import time
import OPi.GPIO as GPIO
import requests
import json

#Variaveis globais:
NumeroAcionamentosBotao = 0

#GPIOs utilizados:
GPIOBotaoEmergencia = 18 #Broadcom pin 18 (P1 pin 12)

GPIO.setboard(GPIO.PCPCPLUS)    # Orange Pi PC board

#Funcao: prepara I/Os
#Parametros: nenhum
#Retorno: nenhum
def PreparaIOs():
	#configura GPIO do botao como entrada e com pull up (do SoC Broadcom)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIOBotaoEmergencia, GPIO.IN)
        return

#Funcao: envia notificacao via pushbullet
#Parametros: numero do acionamento do botao
#Retorno: nenhum
def EnviaNotificacaoPushbullet(Numero):
	now = datetime.now()
	StringDataHora = str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" em "+str(now.day)+"/"+str(now.month)+"/"+str(now.year)

	StringMsg = "Acionamento numero "+str(Numero)+" do botao de emergencia. Botao acionado por ultimo em "+StringDataHora+"."
	
	print(StringMsg)
	
	return

#Funcao: verifica acionamento e desacionamento do botao de emergencia
#Parametros: nenhum
#Retorno: nenhum
def VerificaBotaoEmergencia():
	global NumeroAcionamentosBotao

	#se o botao foi pressionado, envia a notificacao. 
	#caso contrario, nada e feito.
	if (GPIO.input(GPIOBotaoEmergencia) == 1):
		#Atualiza contagem de acionamentos e envia notificacao pelo pushbullet		
		NumeroAcionamentosBotao = NumeroAcionamentosBotao + 1
		EnviaNotificacaoPushbullet(NumeroAcionamentosBotao)		

		#delay para debouncing (50ms)
		time.sleep(0.050)

		#aguarda botao ser solto
		while (GPIO.input(GPIOBotaoEmergencia) == 1):
			continue

	return

#------------------------
#   Programa principal
#-----------------------
time.sleep(30)
PreparaIOs()

while True:
	print('iniciado!')
	VerificaBotaoEmergencia()

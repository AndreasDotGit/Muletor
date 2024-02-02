from methods import AppendMessageForDBConnection as AMDC
from colorama import Fore, Back
from pathlib import Path
import os

os.system('cls')
print('''***************DISCLAIMER***************
Il software utilizzato è mirato a manipolare i codici
dei flussi mulesoft. Qualora venisse effettuato
per sbaglio qualsiasi intervento, si prega di''', 
Fore.YELLOW + 'REVERTARE' + Fore.RESET + '.\n' +
Back.YELLOW + Fore.BLACK + '''\nIl programma funziona solo se la cartella è posizionata al livello del pom.xml\n''' + Back.RESET + Fore.RESET +
'***************DISCLAIMER***************' + Back.RESET + '\n')

while(True):
    basePath = format(Path().absolute().parents[0])
    if 'pom.xml' in os.listdir(format(basePath)):
        print(Back.LIGHTBLUE_EX + Fore.WHITE + '|HOME' + Back.RESET + Fore.RESET)
        print("Azioni disponibili:")
        print('1) APPEND SELECT TO DB (usato per chiudere le connessioni del DB)')
        print('0) Exit\n')
        usr = input("Scegli una opzione: ")
        if(usr == '1'):
            os.system('cls')
            AMDC.init(basePath)
        elif(usr == '0'):
            os.system('cls')
            exit(1)
        else:
            os.system('cls')
            print(Fore.YELLOW + "Input non valido" + Fore.RESET + '\n')
    else:
        print(Back.RED + Fore.WHITE + "Pom non trovato" + Back.RESET + Fore.RESET)
        exit(1)
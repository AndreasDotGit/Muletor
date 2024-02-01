import xml.etree.ElementTree as ET
import lxml.etree as let
import uuid
from pathlib import Path
import os

from colorama import Fore, Back, Style


def __dirControl(srcDir):
    listDir = os.listdir(format(srcDir))
    for content in listDir:
        if '.' in content:
            if(content != 'pom.xml' and content != 'global.xml'):
                print(Fore.BLACK + Back.WHITE + "File trovato:", content + Fore.RESET + Back.RESET)
                __appendTransfromAfterSelect(srcDir + '\\' + content)
        else:
            print('Trovata cartella', Fore.YELLOW + Back.BLACK + content + Fore.RESET + Back.RESET + ", controllo il contenuto:" )
            __dirControl(srcDir + '\\' + content)


def __appendTransfromAfterSelect(fileName):
    print("FILE", fileName)
    let.register_namespace('mule', 'http://www.mulesoft.org/schema/mule/ee/core')
    let.register_namespace('doc', 'http://www.mulesoft.org/schema/mule/documentation')
    tree = let.parse(fileName,parser = let.XMLParser(strip_cdata=False))
    muleRoot = tree.getroot()
    for flow in muleRoot:
        print('\t' + Fore.BLUE + Back.RESET +"Flusso", flow.attrib['name'] + Fore.RESET + Back.RESET)
        for element in flow:
            if element.tag.find('}') != -1:
                if element.tag.split('}')[1] == 'select':
                    print('\t\t' + Fore.GREEN + Back.RESET + 'SELECT TROVATA' + Fore.RESET)
                    if 'target' in element.attrib:
                        nameResSelect = element.attrib['target']
                        print('\t\t' +'Select con la variabile:', Fore.GREEN + element.attrib['target'] + Fore.RESET)
                    else:
                        print('\t\t' + "Select senza variabile, verrà utilizzato il payload")
                        nameResSelect = 'payload'
                    
                    transfrom = let.Element('{http://www.mulesoft.org/schema/mule/ee/core}transform')
                    transfrom.set('{http://www.mulesoft.org/schema/mule/documentation}name', nameResSelect)
                    newUUID = str(uuid.uuid1())
                    transfrom.set('{http://www.mulesoft.org/schema/mule/documentation}id', newUUID)
                    tMessage = let.Element('{http://www.mulesoft.org/schema/mule/ee/core}message')
                    if nameResSelect == 'payload':
                        tPayload = let.Element('{http://www.mulesoft.org/schema/mule/ee/core}set-payload')
                        tPayload.text = let.CDATA('%dw 2.0\noutput application/json\n---\npayload map $')
                        tMessage.append(tPayload)
                        transfrom.append(tMessage)
                        print('\t\t' + Fore.BLACK + Back.GREEN + 'Transfrom message creato per il payload' + Fore.RESET + Back.RESET)
                    else:
                        transfrom.append(tMessage)
                        tVars = let.Element('{http://www.mulesoft.org/schema/mule/ee/core}variables')
                        tVar = let.Element('{http://www.mulesoft.org/schema/mule/ee/core}set-variable')
                        tVar.set('variableName', nameResSelect)
                        tStr = ('%dw 2.0\noutput application/json\n---\nvars.' + nameResSelect + ' map $')
                        tVar.text= let.CDATA(tStr)
                        tVars.append(tVar)
                        transfrom.append(tVars)
                        print('\t\t' + Fore.BLACK + Back.GREEN + 'Transfrom message creato per la variabile', nameResSelect + Fore.RESET + Back.RESET)
                    element.addnext(transfrom)
                    tree.write(fileName, encoding="utf-8", xml_declaration=True, pretty_print=True)
                    print("\t\tIl file", Fore.CYAN + fileName + Fore.RESET, 'è stato sovrascritto')



def AppendMessageForDBConnection(pomPath):
    print(Back.LIGHTBLUE_EX + Fore.WHITE + '|HOME|APPEND SELECT TO DB' + Back.RESET + Fore.RESET)
    print(Fore.YELLOW + '''
ATTENZIONE: Questa opzione andrà a controllare ogni file xml sotto la cartella \\src\\main\\mule,
manipolando il codice appendendo una Transform Message dopo ogni palette SELECT trovata in ogni flusso,
riscrivendo e riformattando l'intero codice.
''' +
Fore.BLACK +
Back.YELLOW + 
"Si prega di controllare il codice in fase di commit dopo l'esecuzione dello script." + Fore.RESET + Back.RESET + '\n')
    
    while(True):
        usr = input("Vuoi continuare? [Y/N]: ")
        if usr == 'Y' or usr == 'y':
            srcDir = format(pomPath)+ '\\src\\main\\mule'
            __dirControl(srcDir)
            break
        elif usr == 'N' or usr == 'n':
            os.system('cls')
            break
        else:
            print(Fore.YELLOW + 'Input non valido' + Fore.RESET + '\n')

    

   


    
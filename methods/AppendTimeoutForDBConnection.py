import xml.etree.ElementTree as ET
import lxml.etree as let
import uuid
import os
from colorama import Fore, Back

#NAMESPACE
nsMule = 'http://www.mulesoft.org/schema/mule/ee/core'
nsDoc = 'http://www.mulesoft.org/schema/mule/documentation'

#TAG
tagFlow = '{http://www.mulesoft.org/schema/mule/core}flow'
tagSubFlow = '{http://www.mulesoft.org/schema/mule/core}sub-flow'
tagDB = ['{http://www.mulesoft.org/schema/mule/db}select', '{http://www.mulesoft.org/schema/mule/db}update', '{http://www.mulesoft.org/schema/mule/db}insert', '{http://www.mulesoft.org/schema/mule/db}stored-procedure']


#COUNTER
counterAppendedLog = 0


def init(pomPath):
    print(Back.LIGHTBLUE_EX + Fore.WHITE + '|HOME|APPEND TIMEOUT MESSAGE TO DB' + Back.RESET + Fore.RESET)
    print(Fore.YELLOW + '''
ATTENZIONE: Questa opzione andrà a controllare ogni file xml sotto la cartella \\src\\main\\mule,
manipolando il codice appendendo una la proprietà queryTimeout dopo ogni palette DB trovata in ogni flusso,
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
            __counterAppendedLog()
            break
        elif usr == 'N' or usr == 'n':
            os.system('cls')
            break
        else:
            print(Fore.YELLOW + 'Input non valido' + Fore.RESET + '\n')


def __dirControl(srcDir):
    listDir = os.listdir(format(srcDir))
    for content in listDir:
        if '.' in content:
            if(content != 'pom.xml' and content != 'global.xml' and '.xml' in content):
                #print(Fore.BLACK + Back.WHITE + "File trovato:", content + Fore.RESET + Back.RESET)
                __appendTimeoutInDB(srcDir + '\\' + content)
        else:
            #print('Trovata cartella', Fore.YELLOW + Back.BLACK + content + Fore.RESET + Back.RESET + ", controllo il contenuto:" )
            __dirControl(srcDir + '\\' + content)


def __appendTimeoutInDB(fileName):
    print("FILE", Fore.YELLOW + fileName + Fore.RESET)
    let.register_namespace('mule', nsMule)
    let.register_namespace('doc', nsDoc)
    tree = let.parse(fileName,parser = let.XMLParser(strip_cdata=False, remove_comments=True))
    muleRoot = tree.getroot()
    for flow in muleRoot:
        if flow.tag in [tagFlow, tagSubFlow] :
            print('\t' + Fore.BLUE + Back.RESET +"Flusso", flow.attrib['name'] + Fore.RESET + Back.RESET)
            for element in flow:
                __elemControl(fileName, tree, element, treeLog=element.tag.split('}')[1])


def __elemControl(fileName, tree, element, treeLog):
    c_treeLog = treeLog
    if element.tag in tagDB:
        print('\t\t' + Fore.GREEN + 'Path: ' + Fore.RESET + treeLog + ' > ' + Fore.GREEN + 'DB OPERATION: ' + element.tag + ' TROVATA' + Fore.RESET)
        __selectAction(fileName, tree, element)
    else:
        for element in element:
            treeLog = treeLog + ' > ' + element.tag.split('}')[1]
            __elemControl(fileName, tree, element, treeLog)
            treeLog = c_treeLog


def __selectAction(fileName, tree, element):
    if 'queryTimeout' in element.attrib:
        print('\t\t' +'DB Operation con la queryTimeout: ', Fore.GREEN + element.attrib['queryTimeout'] + Fore.RESET)
    else:
        nameTimeoutQuery = '${database.timeoutSec}'
        print('\t\t' + "DB Operation senza queryTimeout, inietto l'attributo " + nameTimeoutQuery) 
        element.set('queryTimeout', nameTimeoutQuery)
        tree.write(fileName, encoding="utf-8", xml_declaration=True, pretty_print=True)
        global counterAppendedLog
        counterAppendedLog += 1
        print("\t\tIl file", Fore.CYAN + fileName + Fore.RESET, 'è stato sovrascritto\n')

def __counterAppendedLog():
    global counterAppendedLog
    print("Sono stati appesi ", Fore.CYAN + str(counterAppendedLog) + Fore.RESET, "Query Timeout Message")
    counterAppendedLog = 0
from ply.yacc import yacc
import re
import codecs
import os
from sys import stdin
from analizadorLexico import tokens
from analizadorSemantico import *
from pip._vendor.distlib.compat import raw_input

toVerify = []

precedence = (
   ('right','ID','IF'),
   ('right','DEF', 'EXEC'),
   ('right', 'SET'),
   ('right', 'LBRACKET', 'RBRACKET'),
   ('left','PRINTLN'),
   ('left','NEQUAL','EQUAL'),
   ('left','LT','LTE','GT','GTE'),
   ('left','PLUS','MINUS'),
   ('left','TIMES','DIVIDE','WDIVIDE'),
   ('left', 'MODULE'),
   ('left','EXPONENT'),
   ('left','LPARENTHESES','RPARENTHESES'),
   )

#Whole coding from user verified here
def p_program(p):
    '''program : funcList'''
    print('Variables: ' + str(returnVariables()) + ', Moves: ' + str(returnMoves()) + ', PrintList: ' + str(returnPrintList()))

#Variables, movements, procedures and statements checked here
def p_block(p):
    '''block : varDecl moveDecl procDecl statementDecl''' #funcDecl enCasoDecl'''
    p[0] = str(p[1]) + ',' + str(p[2]) + ',' + str(p[3]) + ',' + str(p[4])

#List of blocks
def p_blockList1(p):
    '''blockList : block'''
    p[0] = p[1]

def p_blockList2(p):
    '''blockList : blockList block'''
    p[0] = p[1] + p[2]

#List of functions
def p_funcList1(p):
    '''funcList : funcDecl'''
    p[0] = p[1]

def p_funcList2(p):
    '''funcList : funcList funcDecl'''
    p[0] = p[1] + p[2]

#Variable declaration checked here
def p_varDecl1(p):
    '''varDecl : varDeclList SEMICOLON'''
    p[0] = p[1]

def p_varDeclEmpty(p):
    '''varDecl : empty'''
    p[0] = p[1]

def p_varDeclSt1(p):
    '''varDeclSt : SET ID COMMA factor'''
    p[0] = varDeclaration(p[2], p[4], p.lineno(1))#.returnVariable()

def p_varDeclSt2(p):
    '''varDeclSt : SET ID COMMA arithOperationList'''
    p[0] = varDeclaration(p[2], arithOperation(p[4], p.lineno(1)), p.lineno(1))#.returnVariable

def p_varDeclSt3(p):
    '''varDeclSt : SET ID boolOperation'''
    p[0] = boolOperation(p[2], p[3], p.lineno(1))

def p_varDeclList1(p):
    '''varDeclList : varDeclSt'''
    p[0] = p[1]

def p_varDeclList2(p):
    '''varDeclList : varDeclList SEMICOLON varDeclSt'''
    p[0] = str(p[1]) + p[2] + str(p[3])

#Arithmetic Operation checked here
def p_arithOperList1(p):
    '''arithOperationList : arithOperation'''
    p[0] = p[1]

def p_arithOperList2(p):
    '''arithOperationList : arithOperationList addingOperator factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOperList3(p):
    '''arithOperationList : arithOperationList multiplyingOperator factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOperList4(p):
    '''arithOperationList : arithOperationList MODULE factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOperList5(p):
    '''arithOperationList : arithOperationList EXPONENT factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOper1(p):
    '''arithOperation : factor addingOperator factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOper2(p):
    '''arithOperation : factor multiplyingOperator factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOper3(p):
    '''arithOperation : factor MODULE factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOper4(p):
    '''arithOperation : factor EXPONENT factor'''
    p[0] = p[1] + p[2] + p[3]

def p_arithOper5(p):
    '''arithOperation : MINUS ID'''
    p[0] = p[1] + p[2]

#Boolean operators checked here
def p_boolOper1(p):
    '''boolOperation : NEGATE'''
    p[0] = p[1]

def p_boolOper2(p):
    '''boolOperation : MTRUE'''
    p[0] = p[1]

def p_boolOper3(p):
    '''boolOperation : MFALSE'''
    p[0] = p[1]

#Movement Declaration checked here
def p_moveDecl1(p):
    '''moveDecl : moveDeclList SEMICOLON'''
    p[0] = p[1]

def p_moveDeclEmpty(p):
    '''moveDecl : empty'''
    p[0] = p[1]

def p_moveDeclList1(p):
    '''moveDeclList : moveDeclSt'''
    p[0] = p[1]

def p_moveDeclList2(p):
    '''moveDeclList : moveDeclList SEMICOLON moveDeclSt'''
    p[0] = p[1] + p[2] + p[3]
    
def p_moveDeclSt1(p):
    '''moveDeclSt : ABANICO'''
    p[0] = Abanico(p[1])

def p_moveDeclSt2(p):
    '''moveDeclSt : VERTICAL'''
    p[0] = Vertical(p[1])

def p_moveDeclSt3(p):
    '''moveDeclSt : PERCUTOR'''
    p[0] = Percutor(p[1])

def p_moveDeclSt4(p):
    '''moveDeclSt : GOLPE'''
    p[0] = Golpe(p[1])

def p_moveDeclSt5(p):
    '''moveDeclSt : VIBRATO'''
    p[0] = Vibrato(p[1])

def p_moveDeclSt6(p):
    '''moveDeclSt : METRONOMO'''
    p[0] = Metronomo(p[1])

#Procedure Declarations checked here
def p_procDecl1(p):
    '''procDecl : procDeclList SEMICOLON''' 
    p[0] = p[1]

def p_procDeclEmpty(p):
    '''procDecl : empty'''
    p[0] = p[1]

def p_procDeclList1(p):
    '''procDeclList : procDeclSt'''
    p[0] = str(p[1])

def p_procDeclList2(p):
    '''procDeclList : procDeclList SEMICOLON procDeclSt'''
    p[0] = str(p[1]) + p[2] + str(p[3])

def p_procDeclSt1(p):
    '''procDeclSt : PRINTLN LPARENTHESES toPrint RPARENTHESES'''
    p[0] = toPrint()

def p_procDeclSt4(p):
    '''procDeclSt : EXEC ID LPARENTHESES parameter RPARENTHESES'''
    p[0] = execRutinas(p[2], p[4], p.lineno(1))

#Function declarations checked here
def p_funcDecl1(p):
    '''funcDecl : funcDeclList SEMICOLON'''
    p[0] = p[1]

def p_funcDecl2(p):
    '''funcDecl : empty'''
    p[0] = p[1]

def p_funcDeclList1(p):
    '''funcDeclList : funcDeclSt'''
    p[0] = str(p[1])

def p_funcDeclList2(p):
    '''funcDeclList : funcDeclList SEMICOLON funcDeclSt'''
    p[0] = str(p[1]) + p[2] + str(p[3])

def p_funcDeclSt1(p):
    '''funcDeclSt : DEF ID LPARENTHESES parameter RPARENTHESES LBRACKET blockList RBRACKET'''
    p[0] = defRutinas(p[2], p[4], p[7], p.lineno(1))
 
def p_funcDeclSt2(p):
    '''funcDeclSt : DEF PRINCIPAL LBRACKET blockList RBRACKET'''
    p[0] = defPrincipal(p[4], p.lineno(1))

#Parameters checked here
def p_parameter1(p):
    '''parameter : parameterList'''
    p[0] = p[1]

def p_parameter2(p):
    '''parameter : empty'''
    p[0] = p[1]

def p_parameterList1(p):
    '''parameterList : factor'''
    p[0] = p[1]

def p_parameterList2(p):
    '''parameterList : parameterList COMMA factor'''
    p[0] = p[1] + p[2] + p[3]

#Statement Declaration checked here
def p_statementDecl1(p):
    '''statementDecl : statementList SEMICOLON'''
    p[0] = p[1]

def p_statementDeclEmpty(p):
	'''statementDecl : empty'''
	p[0] = p[1]

def p_statementList1(p):
    '''statementList : statement'''
    p[0] = p[1]

def p_statementList2(p):
	'''statementList : statementList SEMICOLON statement'''
	p[0] = str(p[1]) + p[2] + str(p[3])

def p_statement1(p):
    '''statement : IF condition LBRACKET blockList RBRACKET'''
    p[0] = ifVerifier(p[2], p[4], '', p.lineno(1))

def p_statement2(p):
    '''statement : IF condition LBRACKET blockList RBRACKET ELSE LBRACKET blockList RBRACKET'''
    p[0] = ifVerifier(p[2], p[4], p[8], p.lineno(1))

def p_statement3(p):
    '''statement : FOR ID TO factor STEP NUMBER LBRACKET blockList RBRACKET'''
    p[0] = forVerifier(p[2], p[4], p[6], p[8], p.lineno(1))

def p_statement4(p):
    '''statement : FOR ID TO factor LBRACKET blockList RBRACKET'''
    p[0] = forVerifier(p[2], p[4], '1', p[6], p.lineno(1))

def p_statement5(p):
    '''statement : ENCASO cuandoEntonsList SEMICOLON SINO LBRACKET blockList RBRACKET SEMICOLON FINENCASO'''
    #print('encaso 1')
    p[0] = enCasoVerifier(p[2], p[6], p.lineno(1))

def p_statement6(p):
    '''statement : ENCASO ID cuandoEntonsListAux SEMICOLON SINO LBRACKET blockList RBRACKET SEMICOLON FINENCASO'''
    #print('encaso 2')
    for i in toVerify:
        string = ''
        i = p[2] + i
        i = i.split(',')
        for j in i[1:len(i)]:
            string += j + ','
        p[3] += ifVerifier2(i[0], string, p.lineno(1)) + ";"

    p[0] = enCasoVerifier2(p[3], p[7], p.lineno(1))

#Sentencias condicionales checked here
def p_cuandoEntonsList1(p):
    '''cuandoEntonsList : cuandoEntons'''
    p[0] = p[1]

def p_cuandoEntonsList2(p):
    '''cuandoEntonsList : cuandoEntonsList SEMICOLON cuandoEntons'''
    p[0] = p[1] + p[2] + p[3]

def p_cuandoEntons1(p):
    '''cuandoEntons : CUANDO ID relation factor ENTONS LBRACKET blockList RBRACKET'''
    #print('encaso 3')
    p[0] = ifVerifier((p[2] + p[3] + p[4]), p[7], '', p.lineno(1))

def p_cuandoEntonsAux1(p):
    '''cuandoEntonsAux : CUANDO relation factor ENTONS LBRACKET blockList RBRACKET'''
    #print('encaso 4')
    toVerify.append(p[2] + p[3] + ',' + p[6])
    p[0] = ''

def p_cuandoEntonsListAux1(p):
    '''cuandoEntonsListAux : cuandoEntonsAux'''
    p[0] = p[1]

def p_cuandoEntonsListAux2(p):
    '''cuandoEntonsListAux : cuandoEntonsListAux SEMICOLON cuandoEntonsAux'''
    p[0] = p[1] + p[2] + p[3]

#Conditions checked here
def p_condition1(p):
	'''condition : arithOperation relation arithOperation'''
	p[0] = p[1] + p[2] + p[3]

def p_condition2(p):
	'''condition : arithOperation relation factor'''
	p[0] = p[1] + p[2] + p[3]

def p_condition3(p):
	'''condition : factor relation arithOperation'''
	p[0] = p[1] + p[2] + p[3]

def p_condition4(p):
	'''condition : factor relation factor'''
	p[0] = p[1] + p[2] + p[3]

def p_condition5(p):
    '''condition : factor'''
    p[0] = p[1]

#Prints checked here
def p_toPrint1(p):
    '''toPrint : toPrintList'''
    p[0] = p[1]

def p_toPrintEmpty(p):
    '''toPrint : empty'''
    p[0] = p[1]

def p_toPrintList1(p):
    '''toPrintList : toPrintSt'''
    p[0] = p[1]

def p_toPrintList2(p):
    '''toPrintList : toPrintList COMMA toPrintSt'''
    p[0] = p[1] + p[2] + p[3]

def p_toPrintSt1(p):
    '''toPrintSt : STRING'''
    p[0] = addPrintPar(p[1])

def p_toPrintSt2(p):
    '''toPrintSt : factor'''
    p[0] = addPrintPar2(p[1])

def p_toPrintSt3(p):
    '''toPrintSt : TYPE LPARENTHESES ID RPARENTHESES'''
    p[0] = addPrintPar3(p[3], p.lineno(3))

#Relations checked here
def p_relation1(p):
    '''relation : EQUAL'''
    p[0] = p[1]

def p_relation2(p):
    '''relation : NEQUAL'''
    p[0] = p[1]

def p_relation3(p):
    '''relation : LT'''
    p[0] = p[1]

def p_relation4(p):
    '''relation : GT'''
    p[0] = p[1]

def p_relation5(p):
    '''relation : LTE'''
    p[0] = p[1]

def p_relation6(p):
    '''relation : GTE'''
    p[0] = p[1]

#Arithmetic Operators checked here
def p_addingOperator1(p):
    '''addingOperator : PLUS'''
    p[0] = p[1]

def p_addingOperator2(p):
    '''addingOperator : MINUS'''
    p[0] = p[1]

def p_multiplyingOperator1(p):
    '''multiplyingOperator : TIMES'''
    p[0] = p[1]

def p_multiplyingOperator2(p):
    '''multiplyingOperator : DIVIDE'''
    p[0] = p[1]

def p_multiplyingOperator3(p):
    '''multiplyingOperator : WDIVIDE'''
    p[0] = p[1]

#Factors checked here
def p_factor1(p):
    '''factor : ID'''
    p[0] = p[1]

def p_factor2(p):
    '''factor : NUMBER'''
    p[0] = str(p[1])

def p_factor3(p):
    '''factor : LPARENTHESES arithOperation RPARENTHESES'''
    p[0] = p[1] + p[2] + p[3]

def p_factor4(p):
    '''factor : BOOL'''
    p[0] = p[1]

#Empty
def p_empty(p):
	'''empty :'''
	pass

#Error checker
def p_error(p):
	errorList.append(["Error de sintaxis " + str(p.value), p.lexer.lineno])#p.lineno(1)])    

def buscarFicheros(directorio):
	ficheros = []
	numArchivo = ''
	respuesta = False
	cont = 1

	for base, dirs, files in os.walk(directorio):
		ficheros.append(files)

	for file in files:
		print (str(cont)+". "+file)
		cont = cont+1

	while respuesta == False:
		numArchivo = raw_input('\nNumero del test: ')
		for file in files:
			if file == files[int(numArchivo)-1]:
				respuesta = True
				break

	print ("Has escogido \"%s\" \n" %files[int(numArchivo)-1])

	return files[int(numArchivo)-1]

def run():
    directorio = '/home/david/Documents/GitHub/Tambarduine/'
    archivo = 'temp.pl0'
    test = directorio+archivo
    fp = codecs.open(test,"r","utf-8")
    cadena = fp.read()
    fp.close()

    parser = yacc()
    result = parser.parse(cadena)

    print (result)

#run()
'''
const COLORS = {
  SEND: 'red',   
  CONSTANT: 'blue',  
  CALL: 'orange', 
  INTERNAL: 'gray', 
  VIEW: 'yellow',  
  PURE: 'green', 
  TRANSFER: 'purple', 
  PAYABLE: 'brown'  
}
'''

import jsonpath
import json
from solidity_parser import parser
import pprint
from graphviz import Digraph

def parserTojson(sourceUnit):
    x = str(sourceUnit)
    x = x.replace("\'", "\"")
    x = x.replace("True,", "true,")
    x = x.replace("False,", "false,")
    x = x.replace("True}", "true}")
    x = x.replace("False}", "false}")
    x = x.replace("None", "0")
    return x

def getJsonValue(json_data,keyName):
    keyValue = jsonpath.jsonpath(json_data, '$..{keyName}'.format(keyName=keyName))
    return keyValue

def checkAttr(node,attr):
    if getJsonValue(json.loads(parserTojson(node)),"memberName") == False:
        return False
    else: 
        return attr in getJsonValue(json.loads(parserTojson(node)),"memberName")


def testOutput(fileLocation):
    sourceUnit = parser.parse_file(fileLocation, loc=False) # loc=True -> add location information to ast nodes
    sourceUnitObject = parser.objectify(sourceUnit)
    for contract in sourceUnitObject.contracts:
        print("------------------------%s----------------------------"%contract)
        functionName = sourceUnitObject.contracts[contract].functions
        print('%-30s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s' %("funName","visibility","stateMutability","isConstructor","isFallback","isReceive","isSend","isCall","isTransfer"))
        for fun in functionName:
            fff = sourceUnitObject.contracts[contract].functions[fun]
            node = fff._node.body
            print('%-30s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s' %(fun,fff.visibility,fff.stateMutability,str(fff.isConstructor),str(fff.isFallback),str(fff.isReceive),str(checkAttr(node,"send")),str(checkAttr(node,"call")),str(checkAttr(node,"transfer"))))


def build(fileLocation):
    ddd = {}
    sourceUnit = parser.parse_file(fileLocation, loc=False) # loc=True -> add location information to ast nodes
    sourceUnitObject = parser.objectify(sourceUnit)
    for contract in sourceUnitObject.contracts:
        ddd[contract]={}
        print("------------------------%s----------------------------"%contract)
        functionName = sourceUnitObject.contracts[contract].functions
        print('%-30s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s' %("funName","visibility","stateMutability","isConstructor","isFallback","isReceive","isSend","isCall","isTransfer"))
        for fun in functionName:
            fff = sourceUnitObject.contracts[contract].functions[fun]
            node = fff._node.body
            print('%-30s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s' %(fun,fff.visibility,fff.stateMutability,str(fff.isConstructor),str(fff.isFallback),str(fff.isReceive),str(checkAttr(node,"send")),str(checkAttr(node,"call")),str(checkAttr(node,"transfer"))))
            ddd[contract][fun] = (fff.visibility,fff.stateMutability,str(fff.isConstructor),str(fff.isFallback),str(fff.isReceive),str(checkAttr(node,"send")),str(checkAttr(node,"call")),str(checkAttr(node,"transfer")))
    return ddd

COLORS = {
  "send": 'red',    # 3
  "constant": 'blue',  # 2 
  "call": 'orange',  # 3
  "internal": 'gray',  # 1
  "view": 'yellow',  # 2
  "pure": 'green',  # 2
  "transfer": 'purple',  # 3 
  "payable": 'brown',  # 2
}

# 优先判断visibility,其次stateMutability,其次

def colorSelect(fun):
    if fun[0]=="internal":
        return COLORS["internal"]
    elif fun[1]=="constant":
        return COLORS["constant"]
    elif fun[1]=="view":
        return COLORS["view"]
    elif fun[1]=="pure":
        return COLORS["pure"]   
    elif fun[1]=="payable":
        return COLORS["payable"]
    elif fun[5]=='True':
        return COLORS["send"]
    elif fun[6]=='True':
        return COLORS["call"]
    elif fun[7]=='True':
        return COLORS["transfer"]

builded = build("./test/in/issue13.sol")
pprint.pprint(builded)

dot = Digraph()


for contract in builded:
    for bb in builded[contract]:
        dot.node(bb,color=colorSelect(builded[contract][bb]))
        if builded[contract][bb][0] == "internal":
            dot.edge(contract,bb)
        if builded[contract][bb][5] == 'True':
            dot.node("UNTRUSTED",shape='box')
            dot.edge(bb,"UNTRUSTED")
        if builded[contract][bb][7] == 'True':
            dot.node("TRANSFER")
            dot.edge(bb,"TRANSFER")
    print(dot)


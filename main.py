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

def parserTojson(sourceUnit):
    return json.dumps(sourceUnit)

def getJsonValue(json_data,keyName):
    keyValue = jsonpath.jsonpath(json_data, '$..{keyName}'.format(keyName=keyName))
    return keyValue

def checkAttr(node,attr):
    if getJsonValue(json.loads(parserTojson(node)),"memberName") == False:
        return False
    else: 
        return attr in getJsonValue(json.loads(parserTojson(node)),"memberName")

def checkEventCall(node):
    if getJsonValue(json.loads(parserTojson(node)),"eventCall"):
        return True,getJsonValue(json.loads(parserTojson(node)),"eventCall")[0]["expression"]["name"]
    return False,None

def build(fileLocation):
    ddd = {}
    sourceUnit = parser.parse_file(fileLocation, loc=False) # loc=True -> add location information to ast nodes
    sourceUnitObject = parser.objectify(sourceUnit)
    
    for contract in sourceUnitObject.contracts:
        ddd[contract]={}
        # print("------------------------%s----------------------------"%contract)
        functionName = sourceUnitObject.contracts[contract].functions
        # print('%-30s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s' %("funName","visibility","stateMutability","isConstructor","isFallback","isReceive","isSend","isCall","isTransfer","isEmitEvent","eventName"))
        for fun in functionName:
            fff = sourceUnitObject.contracts[contract].functions[fun]
            node = fff._node.body
            isEmitEvent,eventName=checkEventCall(node)
            # print('%-30s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s' %(fun,fff.visibility,fff.stateMutability,str(fff.isConstructor),str(fff.isFallback),str(fff.isReceive),str(checkAttr(node,"send")),str(checkAttr(node,"call")),str(checkAttr(node,"transfer")),str(isEmitEvent),eventName))
            ddd[contract][fun] = (fff.visibility,fff.stateMutability,str(fff.isConstructor),str(fff.isFallback),str(fff.isReceive),str(checkAttr(node,"send")),str(checkAttr(node,"call")),str(checkAttr(node,"transfer")),str(isEmitEvent),eventName)
    return ddd

def colorSelect(fun): # 优先判断visibility,其次stateMutability,其次
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

def generateDot(builded):

    # pprint.pprint(builded)

    dotparent = Digraph(name="parent")

    for contract in builded:
        dot = Digraph(name="cluster_%s"%contract) 
        dot.graph_attr.update(label=contract)
        dotSon1=Digraph(name="cluster_%s_internal"%contract)
        dotSon2=Digraph(name="cluster_%s_public"%contract)
        dotSon3=Digraph(name="cluster_%s_external"%contract)
        dotSon4=Digraph(name="cluster_%s_default"%contract)
        dotSon1.graph_attr.update(label="internal")
        dotSon2.graph_attr.update(label="public")
        dotSon3.graph_attr.update(label="external") 
        dotSon4.graph_attr.update(label="default") 
        for bb in builded[contract]:
            if builded[contract][bb][0] == "internal":
                dotSon1.edge(contract,bb)
                if builded[contract][bb][5] == 'True':
                    dotSon1.node("UNTRUSTED",shape='box')
                    dotSon1.edge(bb,"UNTRUSTED")
                if builded[contract][bb][7] == 'True':
                    dotSon1.node("TRANSFER")
                    dotSon1.edge(bb,"TRANSFER")
                if builded[contract][bb][8] == 'True':
                    dotSon1.node(builded[contract][bb][9],shape="ellipse")
                    dotSon1.edge(bb,builded[contract][bb][9])
            elif builded[contract][bb][0] == "public":
                dotSon2.node(bb,color=colorSelect(builded[contract][bb]))
                if builded[contract][bb][5] == 'True':
                    dotSon2.node("UNTRUSTED",shape='box')
                    dotSon2.edge(bb,"UNTRUSTED")
                if builded[contract][bb][7] == 'True':
                    dotSon2.node("TRANSFER")
                    dotSon2.edge(bb,"TRANSFER")
                if builded[contract][bb][8] == 'True':
                    dotSon2.node(builded[contract][bb][9],shape='egg')
                    dotSon2.edge(bb,builded[contract][bb][9])
            elif builded[contract][bb][0] == "external":
                dotSon3.node(bb,color=colorSelect(builded[contract][bb]))
                if builded[contract][bb][5] == 'True':
                    dotSon3.node("UNTRUSTED",shape='box')
                    dotSon3.edge(bb,"UNTRUSTED")
                if builded[contract][bb][7] == 'True':
                    dotSon3.node("TRANSFER")
                    dotSon3.edge(bb,"TRANSFER")
                if builded[contract][bb][8] == 'True':
                    dotSon3.node(builded[contract][bb][9],shape='egg')
                    dotSon3.edge(bb,builded[contract][bb][9])
            elif builded[contract][bb][0] == "default":
                dotSon4.node(bb,color=colorSelect(builded[contract][bb]))
                if builded[contract][bb][5] == 'True':
                    dotSon4.node("UNTRUSTED",shape='box')
                    dotSon4.edge(bb,"UNTRUSTED")
                if builded[contract][bb][7] == 'True':
                    dotSon4.node("TRANSFER")
                    dotSon4.edge(bb,"TRANSFER")
                if builded[contract][bb][8] == 'True':
                    dotSon4.node(builded[contract][bb][9],shape='egg')
                    dotSon4.edge(bb,builded[contract][bb][9])
        dot.subgraph(dotSon1)
        dot.subgraph(dotSon2)
        dot.subgraph(dotSon3)
        dot.subgraph(dotSon4)
        dotparent.subgraph(dot)

    print(dotparent)
    return dotparent

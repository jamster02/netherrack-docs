import pprint
import requests
import base64
import json
import gzip

res = requests.get("https://raw.githubusercontent.com/EnjoyYourBan/enjoyyourban.github.io/master/actions.json")
actions = res.json()

class Target:
    def __init__(self, line):
        self.line = line
    
    def target(self, playerTarget):
        self.line.code['blocks'][-1]['target'] = playerTarget

class Not:
    def __init__(self, line):
        self.line = line
    
    def _not(self):
        self.line.code['blocks'][-1]['inverted'] = "NOT"

class Close:
    def __init__(self, line):
        self.line = line
    
    def _else(self):
        self.line.code['blocks'].append({"id":"block","block":"else"})
        self.line.code['blocks'].append({"id":"bracket","direct":"open","type":"norm"})

class Variable:
    def __init__(self, name, varType="unsaved"):
        self.name = name
        self.varType = varType
    
    def compile(self):
        return {"item":{"id":"var","data":{"name":self.name,"scope": self.varType}}, "slot":0}

class Text:
    def __init__(self, value):
        self.value = value.replace("&", "§")
    
    def compile(self):
        return {"item": {"id": "txt", "data": {"name": self.value}}, "slot": 0}

class Num:
    def __init__(self, value):
        self.value = value
    
    def compile(self):
        return {"item": {"id": "num", "data": {"name": self.value}}, "slot": 0}

class Location:
    def __init__(self, x, y=0, z=0, pitch=0, yaw=0):
        self.x, self.y, self.z, self.pitch, self.yaw = x, y, z, pitch, yaw
    
    def compile(self):
        return {"item": {"id": "loc", "data": {"loc": {
            "x": self.x, "y": self.y, "z": self.z, "pitch": self.pitch, "yaw": self.yaw
        }, "isBlock": False}}, "slot": 0}

class GameValue:
    def __init__(self, value, valTarget="Default"):
        self.value = value
        self._target = valTarget
    
    def target(self, valTarget="Default"):
        self._target = valTarget
    
    def compile(self):
        return {"item":{"id":"g_val","data":{"type": self.value,"target": self._target}},"slot":0}

class Particle:
    def __init__(self, particle):
        self.particle = particle
    
    def compile(self):
        return {"item":{"id":"part","data":{"particle":self.particle,"count":1,"speed":0,"dx":0,"dy":0,"dz":0}},"slot":0}

class Potion:
    def __init__(self, effect, length, amplifier=1):
        self.effect, self.length, self.amplifier = effect, length, amplifier
    
    def compile(self):
        return {"item":{"id":"pot","data":{"pot":self.effect,"dur":self.length,"amp":self.amplifier}},"slot":0}

class Sound:
    def __init__(self, noise, pitch=1, vol=1):
        self.noise, self.pitch, self.vol = noise, pitch, vol
    
    def compile(self):
        return {"item":{"id":"snd","data":{"sound": self.noise,"pitch": self.pitch,"vol": self.vol}},"slot":0}

class Line:
    def __init__(self, eventType, eventName):
        if eventType not in ("func", "process"):
            self.code = {"blocks": [
                {"block": eventType, "id": "block", "args": {"items": []}, "action": eventName}
            ]}
        else:
            self.code = {"blocks":[{"id":"block","block":eventType,"args":{"items":[{"item":{"id":"bl_tag","data":{"option":"False","tag":"Is Hidden","action":"dynamic","block":eventType}},"slot":26}]},"data":eventName}]}
        
        self.target = "None"
        self.brackets = []
    
    def makeAction(self, block, action, subaction, *items):
        try:
            tags = actions[action]['tags']
        except:
            tags = []

        formatted = []

        index = 0

        for item in items:
            if type(item) == str:
                item = Text(item)
            elif type(item) == int:
                item = Num(item)

            item = item.compile()
            item['slot'] = index
            formatted.append(item)

            index += 1
        
        index = 26

        for tag in tags:
            if tag['name'] == "Delay Unit":
                tag['name'] = "Time Unit"

            tagData = {"item": {
                "id": "bl_tag", "data": {"tag": tag['name'], "option": tag['defaultOption'], 
                "action": action, "block": block}},
                "slot": index
            }
            if subaction:
                tagData['subaction'] = subaction

            formatted.append(tagData)

            index -= 1
        
        codeData = {"block": block, "id": "block", "args": {
            "items": formatted
        }, "action": action}
        if subaction:
            codeData['subaction'] = subaction

        self.code['blocks'].append(codeData)

        return Target(self)
    
    def callFunc(self, function):
        self.code['blocks'].append({"id":"block","block":"call_func","args":{"items":[]},"data":function})
    
    def callProc(self, process):
        self.code['blocks'].append({"id":"block","block":"start_process","args":{"items":[{"item":{"id":"bl_tag","data":{"option":"Create new storage","tag":"Local Variables","action":"dynamic","block":"start_process"}},"slot":25},{"item":{"id":"bl_tag","data":{"option":"With current targets","tag":"Target Mode","action":"dynamic","block":"start_process"}},"slot":26}]},"data":process})

    def control(self, action, *items):
        return self.makeAction("control", action, None, *items)
    
    def selectObj(self, action, subaction=None, *items):
        return self.makeAction("select_obj", action, subaction, *items)

    def entityAction(self, action, *items):
        return self.makeAction("entity_action", action, None, *items)

    def gameAction(self, action, *items):
        return self.makeAction("game_action", action, None, *items)
    
    def playerAction(self, action, *items):
        return self.makeAction("player_action", action, None, *items)
    
    def setVar(self, action, *items):
        return self.makeAction("set_var", action, None, *items)
    
    ## IFs
    def close(self):
        if self.brackets != []:
            if self.brackets[-1] == 'normal':
                bType = 'norm'
            else:
                bType = 'repeat'

            self.code['blocks'].append({"id":"bracket","type":bType,"direct":"close"})
            self.brackets.pop(-1)
        else:
            raise Exception("no bracket to close")

        return Close(self)
    
    def ifEntity(self, action, *items):
        self.makeAction("if_entity", action, None, *items)
        
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)
    
    def ifGame(self, action, *items):
        self.makeAction("if_game", action, None, *items)
        
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)

    def ifPlayer(self, action, *items):
        self.makeAction("if_player", action, None, *items)
        
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)

    def ifVar(self, action, *items):
        self.makeAction("if_var", action, None, *items)
        
        self.code['blocks'].append({"id":"bracket","type":"norm","direct":"open"})
        self.brackets.append("normal")

        return Not(self)
    
    def repeat(self, action, *items):
        self.makeAction("repeat", action, None, *items)
        
        self.code['blocks'].append({"id":"bracket","type":"repeat","direct":"open"})
        self.brackets.append("special")
    
    def build(self):
        if self.brackets != []:
            raise Exception("grr u didnt close the brackets")

        jsonCode = json.dumps(self.code)

        g = gzip.compress(bytes(jsonCode, 'utf-8'))

        encryptCode = base64.b64encode(g)
        encryptCode = str(encryptCode, 'utf-8')
        
        commandCode = '''
        /give @p minecraft:ender_chest{PublicBukkitValues:{"hypercube:codetemplatedata":'{"author":"Netherrack","name":"Netherrack Template","version":1,"code":"'''+encryptCode+'''"}'},display:{Name:'{"text":"Netherrack Template"}'}}
        '''

        return commandCode, jsonCode, encryptCode
'''
doorlock control via HA
entered 11/10/25
return lock state

'''

Version = 'haDoorCtr3.py 31/10/25'

from synapse.platforms import *
from synapse.hexSupport import *
from synapse.switchboard import *

Mains1 = '\x4C\x6B\x61'  # hexadecimal unique address of node
parent = '\x00\x00\x01'  

RedLed = GPIO_37
GreenLed = GPIO_36
testMsg = 'test message'


def init():
    global wait, cycleCount, go, message, sndMsg, memory,checkMsg,passwCheck,sendComd,lockState, term
    wait = False
    sndMsg = False
    sendComd = False
    checkMsg = False
    passwCheck = False
    setPinDir(RedLed,True)
    writePin(RedLed,False)
    setPinDir(GreenLed,True)
    writePin(GreenLed,False)
    lockState =0
    cycleCount = 0
    memory = 0
    term = '\x1A '
    message = 'LOCKED '
    
    saveNvParam(20,0)  # node is stationary
    initUart(0, 9600)  
    stdinMode(0, False)   # line mode, no echo
    #ucastSerial("\x00\x00\x01")
    crossConnect(DS_UART0, DS_STDIO)  # cross connect serial to uart 0
    #crossConnect(DS_STDIO,DS_TRANSPARENT)
    seq =0
    # looking for balance
 
def sendMessage():
    # crossConnect(DS_STDIO,DS_TRANSPARENT)
    #s is a counter to send a second terminator charactor
    global s, sndMsg,cycleCount
    s=0
    cycleCount =0
    sndMsg = True  
     
@setHook(HOOK_STARTUP)
def startupEvent():
    init() 
    
@setHook(HOOK_100MS)
def tick():
#  command sent when requested every 2s
    global cycleCount
    global state,lastLockState,sndMsg,sendComd,message,term
    global go
    cycleCount = cycleCount +1
    if cycleCount % 10==0: 
       pulsePin(RedLed,20,True) 
       #print "*"
       if sndMsg :
            print message,term
            sndMsg = False
            


@setHook(HOOK_STDIN)
def stdinEvent(buf):
    """Receive handler for character input on UART0.
       The parameter 'buf' will contain one or more received characters. 
       with a command then a several more characters inserted.
    """
    global state
    state = buf  # buf from the GMS module when a command is correct it transmits /r/nOK
    #rpc(Mains1,'showModemResponse',buf)
    #pulsePin(GreenLed,50,True)
    #print buf
    procTokens(state)    
       
       
def procTokens(s):
    buf = s
    # rpc(Mains1,'showModemResponse',buf)
    global checkMsg,passwCheck,message,bal,cb,LockState,devControl,sndMsg
   
    # devControl is a further item to control other things
    
    if searchForToken(buf,'OK',False) :
        pulsePin(GreenLed,50,True)
    
    if searchForToken(buf,'xxxxxx',False):   # only responds to this number  your code 1
        checkMsg = True
        passwCheck = False
        pulsePin(GreenLed,20,True)
        # rpc(Mains1,'showModemResponse',buf)
    if checkMsg and searchForToken(buf,'y.yyy',False): # password  your code 2
        checkMsg = False
        passwCheck = True
        pulsePin(GreenLed,20,True)
        pulsePin(GreenLed,200,False)
        pulsePin(GreenLed,20,True)
        
    if passwCheck:
        #pulsePin(RedLed,20,True)
        if searchForToken(buf,'lock',False) :
            doorControl(True)
            LockState = True
            pulsePin(RedLed,20,True)
            passwCheck = False
            message = 'LOCKED'
            sndMsg = True
        if searchForToken(buf,'unlock',False) :
            doorControl(False)
            LockState = False
            pulsePin(GreenLed,20,True)
            message = 'UNLOCKED'
            sndMsg = True
            passwCheck = False
        if searchForToken(buf,'state',False) :
	    if LockState:
	        message = 'LOCKED'
	    else:
	        message = 'UNLOCKED'
	      
	    pulsePin(GreenLed,20,True)
	    sndMsg = True
            passwCheck = False
        i= 8000  # give it time for the lock status to be updated in Mains1 and ch
        #pulsePin(RedLed,20,True)
        while i > 0:
            i-= 1
        #ulsePin(RedLed,20,True)
        # ls = rpc(Mains1,'getLockState')  # get lock state  returns incorrect state
        
        
        
        
    if searchForToken(buf,'ERROR',False):
        rpc(Mains1,'showModemResponse',buf)
        
    
        
    
   

def searchForToken(test,tok,c):
    # looks for tok  in test
    # if c is true it extracts the control token
    global devControl
    n= len(tok)
    m=len(test)
    find = False
    i=0
    while(i < m and not find):
        if test[i:i+n] == tok :
           find = True
           if c:
               devControl = test[i+n:i+n+5]  # this should extract lock parameter
               #rpc(Mains1,'showModemResponse',devControl) ####
        i +=1
    return find

def doorControl(doorState):
    global code
    #if LS is true then lock the door 
    # simple 256 bit encryption
    start = 1 + (random() & 0x00ff)
    code = start
    b=1
    b=sequence(b)
    if doorState:
        rpc (Mains1,'remoteLock', (start-1),code & 0x00ff,True)   # lock control node
    else:
        rpc (Mains1,'remoteLock', (start-1),code & 0x00ff,False)
        
def sequence (bit):
    global code
    code = code << 1
    code = code | bit
    b =1
    b = ((code & 0x40) >> 6) ^ b
    b = ((code & 0x20) >> 5) ^ b
    b = ((code & 0x10) >> 4) ^ b
    b = ((code & 0x08) >> 3) ^ b
    return b
    


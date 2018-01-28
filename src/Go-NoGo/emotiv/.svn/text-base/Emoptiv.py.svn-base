import emotiv
import sys
import EdfWriter as EW
import time
import threading
import SocketServer
import socket
import cPickle as pickle
import gzip


thismodule = sys.modules[__name__]

for v in dir(emotiv):
    if v.startswith('ED'):
        thismodule.__setattr__(v, emotiv.__getattribute__(v))
    if v.startswith('EXP'):
        thismodule.__setattr__(v, emotiv.__getattribute__(v))

thismodule.__setattr__('NCHANNELS', emotiv.NCHANNELS)

edf_channels = [dict() for x in range(emotiv.NCHANNELS)]

edf_channels[0]['label'] = 'COUNTER'
edf_channels[1]['label'] = 'INTERPOLATED'
edf_channels[2]['label'] = 'RAW_CQ'
edf_channels[3]['label'] = 'AF3'
edf_channels[4]['label'] = 'F7'
edf_channels[5]['label'] = 'F3'
edf_channels[6]['label'] = 'FC5'
edf_channels[7]['label'] = 'T7'
edf_channels[8]['label'] = 'P7'
edf_channels[9]['label'] = 'O1'
edf_channels[10]['label'] = 'O2'
edf_channels[11]['label'] = 'P8'
edf_channels[12]['label'] = 'T8'
edf_channels[13]['label'] = 'FC6'
edf_channels[14]['label'] = 'F4'
edf_channels[15]['label'] = 'F8'
edf_channels[16]['label'] = 'AF4'
edf_channels[17]['label'] = 'GYROX'
edf_channels[18]['label'] = 'GYROY'
edf_channels[19]['label'] = 'TIMESTAMP'
edf_channels[20]['label'] = 'ES_TIMESTAMP'
edf_channels[21]['label'] = 'FUNC_ID'
edf_channels[22]['label'] = 'FUNC_VALUE'
edf_channels[23]['label'] = 'MARKER'
edf_channels[24]['label'] = 'SYNC_SIGNAL'

for i in range(emotiv.NCHANNELS):
    edf_channels[i]['sample_rate'] = 128
    edf_channels[i]['dimension'] = ''
    edf_channels[i]['physical_max'] = 16000
    edf_channels[i]['physical_min'] = 0
    edf_channels[i]['digital_max'] = 16000
    edf_channels[i]['digital_min'] = 0

for i in range(emotiv.ED_AF3, emotiv.ED_AF4):
    edf_channels[i]['dimension'] = 'mV'
    edf_channels[i]['physical_max'] = 31200


class EmotivCommandHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        sale = False
        self.request.settimeout(2.0)
        while not sale and not self.server.emotiv.exiting:
            try:
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(1024).strip()
                print "{} wrote:".format(self.client_address[0]), self.data
                strings = self.data.split(' ')
                result = False
                if strings[0] == "MARK":
                    uid = int(strings[1])
                    value = int(strings[2])
                    ret = self.server.emotiv.mark(uid, value)
                    if ret == emotiv.EDK_OK:
                        result = True
                elif strings[0] == "REC":
                    fname = strings[1];
                    result = self.server.emotiv.setEdfOutput(fname)
                    if result == True:
                        result = self.server.emotiv.startWriting()
                elif strings[0] == "STOP":
                    result = self.server.emotiv.stopWriting()
                else:
                    print "Unknown command", strings[0]

                print "Command executed"
                # just send back the same data, but upper-cased
                if result:
                    self.request.sendall(" " + str(emotiv.EDK_OK))
                else:
                    self.request.sendall("-1")
                print "Replied"
            except socket.timeout:
                sale = False
            except Exception as inst:
                print "Algo se bardeo"
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to printed directly
                sale = True


class EmotivCommandServer(SocketServer.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, emotiv):
        SocketServer.ThreadingTCPServer.__init__(self,server_address,RequestHandlerClass)
        self.emotiv = emotiv



class Emotiv:
    def __init__(self, debug, listen=False, h=0,p=0):
        global edf_channels
        self.debug = debug
        self.eEvent = emotiv.EE_EmoEngineEventCreate()
        self.eState = emotiv.EE_EmoStateCreate()
        self.users = []
        self.channels = [x for x in range(emotiv.NCHANNELS)]
        self.data = [[] for x in self.channels]
        self.connected = False
        self.setted = False
        self.started = False
        self.hData = None
        self.readyFunction = None
        self.readyFunctionLock = threading.Lock()
        self.channelsLock = threading.Lock()
        self.stopflag = False
        self.stopLock = threading.Lock()
        self.reader = None
        self.edfName = None
        self.edfWriter = None
        self.writing = False
        self.exiting = False
        self.writeLock = threading.Lock()
        self.callbacks = dict()
        self.callbacks['blink'] = None
        self.callbacks['lwink'] = None
        self.callbacks['rwink'] = None
        self.callbacks['eyebrow'] = None
        self.callbacks['furrow'] = None
        self.callbacks['clench'] = None
        self.callbacks['smile'] = None
        self.callbacks['laugh'] = None
        self.callbacks['lsmirk'] = None
        self.callbacks['rsmirk'] = None
        self.pickle_name = None
        self.pickle_file = None

        if listen:
            SocketServer.ThreadingTCPServer.allow_reuse_address = True
            self.server = EmotivCommandServer((h, p), EmotivCommandHandler, self)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            # Exit the server thread when the main thread terminates
            self.server_thread.daemon = True
            self.server_thread.start()


    def connect(self):
        if self.debug:
            print("Connecting..."),
            sys.stdout.flush()
        res = emotiv.EE_EngineConnect()
        if res == emotiv.EDK_OK:
            if self.debug:
                print("Ok!\n")
                sys.stdout.flush()
            self.connected = True
        else:
            if self.debug:
                print "Error: ", res
        return res

    def setup(self):
        if not self.connected:
            print "Emotiv Engine not connected"
            sys.stdout.flush()
            return False
        if self.debug:
            print "Getting users and sampling rate... ",
            sys.stdout.flush()
        stop = False
        while stop == False:
            state = emotiv.EE_EngineGetNextEvent(self.eEvent)
            if (state == emotiv.EDK_OK):
                eventType = emotiv.EE_EmoEngineEventGetType(self.eEvent)
                (result, userID) = emotiv.EE_EmoEngineEventGetUserId(self.eEvent)
                if not userID in self.users:
                    self.users.append(userID)
                print userID, result
                if (eventType == emotiv.EE_UserAdded):
                    if self.debug:
                        print "got User Id... ", userID,
                        sys.stdout.flush()
                    (result, self.samplingRate) = emotiv.EE_DataGetSamplingRate(userID)

                    if result != emotiv.EDK_OK:
                        print "Cannot retrieve sampling rate."
                        sys.stdout.flush()
                    else:
                        if self.debug:
                            print "got sampling rate... ", self.samplingRate,
                            sys.stdout.flush()
                        stop = True
            time.sleep(1)
        if self.debug:
            print "Ok!"
            sys.stdout.flush()
        self.hData = emotiv.EE_DataCreate()
        self.setted = True;
        return True

    def setBufferSizeInSecs(self, size):
        return emotiv.EE_DataSetBufferSizeInSec(size)

    def disconnect(self):
        self.exiting = True
        emotiv.EE_EngineDisconnect()

    def setChannelsFilter(self, channels):
        self.channelsLock.acquire()
        self.writeLock.acquire()
        if self.writing:
            print "Cannot change channels while writting"
            self.writeLock.release()
            self.channelsLock.release()
            return False

        self.channels = channels
        self.data = [[] for x in self.channels];

        self.writeLock.release()
        self.channelsLock.release()
        return True

    def setReadyFunction(self, function):
        self.readyFunctionLock.acquire()
        self.readyFunction = function
        self.readyFunctionLock.release()

    def getUsers(self):
        return self.users

    def enableForUser(self, userId):
        emotiv.EE_DataAcquisitionEnable(userId,True);

    def __acquire(self):
        self.stopLock.acquire()
        self.stopflag = False
        while self.stopflag == False:
            self.stopLock.release()
            emotiv.EE_DataUpdateHandle(0, self.hData);
            (result, nSamplesTaken) = emotiv.EE_DataGetNumberOfSample(self.hData)
            if nSamplesTaken != 0:
                self.channelsLock.acquire()
                self.writeLock.acquire()
                for i, val in enumerate(self.channels):
                    (result, self.data[i]) = emotiv.EE_DataGet(self.hData, val, nSamplesTaken)
                    if self.writing:
                        for sample in range(nSamplesTaken):
                            self.edfWriter.write_sample(val, self.data[i][sample])
                # Guardar datos en pickle
                if self.writing:
                    pickle.dump(self.data, self.pickle_file, pickle.HIGHEST_PROTOCOL)
                self.writeLock.release()
                self.channelsLock.release()
                self.readyFunctionLock.acquire()
                if self.readyFunction != None:
                    self.readyFunction(self.data)
                self.readyFunctionLock.release()
            time.sleep(0.1)
            state = emotiv.EE_EngineGetNextEvent(self.eEvent)
            if state == emotiv.EDK_OK:
                eventType = emotiv.EE_EmoEngineEventGetType(self.eEvent);
                if eventType == emotiv.EE_EmoStateUpdated:
                    emotiv.EE_EmoEngineEventGetEmoState(self.eEvent, self.eState);
                    self._processExpressivEvent()
            self.stopLock.acquire()

        self.started = False;
        self.stopLock.release()
        print "Finishing acquire"


    def _processExpressivEvent(self):
        if emotiv.ES_ExpressivIsBlink(self.eState) and self.callbacks['blink'] != None:
            self.callbacks['blink']()
        if emotiv.ES_ExpressivIsLeftWink(self.eState) and self.callbacks['lwink'] != None:
            self.callbacks['lwink']()
        if emotiv.ES_ExpressivIsRightWink(self.eState) and self.callbacks['rwink'] != None:
            self.callbacks['rwink']()
        upower = emotiv.ES_ExpressivGetUpperFaceActionPower(self.eState)
        if upower > 0.0:
            upperFaceType = emotiv.ES_ExpressivGetUpperFaceAction(self.eState)
            if upperFaceType == emotiv.EXP_EYEBROW and self.callbacks['eyebrow'] != None:
                self.callbacks['eyebrow'](upower)
            if upperFaceType == emotiv.EXP_FURROW and self.callbacks['furrow'] != None:
                self.callbacks['furrow'](upower)
        lpower = emotiv.ES_ExpressivGetLowerFaceActionPower(self.eState)
        if lpower > 0.0:
            upperFaceType = emotiv.ES_ExpressivGetLowerFaceAction(self.eState)
            if upperFaceType == emotiv.EXP_CLENCH and self.callbacks['clench'] != None:
                self.callbacks['clench'](lpower)
            if upperFaceType == emotiv.EXP_SMILE and self.callbacks['smile'] != None:
                self.callbacks['smile'](lpower)
            if upperFaceType == emotiv.EXP_LAUGH and self.callbacks['laugh'] != None:
                self.callbacks['laugh'](lpower)
            if upperFaceType == emotiv.EXP_SMIRK_LEFT and self.callbacks['lsmirk'] != None:
                self.callbacks['lsmirk'](lpower)
            if upperFaceType == emotiv.EXP_SMIRK_RIGHT and self.callbacks['rsmirk'] != None:
                self.callbacks['rsmirk'](lpower)


    def start(self):
        if not self.setted:
            print "Emotiv not setted up"
            sys.stdout.flush()
            return False
        self.stopLock.acquire()
        if self.started:
            print "Emotiv already started"
            sys.stdout.flush()
            return False
        self.started = True
        self.stopLock.release()
        self.reader = threading.Thread(target=self.__acquire)
        self.reader.daemon = True
        self.reader.start()
        return True


    def addExpressivCallback(self, event, callbackFunc):
        self.callbacks[event] = callbackFunc


    def stop(self):
        if self.debug:
            print "Trying to stop"
        self.writeLock.acquire()
        if self.edfWriter != None and self.writing == True:
            self.edfWriter.close()
        if self.pickle_file is not None and not self.pickle_file.closed:
            self.pickle_file.close()
        self.writeLock.release()
        self.stopLock.acquire()
        if self.debug:
            print "Stopping"
        self.stopflag = True
        self.stopLock.release()

    def mark(self, userid, value):
        if self.debug:
            print "Mark to user", userid, "value", value
        result = emotiv.EE_DataSetMarker(userid, value)
        return result


    def setEdfOutput(self, filename):
        self.writeLock.acquire()
        if self.writing == True:
            return False
        self.edfName = filename + '.edf';
        self.pickle_name = filename + '.pklz'
        self.writeLock.release()
        return True

    def startWriting(self):
        if (self.edfName == None):
            print "Cannot write, edf file name not set"
            return False
        else:
            if self.debug:
                print "Writing to", self.edfName
            self.writeLock.acquire()
            self.pickle_file = gzip.open(self.pickle_name,'wb')
            self.edfWriter = EW.EdfWriter(self.edfName, edf_channels)
            self.writing = True
            self.writeLock.release()
            return True

    def stopWriting(self):
        self.writeLock.acquire()
        if self.edfWriter != None and self.writing == True:
            if self.debug:
                print "Stopping recording"
            self.edfWriter.close()
        if self.pickle_file is not None and not self.pickle_file.closed:
            self.pickle_file.close()
        self.writing = False
        self.writeLock.release()
        return True

    def getSamplingRate(self):
        return self.samplingRate


#For recording purposes only

if __name__ == "__main__":
    HOST, PORT = "localhost", 9199
    emo = Emotiv(True, True, HOST, PORT)
    emo.connect()
    emo.setup()
    emo.setBufferSizeInSecs(1.0)
    emo.enableForUser(0)
    
    idt = emo.start()
    print emo.mark(0,1)
    sale = False
    while sale == False:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print "Saliendo"
            sale = True

    emo.stop()
    emo.disconnect()

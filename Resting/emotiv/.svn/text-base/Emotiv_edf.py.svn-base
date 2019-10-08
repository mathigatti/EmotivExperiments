import random
import threading
# import time
import EdfReader


NCHANNELS = 25

edf_channels = [dict() for x in xrange(NCHANNELS)]
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

for i in xrange(NCHANNELS):
    edf_channels[i]['sample_rate'] = 128
    edf_channels[i]['dimension'] = ''
    edf_channels[i]['physical_max'] = 16000
    edf_channels[i]['physical_min'] = 0
    edf_channels[i]['digital_max'] = 16000
    edf_channels[i]['digital_min'] = 0


class Emotiv:
    def __init__(self, debug, listen=False, h=0,p=0, edf_file='/home/shernandez/telefonica/src/p3/edfs/capitan_del_espacio_.edf'):
        global edf_channels
        self.eEvent = None
        self.eState = None
        self.users = []
        self.channels = [x for x in xrange(NCHANNELS)]
        self.data = [[] for x in self.channels]
        self.connected = False
        self.setted = False
        self.started = False
        self.hData = None
        self.readyFunction = None
        self.channelsLock = threading.Lock()
        self.readyFunctionLock = threading.Lock()
        self.stopflag = False
        self.exiting = False
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
        self.letterStarted = False
        self.lettersFlashed = 0
        self.flashesPerTrial = 300
        self.edf = EdfReader.EdfReader(edf_file)


    def connect(self):
        self.connected = True
        return 1

    def setup(self):
        self.users.append('dummyUser')
        self.samplingRate = 128
        self.hData = []
        self.setted = True;
        return True

    def setBufferSizeInSecs(self, size=1.0):
        return []

    def disconnect(self):
        self.exiting = True

    def setChannelsFilter(self, channels):
        self.channels = channels
        self.data = [[] for x in self.channels];
        return True

    def setReadyFunction(self, function):
        self.readyFunction = function

    def getUsers(self):
        return self.users

    def enableForUser(self, userId):
        pass

    def __acquire(self):
        self.stopflag = False
        while self.stopflag == False:
            mas_cuatro = random.randint(0,1)
            nSamplesTaken = 12 + 4 * mas_cuatro
            if nSamplesTaken != 0:
                self.channelsLock.acquire()
                self.data = [[]] * 25
                for _ in xrange(nSamplesTaken):
                    if self.edf.has_next():
                        sample = self.edf.read_sample()
                        self.data = [channel_data + [sample[i]] for i, channel_data in enumerate(self.data) ]              
                self.channelsLock.release()

                self.readyFunctionLock.acquire()
                if self.readyFunction != None:
                    self.readyFunction(self.data)
                self.readyFunctionLock.release()
            # time.sleep(0.1)
        self.started = False
        print "Finishing acquire"

    def _processExpressivEvent(self):
        pass

    def start(self):
        if not self.setted:
            print "Emotiv not setted up"
            return False
        if self.started:
            print "Emotiv already started"
            return False
        self.started = True
        self.reader = threading.Thread(target=self.__acquire)
        self.reader.daemon = True
        self.reader.start()
        return self.reader

    def addExpressivCallback(self, event, callbackFunc):
        self.callbacks[event] = callbackFunc

    def stop(self):
        self.stopflag = True

    def mark(self, userid, value):
        return 1

    def setEdfOutput(self, filename):
        pass

    def startWriting(self):
        pass

    def stopWriting(self):
        pass

    def getSamplingRate(self):
        return self.samplingRate

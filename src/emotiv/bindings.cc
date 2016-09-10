#include <Python.h>
#include <edk.h>
#include <edkErrorCode.h>
#include <EmoStateDLL.h>

static PyObject *emotivError;

char errbuffer [2048];

void freeData(PyObject * hData) {
	EE_DataFree(PyCapsule_GetPointer(hData, NULL));
	
}


static PyObject *
emotiv_EE_DataCreate(PyObject *self, PyObject *args)
{

	DataHandle hData = EE_DataCreate();
	PyObject * retorno = PyCapsule_New(hData, NULL, &freeData);
	return retorno;
}

static PyObject *
emotiv_EE_DataSetBufferSizeInSec(PyObject *self, PyObject *args)
{
	float size;
	if (!PyArg_ParseTuple(args, "f", &size)) {
		PyErr_SetString(emotivError, "No buffer size specified.");
	}
	int result = EE_DataSetBufferSizeInSec(size);
	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

void freeEvent(PyObject * eEvent) {
	EE_EmoEngineEventFree(PyCapsule_GetPointer(eEvent, NULL));
	
}

static PyObject *
emotiv_EE_EmoEngineEventCreate(PyObject *self, PyObject *args)
{

	EmoEngineEventHandle eEvent = EE_EmoEngineEventCreate();
	// printf("EmoEngineEventHandle at %p\n", eEvent);
	PyObject * retorno = PyCapsule_New(eEvent, NULL, &freeEvent);
	return retorno;
}

void freeState(PyObject * eState) {
	EE_EmoStateFree(PyCapsule_GetPointer(eState, NULL));
	
}

static PyObject *
emotiv_EE_EmoStateCreate(PyObject *self, PyObject *args)
{

	EmoStateHandle eState = EE_EmoStateCreate();
	PyObject * retorno = PyCapsule_New(eState, NULL, &freeState);
	return retorno;
}


static PyObject *
emotiv_EE_EngineConnect(PyObject *self, PyObject *args)
{
	
	int result = EE_EngineConnect();
	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_EE_EngineDisconnect(PyObject *self, PyObject *args)
{
	
	int result = EE_EngineDisconnect();
	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_EE_EngineGetNextEvent(PyObject *self, PyObject *args)
{
	PyObject * eEventObject;
	// printf("emotiv_EE_EngineGetNextEvent\n");
	if (!PyArg_ParseTuple(args, "O", &eEventObject)) {
		PyErr_SetString(emotivError, "No EmoEngineEventHandle specified.");
		
	}
	EmoEngineEventHandle eEvent = (EmoEngineEventHandle ) PyCapsule_GetPointer(eEventObject, NULL);
	// printf("emotiv_EE_EngineGetNextEvent %p\n", eEvent);

	int state = EE_EngineGetNextEvent(eEvent);

	PyObject * retorno = Py_BuildValue("i", state);
	return retorno;
}

static PyObject *
emotiv_EE_EmoEngineEventGetType(PyObject *self, PyObject *args)
{
	PyObject * eEventObject;
	// printf("emotiv_EE_EmoEngineEventGetType\n");

	if (!PyArg_ParseTuple(args, "O", &eEventObject)) {
		PyErr_SetString(emotivError, "No EmoEngineEventHandle specified.");
		
	}
	EmoEngineEventHandle eEvent = (EmoEngineEventHandle) PyCapsule_GetPointer(eEventObject, NULL);
	EE_Event_t eventType = EE_EmoEngineEventGetType(eEvent);

	PyObject * retorno = Py_BuildValue("i", eventType);
	return retorno;
}

static PyObject *
emotiv_EE_EmoEngineEventGetUserId(PyObject *self, PyObject *args)
{
	PyObject * eEventObject;
	// printf("emotiv_EE_EmoEngineEventGetUserId\n");
	
	if (!PyArg_ParseTuple(args, "O", &eEventObject)) {
		PyErr_SetString(emotivError, "No EmoEngineEventHandle specified.");
		
	}
	unsigned int userID = 0;
	EmoEngineEventHandle eEvent = (EmoEngineEventHandle) PyCapsule_GetPointer(eEventObject, NULL);
	int result = EE_EmoEngineEventGetUserId(eEvent, &userID);

	PyObject * retorno = Py_BuildValue("ii", result, userID);
	return retorno;
}

static PyObject *
emotiv_EE_DataGetSamplingRate(PyObject *self, PyObject *args)
{
	unsigned int userID;
	if (!PyArg_ParseTuple(args, "I", &userID)) {
		PyErr_SetString(emotivError, "No user ID specified.");
	}

	unsigned int samplingRate = 0;
	int result = EE_DataGetSamplingRate(userID, &samplingRate);

	PyObject * retorno = Py_BuildValue("ii", result, samplingRate);
	return retorno;
}

static PyObject *
emotiv_EE_DataAcquisitionEnable(PyObject *self, PyObject *args)
{
	unsigned int userID;
	int value;
	if (!PyArg_ParseTuple(args, "Ii", &userID, &value)) {
		PyErr_SetString(emotivError, "No user ID or value specified.");
	}

	int result = EE_DataAcquisitionEnable(userID, value);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}



static PyObject *
emotiv_EE_DataUpdateHandle(PyObject *self, PyObject *args)
{
	PyObject * handleObject;
	unsigned int userID;
	if (!PyArg_ParseTuple(args, "IO", &userID, &handleObject)) {
		PyErr_SetString(emotivError, "No userID or DataHandle specified.");
		
	}
	DataHandle hData = (DataHandle ) PyCapsule_GetPointer(handleObject, NULL);

	int result = EE_DataUpdateHandle(userID, hData);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}


static PyObject *
emotiv_EE_DataGetNumberOfSample(PyObject *self, PyObject *args)
{
	PyObject * handleObject;
	if (!PyArg_ParseTuple(args, "O", &handleObject)) {
		PyErr_SetString(emotivError, "No DataHandle specified.");
		
	}
	DataHandle hData = (DataHandle ) PyCapsule_GetPointer(handleObject, NULL);
	unsigned int nSamplesTaken;
	int result = EE_DataGetNumberOfSample(hData, &nSamplesTaken);

	PyObject * retorno = Py_BuildValue("ii", result, nSamplesTaken);
	return retorno;
}

static PyObject *
emotiv_EE_DataGet(PyObject *self, PyObject *args)
{
	PyObject * handleObject;
	int dataChannel;
	int nSamples;
	if (!PyArg_ParseTuple(args, "Oii", &handleObject, &dataChannel, &nSamples)) {
		PyErr_SetString(emotivError, "No DataHandle specified.");
		
	}
	double data[nSamples];
	DataHandle hData = (DataHandle ) PyCapsule_GetPointer(handleObject, NULL);
	int result = EE_DataGet(hData, (EE_DataChannel_t) dataChannel, data, nSamples);

	PyObject * lst = PyList_New(nSamples);
	if (!lst)
	    lst = NULL;
	for (int i = 0; i < nSamples; i++) {
	    PyObject *num = PyFloat_FromDouble(data[i]);
	    if (!num) {
	        Py_DECREF(lst);
	        lst = NULL;
	    }
	    PyList_SET_ITEM(lst, i, num);   // reference to num stolen
	}
	PyObject * retorno = Py_BuildValue("iO", result, lst);
	return retorno;
}




static PyObject *
emotiv_EE_DataSetMarker(PyObject *self, PyObject *args)
{
	unsigned int userID;
	int value;
	if (!PyArg_ParseTuple(args, "Ii", &userID, &value)) {
		PyErr_SetString(emotivError, "No userID or value specified.");
		
	}
	int result = EE_DataSetMarker(userID, value);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_EE_ExpressivSetThreshold(PyObject *self, PyObject *args)
{
	unsigned int userID;
	int algoName;
	int thresholdName;
	int value;
	if (!PyArg_ParseTuple(args, "Iiii", &userID, &algoName, &thresholdName, &value)) {
		PyErr_SetString(emotivError, "No userID, algoName, thresholdName or value specified.");
		
	}
	int result = EE_ExpressivSetThreshold(userID, (EE_ExpressivAlgo_enum)algoName, (EE_ExpressivThreshold_enum)thresholdName, value);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_EE_EmoEngineEventGetEmoState(PyObject *self, PyObject *args)
{
	PyObject * eEventObject;
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "OO", &eEventObject, &eStateObject)) {
		PyErr_SetString(emotivError, "No eEventObject or eStateObject specified.");
		
	}
	EmoEngineEventHandle eEvent = (EmoEngineEventHandle) PyCapsule_GetPointer(eEventObject, NULL);
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	int result = EE_EmoEngineEventGetEmoState(eEvent, eState);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_ES_ExpressivIsBlink(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	int result = ES_ExpressivIsBlink(eState);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}


static PyObject *
emotiv_ES_ExpressivIsLeftWink(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	int result = ES_ExpressivIsLeftWink(eState);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}



static PyObject *
emotiv_ES_ExpressivIsRightWink(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	int result = ES_ExpressivIsRightWink(eState);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_ES_ExpressivGetUpperFaceAction(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	int result = ES_ExpressivGetUpperFaceAction(eState);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_ES_ExpressivGetLowerFaceAction(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	int result = ES_ExpressivGetLowerFaceAction(eState);

	PyObject * retorno = Py_BuildValue("i", result);
	return retorno;
}

static PyObject *
emotiv_ES_ExpressivGetUpperFaceActionPower(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	float result = ES_ExpressivGetUpperFaceActionPower(eState);

	PyObject * retorno = Py_BuildValue("f", result);
	return retorno;
}

static PyObject *
emotiv_ES_ExpressivGetLowerFaceActionPower(PyObject *self, PyObject *args)
{
	PyObject * eStateObject;
	if (!PyArg_ParseTuple(args, "O", &eStateObject)) {
		PyErr_SetString(emotivError, "No eStateObject specified.");
		
	}
	EmoStateHandle eState = (EmoStateHandle) PyCapsule_GetPointer(eStateObject, NULL);
	float result = ES_ExpressivGetLowerFaceActionPower(eState);

	PyObject * retorno = Py_BuildValue("f", result);
	return retorno;
}


static PyMethodDef EmotivMethods[] = {
	{"EE_DataCreate",  emotiv_EE_DataCreate, METH_VARARGS, "Returns a handle to memory that can hold data. This handle can be reused by the caller to retrieve subsequent data."},
	{"EE_DataSetBufferSizeInSec",  emotiv_EE_DataSetBufferSizeInSec, METH_VARARGS, "Sets the size of the data buffer. The size of the buffer affects how frequent EE_DataUpdateHandle() needs to be called to prevent data loss."},
	{"EE_EmoEngineEventCreate",  emotiv_EE_EmoEngineEventCreate, METH_VARARGS, "Returns a handle to memory that can hold an EmoEngine event. This handle can be reused by the caller to retrieve subsequent events."},
	{"EE_EmoStateCreate",  emotiv_EE_EmoStateCreate, METH_VARARGS, "Returns a handle to memory that can store an EmoState. This handle can be reused by the caller to retrieve subsequent EmoStates."},
	{"EE_EngineConnect",  emotiv_EE_EngineConnect, METH_VARARGS, "Initializes the connection to EmoEngine. This function should be called at the beginning of programs that make use of EmoEngine, most probably in initialization routine or constructor."},
	{"EE_EngineGetNextEvent",  emotiv_EE_EngineGetNextEvent, METH_VARARGS, "Retrieves the next EmoEngine event."},
	{"EE_EmoEngineEventGetType",  emotiv_EE_EmoEngineEventGetType, METH_VARARGS, "Returns the event type for an event already retrieved using EE_EngineGetNextEvent."},
	{"EE_EmoEngineEventGetUserId",  emotiv_EE_EmoEngineEventGetUserId, METH_VARARGS, "Retrieves the user ID for EE_UserAdded and EE_UserRemoved events."},
	{"EE_DataGetSamplingRate",  emotiv_EE_DataGetSamplingRate, METH_VARARGS, "Gets sampling rate."},
	{"EE_DataAcquisitionEnable",  emotiv_EE_DataAcquisitionEnable, METH_VARARGS, "Controls acquisition of data from EmoEngine (which is off by default)."},
	{"EE_DataUpdateHandle",  emotiv_EE_DataUpdateHandle, METH_VARARGS, "Updates the content of the data handle to point to new data since the last call."},
	{"EE_DataGetNumberOfSample",  emotiv_EE_DataGetNumberOfSample, METH_VARARGS, "Returns number of sample of data stored in the data handle."},
	{"EE_DataGet",  emotiv_EE_DataGet, METH_VARARGS, "Extracts data from the data handle."},
	{"EE_EngineDisconnect",  emotiv_EE_EngineDisconnect, METH_VARARGS, "Terminates the connection to EmoEngine. This function should be called at the end of programs which make use of EmoEngine, most probably in clean up routine or destructor."},
	{"EE_DataSetMarker",  emotiv_EE_DataSetMarker, METH_VARARGS, "Sets marker."},
	{"EE_ExpressivSetThreshold",  emotiv_EE_ExpressivSetThreshold, METH_VARARGS, "Sets threshold for Expressiv algorithms."},
	{"EE_EmoEngineEventGetEmoState",  emotiv_EE_EmoEngineEventGetEmoState, METH_VARARGS, "Get Emo State from Event."},
	{"ES_ExpressivIsBlink",  emotiv_ES_ExpressivIsBlink, METH_VARARGS, "Returns 1 if the event is a blink."},
	{"ES_ExpressivIsLeftWink",  emotiv_ES_ExpressivIsLeftWink, METH_VARARGS, "Returns 1 if the event is a left wink"},
	{"ES_ExpressivIsRightWink",  emotiv_ES_ExpressivIsRightWink, METH_VARARGS, "Returns 1 if the event is a right wink"},
	{"ES_ExpressivGetUpperFaceAction",  emotiv_ES_ExpressivGetUpperFaceAction, METH_VARARGS, "Returns the detected upper face Expressiv action of the user"},
	{"ES_ExpressivGetLowerFaceAction",  emotiv_ES_ExpressivGetLowerFaceAction, METH_VARARGS, "Returns the detected lower face Expressiv action of the user"},
	{"ES_ExpressivGetUpperFaceActionPower",  emotiv_ES_ExpressivGetUpperFaceActionPower, METH_VARARGS, "Returns the detected upper face Expressiv action power of the user."},
	{"ES_ExpressivGetLowerFaceActionPower",  emotiv_ES_ExpressivGetLowerFaceActionPower, METH_VARARGS, "Returns the detected lower face Expressiv action power of the user."},
	{NULL, NULL, 0, NULL}
};

#define xstr(s) str(s)
#define str(s) #s

#define ADD_CONSTANT_VALUE(x) PyModule_AddIntConstant(m, #x, x);

PyMODINIT_FUNC
initemotiv(void)
{
	PyObject *m;

	m = Py_InitModule("emotiv", EmotivMethods);
	if (m == NULL)
		return;
	emotivError = PyErr_NewException("emotiv.error", NULL, NULL);
	Py_INCREF(emotivError);
	PyModule_AddObject(m, "error", emotivError);

	ADD_CONSTANT_VALUE(EDK_OK)
	ADD_CONSTANT_VALUE(EDK_UNKNOWN_ERROR)
	ADD_CONSTANT_VALUE(EDK_INVALID_DEV_ID_ERROR)
	ADD_CONSTANT_VALUE(EDK_INVALID_PROFILE_ARCHIVE)
	ADD_CONSTANT_VALUE(EDK_NO_USER_FOR_BASEPROFILE)	
	ADD_CONSTANT_VALUE(EDK_CANNOT_ACQUIRE_DATA)	
	ADD_CONSTANT_VALUE(EDK_BUFFER_TOO_SMALL)		
	ADD_CONSTANT_VALUE(EDK_OUT_OF_RANGE)			
	ADD_CONSTANT_VALUE(EDK_INVALID_PARAMETER)
	ADD_CONSTANT_VALUE(EDK_PARAMETER_LOCKED)
	ADD_CONSTANT_VALUE(EDK_COG_INVALID_TRAINING_ACTION)
	ADD_CONSTANT_VALUE(EDK_COG_INVALID_TRAINING_CONTROL)
	ADD_CONSTANT_VALUE(EDK_COG_INVALID_ACTIVE_ACTION)
	ADD_CONSTANT_VALUE(EDK_COG_EXCESS_MAX_ACTIONS)
	ADD_CONSTANT_VALUE(EDK_EXP_NO_SIG_AVAILABLE)        
	ADD_CONSTANT_VALUE(EDK_FILESYSTEM_ERROR)          
	ADD_CONSTANT_VALUE(EDK_INVALID_USER_ID)		
	ADD_CONSTANT_VALUE(EDK_EMOENGINE_UNINITIALIZED)
	ADD_CONSTANT_VALUE(EDK_EMOENGINE_DISCONNECTED)	
	ADD_CONSTANT_VALUE(EDK_EMOENGINE_PROXY_ERROR)	
	ADD_CONSTANT_VALUE(EDK_NO_EVENT)		
	ADD_CONSTANT_VALUE(EDK_GYRO_NOT_CALIBRATED)
	ADD_CONSTANT_VALUE(EDK_OPTIMIZATION_IS_ON)	
	ADD_CONSTANT_VALUE(EDK_RESERVED1)

	ADD_CONSTANT_VALUE(EE_UnknownEvent)
	ADD_CONSTANT_VALUE(EE_UnknownEvent)
	ADD_CONSTANT_VALUE(EE_EmulatorError)
	ADD_CONSTANT_VALUE(EE_ReservedEvent)
	ADD_CONSTANT_VALUE(EE_UserAdded)
	ADD_CONSTANT_VALUE(EE_UserRemoved)	
	ADD_CONSTANT_VALUE(EE_EmoStateUpdated)
	ADD_CONSTANT_VALUE(EE_ProfileEvent)
	ADD_CONSTANT_VALUE(EE_CognitivEvent)
	ADD_CONSTANT_VALUE(EE_ExpressivEvent)
	ADD_CONSTANT_VALUE(EE_InternalStateChanged)
	ADD_CONSTANT_VALUE(EE_AllEvent)

	ADD_CONSTANT_VALUE(ED_COUNTER)
	ADD_CONSTANT_VALUE(ED_INTERPOLATED)
	ADD_CONSTANT_VALUE(ED_RAW_CQ)
	ADD_CONSTANT_VALUE(ED_AF3)
	ADD_CONSTANT_VALUE(ED_F7)
	ADD_CONSTANT_VALUE(ED_F3)
	ADD_CONSTANT_VALUE(ED_FC5)
	ADD_CONSTANT_VALUE(ED_T7) 
	ADD_CONSTANT_VALUE(ED_P7) 
	ADD_CONSTANT_VALUE(ED_O1) 
	ADD_CONSTANT_VALUE(ED_O2) 
	ADD_CONSTANT_VALUE(ED_P8) 
	ADD_CONSTANT_VALUE(ED_T8)
	ADD_CONSTANT_VALUE(ED_FC6) 
	ADD_CONSTANT_VALUE(ED_F4) 
	ADD_CONSTANT_VALUE(ED_F8)
	ADD_CONSTANT_VALUE(ED_AF4)
	ADD_CONSTANT_VALUE(ED_GYROX) 
	ADD_CONSTANT_VALUE(ED_GYROY)
	ADD_CONSTANT_VALUE(ED_TIMESTAMP)
	ADD_CONSTANT_VALUE(ED_ES_TIMESTAMP)
	ADD_CONSTANT_VALUE(ED_FUNC_ID)
	ADD_CONSTANT_VALUE(ED_FUNC_VALUE)
	ADD_CONSTANT_VALUE(ED_MARKER)
	ADD_CONSTANT_VALUE(ED_SYNC_SIGNAL)



	ADD_CONSTANT_VALUE(EXP_NEUTRAL)
	ADD_CONSTANT_VALUE(EXP_BLINK)
	ADD_CONSTANT_VALUE(EXP_WINK_LEFT) 	
	ADD_CONSTANT_VALUE(EXP_WINK_RIGHT) 	
	ADD_CONSTANT_VALUE(EXP_HORIEYE)
	ADD_CONSTANT_VALUE(EXP_EYEBROW)	
	ADD_CONSTANT_VALUE(EXP_FURROW)	
	ADD_CONSTANT_VALUE(EXP_SMILE)	
	ADD_CONSTANT_VALUE(EXP_CLENCH) 	
	ADD_CONSTANT_VALUE(EXP_LAUGH)	
	ADD_CONSTANT_VALUE(EXP_SMIRK_LEFT) 	
	ADD_CONSTANT_VALUE(EXP_SMIRK_RIGHT)

	ADD_CONSTANT_VALUE(EXP_SENSITIVITY)



	PyModule_AddIntConstant(m, "NCHANNELS", ED_SYNC_SIGNAL+1);

}

import copy
import datetime as dt
import struct

class EdfWriter(object):
    def __init__(self, file_name, channel_info, **kwargs):
        '''Initialises an EDF file at @file_name. 
        @channel_info should be a 
        list of dicts, one for each channel in the data. Each dict needs 
        these values:
            
            'label' : channel label (string, <= 16 characters, must be unique)
            'dimension' : physical dimension (e.g., mV) (string, <= 8 characters)
            'sample_rate' : sample frequency in hertz (int)
            'physical_max' : maximum physical value (float)
            'physical_min' : minimum physical value (float)
            'digital_max' : maximum digital value (int, -2**15 <= x < 2**15)
            'digital_min' : minimum digital value (int, -2**15 <= x < 2**15)
            optional:
            'transducer_type'
            'prefiltering'

        @kwargs can contain:
            'patient_name'
            'recording'

        '''
        self.path = file_name
        self.channels = {}
        self.records_written = 0
        self.channels = channel_info
        self.sample_buffer = dict([(c['label'],[]) for c in channel_info])
        self.channels_written = 0
        self.file_handle = open(self.path , 'w')
        self._write_header(**kwargs)
         

    def write_sample(self, channel, sample):
        '''Queues a digital sample for @channel_label for recording; the data won't 
        actually be written until one second's worth of data has been queued.'''
        self.sample_buffer[self.channels[channel]['label']].append(sample)
        if len(self.sample_buffer[self.channels[channel]['label']]) == self.channels[channel]['sample_rate']:
            self.channels_written = self.channels_written+1

        if self.channels_written == len(self.channels):
            self._flush_samples()
            self.channels_written = 0

    def close(self):
        self.file_handle.seek(236)
        field = str(self.records_written)
        l = len(field)
        field = field + ' ' * (8 -l)
        self.file_handle.write(field)
        self.file_handle.close()

    def _write_header(self, **kwargs):
        def get_if_set(kw_name):
            item = kwargs.pop(kw_name, None)
            if item is not None:
                return item
            else:
                return ''

        # Version
        self.file_handle.write('0' + ' ' * 7)

        # Patient
        field = get_if_set('patient_name')
        l = len(field)
        field = field + ' ' * (80 -l)
        self.file_handle.write(field)

        # Recording
        field = get_if_set('recording')
        l = len(field)
        field = field + ' ' * (80 -l)
        self.file_handle.write(field)

        # Start Date
        d = dt.datetime.now()
        field = d.strftime('%d.%m.%y')
        self.file_handle.write(field)

        # Start Time
        field = d.strftime('%H.%M.%S')
        self.file_handle.write(field)

        # Length of header
        ns = len(self.channels)
        header_len = ns * 256 + 256
        field = str(header_len)
        l = len(field)
        field = field + ' ' * (8 -l)
        self.file_handle.write(field)

        # Reserved
        field = ' ' * 44
        self.file_handle.write(field)

        # Data records (sec)
        field = '-1' + ' ' * 6
        self.file_handle.write(field)

        # Duration of a data record
        field = '1' + ' ' * 7
        self.file_handle.write(field)

        # Number of signals
        field = str(ns)
        l = len(field)
        field = field + ' ' * (4 -l)
        self.file_handle.write(field)

        for i,val in enumerate(self.channels):
            # Signal label
            field = val['label']
            l = len(field)
            field = field + ' ' * (16 -l)
            self.file_handle.write(field)

        for i,val in enumerate(self.channels):
            field = ''
            if 'transducer_type' in val:
                field = val['transducer_type']
        
        for i,val in enumerate(self.channels):
            
            l = len(field)
            field = field + ' ' * (80 -l)
            self.file_handle.write(field)

        for i,val in enumerate(self.channels):
            
            field = val['dimension']
            l = len(field)
            field = field + ' ' * (8 -l)
            self.file_handle.write(field)    

        for i,val in enumerate(self.channels):
            
            field = str(val['physical_min'])
            l = len(field)
            field = field + ' ' * (8 -l)
            self.file_handle.write(field) 

        for i,val in enumerate(self.channels):
            
            field = str(val['physical_max'])
            l = len(field)
            field = field + ' ' * (8 -l)
            self.file_handle.write(field) 

        for i,val in enumerate(self.channels):
            
            field = str(val['digital_min'])
            l = len(field)
            field = field + ' ' * (8 -l)
            self.file_handle.write(field)

        for i,val in enumerate(self.channels):
            
            field = str(val['digital_max'])
            l = len(field)
            field = field + ' ' * (8 -l)
            self.file_handle.write(field) 

        for i,val in enumerate(self.channels):
            
            field = ''
            if 'prefiltering' in val:
                field = val['prefiltering']
            l = len(field)
            field = field + ' ' * (80 -l)
            self.file_handle.write(field) 

        for i,val in enumerate(self.channels):
            
            field = str(val['sample_rate'])
            l = len(field)
            field = field + ' ' * (8 -l)
            self.file_handle.write(field) 

        for i,val in enumerate(self.channels):
            
            # Reserved
            field = ' ' * 32
            self.file_handle.write(field)


    def _flush_samples(self):
        for c in self.channels:
            scale = (float(c['digital_max']) - float(c['digital_min']))/(float(c['physical_max']) - float(c['physical_min']))
            for s in range(c['sample_rate']):
                self.file_handle.write(struct.pack("<h", int(self.sample_buffer[c['label']][s]*scale)))
            self.sample_buffer[c['label']] = self.sample_buffer[c['label']][c['sample_rate']:]
        self.records_written = self.records_written + 1


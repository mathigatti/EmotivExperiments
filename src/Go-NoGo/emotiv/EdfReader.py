import struct


class EdfReader(object):
    def __init__(self, file_name, **kwargs):
        '''Reads an EDF file at @file_name.
        '''
        self.path = file_name
        self.metadata = dict()
        self.file_handle = open(self.path, 'r')
        self.metadata['version'] = self.file_handle.read(8)
        self.metadata['patient'] = self.file_handle.read(80)
        self.metadata['recording'] = self.file_handle.read(80)
        self.metadata['startdate'] = self.file_handle.read(8)
        self.metadata['starttime'] = self.file_handle.read(8)
        self.metadata['header_bytes'] = int(self.file_handle.read(8))
        self.metadata['reserved'] = self.file_handle.read(44)
        self.metadata['ndata'] = int(self.file_handle.read(8))
        self.metadata['ldata'] = int(self.file_handle.read(8))
        self.metadata['nchannels'] = self.file_handle.read(4)

        self.nchannels = int(self.metadata['nchannels'])

        self.metadata['channels'] = [dict() for x in range(self.nchannels)]

        for i in range(self.nchannels):
            self.metadata['channels'][i]['label'] = self.file_handle.read(16)
        for i in range(self.nchannels):
            self.metadata['channels'][i]['type'] = self.file_handle.read(80)
        for i in range(self.nchannels):
            self.metadata['channels'][i]['dimension'] = self.file_handle.read(8)
        for i in range(self.nchannels):
            self.metadata['channels'][i]['physical_min'] = \
                float(self.file_handle.read(8))
        for i in range(self.nchannels):
            self.metadata['channels'][i]['physical_max'] = \
                float(self.file_handle.read(8))
        for i in range(self.nchannels):
            self.metadata['channels'][i]['digital_min'] = \
                float(self.file_handle.read(8))
        for i in range(self.nchannels):
            self.metadata['channels'][i]['digital_max'] = \
                float(self.file_handle.read(8))
        for i in range(self.nchannels):
            self.metadata['channels'][i]['prefiltering'] = \
                self.file_handle.read(80)
        for i in range(self.nchannels):
            self.metadata['channels'][i]['sampling_rate'] = \
                int(self.file_handle.read(8))
        for i in range(self.nchannels):
            self.metadata['channels'][i]['reserved'] = self.file_handle.read(32)

        self.readdata = [[] for x in range(self.nchannels)]
        # Prepare buffers for block reads
        for i in range(self.nchannels):
            self.readdata[i] = \
                [0 for x in range(self.metadata['channels'][i]['sampling_rate']
                 * self.metadata['ldata'])]

        self.records_read = 0
        self.samples_read_in_record = self.sampling_rate()

    def _read_sample_block(self):
        for channel in range(self.nchannels):
            scale = (self.metadata['channels'][channel]['digital_max'] -
                     self.metadata['channels'][channel]['digital_min']) / \
                    (self.metadata['channels'][channel]['physical_max'] -
                     self.metadata['channels'][channel]['physical_min'])
            toread = self.metadata['channels'][channel]['sampling_rate'] \
                * self.metadata['ldata']
            for sample in range(toread):
                raw_sample = struct.unpack('<h', self.file_handle.read(2))[0]
                self.readdata[channel][sample] = raw_sample/scale
        self.records_read = self.records_read+1
        self.samples_read_in_record = 0

    def ensure_sample_block(self):
        if self.samples_read_in_record == self.sampling_rate():
            self._read_sample_block()

    ''' Reads a sample from each channel. If needed, reads a sample block
    from the file.
    Asumes every channel has the same sampling rate
    '''
    def read_sample(self):
        if self.samples_read_in_record == self.sampling_rate():
            self._read_sample_block()
        sample = [0.0 for x in range(self.nchannels)]
        for i in range(self.nchannels):
            sample[i] = self.readdata[i][self.samples_read_in_record]
        self.samples_read_in_record = self.samples_read_in_record+1
        return sample

    def has_next(self):
        return self.records_read != self.metadata['ndata']

    def sampling_rate(self):
        return self.metadata['channels'][0]['sampling_rate']

    def close(self):
        self.file_handle.close()


if __name__ == "__main__":
    import time
    er = EdfReader('tests/test.edf')
    while er.has_next():
        print er.read_sample()
        time.sleep(1.0/er.sampling_rate())

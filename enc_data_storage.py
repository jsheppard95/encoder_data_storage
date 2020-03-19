"""
enc_data_storage.py

Module to read encoder array PVs and output .csv file with timestamps
"""

from ophyd.signal import EpicsSignalRO
import numpy as np
import sys
import time

# Constants
ENC_PV = 'MR1L0:ENC:PITCH:ACTPOSARRAY_RBV' # Encoder Array PV
SIG_NAME = 'mr1l0_enc_pitch_actposarray_rbv' # Encoder Array PV Sinal Name
EPICS_SAMPLE_TIME = 1.0 # Timespan of array data in seconds
DELTA_T = 0.001 # Time spacing between array points in seconds
OUTFILE_NAME = 'test_data.csv'
ACQ_TIME = 3 # Acquisition time, integer number of seconds

sig = EpicsSignalRO(ENC_PV)

try:
    sig.wait_for_connection(timeout=3.0)
except TimeoutError:
    print('Could not connect to data from PV %s, timed out.' % ENC_PV)
    print('Either on wrong subnet or the ioc is off.')
    print('Make sure you are on one of the following machines:')
    print('psbuild-rhel7-01, psbuild-rhel7-02, lfe-console (lfe PVs),'
          'kfe-console (kfe PVs')
    sys.exit(1)


tvals = [] # Time values associated with each encoder RBV
enc_vals = [] # Encoder RBV arrays, 1000 elements each
timestamps = [] # timestamp for each encoder array

def cb(value=None, timestamp=None, **kwargs):
    """
    Callback function that gets passed to EpicsSignalRO.subscribe
    Processes the array/timestamps and computes time value for each point in the array

    Parameters:
    -----------
    acq_time : int
        seconds of data to write to file. should be a positive integer
    outfile_name : str
        Output file to write encoder array with timestamps to
    value : numpy array
        Will become current actual position array, gets filled by EpicsSignalRO
    timestamp : float
        Will become current timestamp for actual position array,
        i.e ``timestamp`` of ``value``
    """
    # Get Current array and associated timestamp
    # Assuming timestamp corresponds to last point in array, is this an OK
    # assumption?
    enc_vals.append(value)
    timestamps.append(timestamp) # Ken mentioned system time was better, why?

sig.subscribe(cb) # callback id
time.sleep(ACQ_TIME) # wait the integer number of seconds to acquire
sig.unsubscribe_all()

# Inspecting with datetime.fromtimestamp(current_timestamp), this appears
# to be correct
# Should have list [arr1, arr2, ... , arrACQ_TIME]
# Need to covert to arrays of tvals that match up with enc_vals
for i in range(len(enc_vals)):
    curr_time_array = np.zeros(enc_vals[i].size)
    # Enc Array has 1000 points sampled at 1 kHz -> 1 s of data, each point
    # 0.001 s apart
    # Assume timestamp corresponds to last point in array
    curr_time_array[0] = timestamps[i] - EPICS_SAMPLE_TIME
    for j in range(1, curr_time_array.size):
        curr_time_array[j] = curr_time_array[0] + (DELTA_T*j)
    tvals.append(curr_time_array)

# Write tvals and current_array to file
with open(OUTFILE_NAME, 'w') as outfile:
    # HEADER: timestamp, PV
    outfile.write(ENC_PV + '\n')
    outfile.write('\n')
    # Now write the real arrays
    for i in range(len(tvals)):
        for j in range(len(tvals[i])):
            outfile.write(str(tvals[i][j]) + ',' + str(enc_vals[i][j]) + '\n')

"""
enc_data_storage.py

Module to read encoder array PVs and output .csv file with timestamps
"""

from ophyd.signal import EpicsSignalRO
import numpy as np

# Constants
ENC_PV = 'MR1L0:ENC:PITCH:ACTPOSARRAY_RBV' # Encoder Array PV
SIG_NAME = 'mr1l0_enc_pitch_actposarray_rbv' # Encoder Array PV Sinal Name
SAMPLE_TIME = 1.0 # Timespan of array data in seconds
DELTA_T = 0.001 # Time spacing between array points in seconds
OUTFILE_NAME = 'test_data.csv'

def cb(outfile_name=OUTFILE_NAME, value=None, timestamp=None, **kwargs):
    """
    Callback function that gets passed to EpicsSignalRO.subscribe
    Processes the array/timestamps and computes time value for each point in the array

    Parameters:
    -----------
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
    current_array = value
    current_timestamp = timestamp # Ken mentioned system time was better, why?
    # Inspecting with datetime.fromtimestamp(current_timestamp), this appears
    # to be correct
    tvals = np.zeros(current_array.size)
    # Enc Array has 1000 points sampled at 1 kHz -> 1 s of data, each point
    # 0.001 s apart
    tvals[0] = current_timestamp - SAMPLE_TIME
    for i in range(1, tvals.size):
        tvals[i] = tvals[0] + (DELTA_T*i)
    # Write tvals and current_array to file
    outfile = open(outfile_name, 'w')
    # write enc timestamp to top of file - used for debug
    outfile.write(str(current_timestamp) + '\n')
    outfile.write('\n')
    # Now write the real arrays
    for i in range(len(tvals)):
        outfile.write(str(tvals[i]) + ' ' + str(current_array[i]) + '\n')
    outfile.close()

"""
enc_data_storage.py

Module to read encoder array PVs and output .csv file with timestamps
"""

from ophyd.signal import EpicsSignalRO
import numpy as np
import sys
import time

# Constants
EPICS_SAMPLE_TIME = 10.0 # Timespan of array data in seconds
DELTA_T = 0.01 # Time spacing between array points in seconds

##############################################################################
# Collecting Args and Error Handling:
def usage():
    print('Usage:')
    print('./optics-enc-data-storage.sh <PV> <Acquisition Time> <Outfile Name>')

# Input Args: pv acq_time outfile
args = sys.argv
if len(sys.argv) != 4:
    print('Incorrect Number of Arguments')
    usage()
    sys.exit(1)

enc_pv = args[1]
try:
    acq_time = float(args[2])
except ValueError:
    print('Input Arguments In Wrong Order')
    usage()
    sys.exit(1)

if acq_time % EPICS_SAMPLE_TIME != 0:
    print('Acquisition Time Should Be An Integer Multiple Of %s s' % EPICS_SAMPLE_TIME)
    usage()
    sys.exit(1)

outfile_name = args[3]
##############################################################################

# Instantiate EpicsSignalRO
sig_name = enc_pv.lower().replace(':', '_')
sig = EpicsSignalRO(enc_pv, auto_monitor=True, name=sig_name)

try:
    sig.wait_for_connection(timeout=3.0)
except TimeoutError:
    print('Could not connect to data from PV %s, timed out.' % enc_pv)
    print('Either on wrong subnet or the ioc is off.')
    print('Make sure you are on one of the following machines:')
    print('psbuild-rhel7-01, psbuild-rhel7-02, lfe-console (lfe PVs),'
          'kfe-console (kfe PVs')
    sys.exit(1)

tvals = [] # Time values associated with each encoder RBV
enc_vals = [] # Encoder RBV arrays, 1000 elements each
timestamps = [] # timestamp for each encoder array

def cb(value=None, old_value=None, timestamp=None, **kwargs):
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
    # Only taking new arrays, check for update
    comparison = value == old_value
    if not comparison.all():
        enc_vals.append(value)
        timestamps.append(timestamp) # System time may be better, why?

cbid = sig.subscribe(cb) # callback id
print('Acquiring Data From PV %s ...' % enc_pv)
print('Please wait %s s' % acq_time)
time.sleep(acq_time - (EPICS_SAMPLE_TIME/2)) # wait time found by experiment
# cb seems to always finish its cycle before exiting, waiting exact acq_time
# seems to always give an extra array
# sig.unsubscribe not working in script, causes seg fault
sig.destroy() # This has desired behavior
print('Data Acquired, generated file %s' % outfile_name)

# Inspecting with datetime.fromtimestamp(current_timestamp), this appears
# to be correct
# Should have list [arr_1, arr_2, ... , arr_(acq_time/EPICS_SAMPLE_TIME)]
# Need to covert to arrays of tvals that match up with enc_vals
for i in range(len(enc_vals)):
    curr_time_array = np.zeros(enc_vals[i].size)
    # Enc Array has 1000 points sampled at 100 Hz -> 10 s of data, each point
    # 0.01 s apart
    # Assume timestamp corresponds to last point in array
    curr_time_array[0] = timestamps[i] - EPICS_SAMPLE_TIME
    for j in range(1, curr_time_array.size):
        curr_time_array[j] = curr_time_array[0] + (DELTA_T*j)
    tvals.append(curr_time_array)

# Write tvals and current_array to file
with open(outfile_name, 'w') as outfile:
    # Now write the real arrays
    for i in range(len(tvals)):
        for j in range(len(tvals[i])):
            outfile.write(str(tvals[i][j]) + ',' + str(enc_vals[i][j]) + '\n')

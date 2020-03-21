# encoder_data_storage
Usage:
```
# Go to directory with script:
$ cd /reg/g/pcds/l2si-commissioning/mirrors/encoder_data_storage/

# Run Script
$ ./optics-enc-data-storage.sh <PV> <Acquisition Time> <Outfile Name>

# Print Usage Message
$ ./optics-enc-data-storage.sh

# Example Usage:
$ ./optics-enc-data-storage.sh MR1L0:ENC:PITCH:ACTPOSARRAY_RBV 30 test.csv
```

Parameters:
```
<PV> : str
    Encoder Array PV to acquire data from.
    See https://confluence.slac.stanford.edu/display/PCDS/Offset+Mirror#OffsetMirror-EncoderReadbacks:
<Acquisition Time> : int
    Timespan of <PV> to write to file. Should be an integer multiple of 10 s
    since each array contains 10 s of data
<Outfile Name> : str
    Output file name, include full path, otherwise will write file to
    current directory
```

Converting Between Timestamp and Datetime:
```
In [1]: from datetime import datetime

In [2]: now = datetime.now()

In [3]: now
Out[3]: datetime.datetime(2020, 3, 18, 20, 56, 42, 355520)

In [4]: datetime.timestamp(now)
Out[4]: 1584590202.35552

In [5]: datetime.fromtimestamp(1584574331.86458)
Out[5]: datetime.datetime(2020, 3, 18, 16, 32, 11, 864580)
```

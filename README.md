# encoder_data_storage
Current Usage:

In an IPython Session:

```
from enc_data_storge import *
enc_signal = EpicsSignalRO(ENC_PV, automonitor=True, name=SIG_NAME) # ENC_PV and SIG_NAME defined in enc_data_storage.py
enc_signal.subscribe(cb) # cb defined in enc_data_storage.py

# Wait for an arbitrary amount of time
enc_signal.unsubscribe_all()
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

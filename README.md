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

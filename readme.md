# module twin

```bash
python module_twin.py CONNECTION_STRING  DEVICE_ID  MODULE_ID  config_module.json
```

e.g. 
python ./module_twin.py "HostName=iothubtervo01.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=G" iotedgedps01 SampleModule config_module.json



pip list

azure-core         1.31.0
azure-iot-hub      2.6.1
certifi            2024.8.30
charset-normalizer 3.4.0
idna               3.10
isodate            0.7.2
msrest             0.7.1
oauthlib           3.2.2
pip                22.0.2
requests           2.32.3
requests-oauthlib  2.0.0
setuptools         59.6.0
six                1.16.0
typing_extensions  4.12.2
uamqp              1.6.10
urllib3            2.2.3
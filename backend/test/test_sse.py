from sseclient import SSEClient

datas_stream = SSEClient('http://127.0.0.1:8000/resources/datas_stream')
for data in datas_stream:
    print(str(data))
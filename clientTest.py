from ap.client import client

client = client('127.0.0.1',61134)
client.send_credential('xinhuan','12345678')
client.close_client()
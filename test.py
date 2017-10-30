#!/usr/bin/env python3
import icgc
client=icgc.Client(url="http://localhost:8080/api/v1", authentication='')
response=client.query(requestType='donors', pql='select(*)')
print(response.json())

#!/usr/bin/env python3
"""
Test.py

This is a simple example test script to connect to a copy of the ICGC web
portal running on your
local machine.


"""
import icgc


def run():
    """
    Runs the test script
    """
    client = icgc.Client(url="http://localhost:8080/api/v1")
    for request_type in client.request_types():
        response = client.query(request_type=request_type, pql='select(*)')
        print(request_type, "===\n\n", response)


if __name__ == '__main__':
    run()

#!/usr/bin/env python3
# Copyright (c) 2017 The Ontario Institute for Cancer Research. All rights reserved. 
#
# This program and the accompanying materials are made available under the terms of the
# GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with  
# this program. If not, see <http://www.gnu.org/licenses/>.                                                     
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
Test.py

This is a simple example test script to connect to a copy of the ICGC web
portal running on your local machine.
"""

import icgc

def run():
    """
    Runs the test script
    """
    # Change the base URL to use a portal server running on my 
    # computer (on localhost port 8080), not the icgc portal server.
    icgc.BASE_URL="http://localhost:8080/api/v1/"

    for request_type in icgc.request_types():
        response = icgc.query(request_type=request_type, pql='select(*)')
        print(request_type, "===\n\n", response)

if __name__ == '__main__':
    run()

#!/usr/bin/env python3
# Copyright (c) 2017 The Ontario Institute for Cancer Research. All rights
# reserved.
#
# This program and the accompanying materials are made available under the
# terms of the GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT,  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE  POSSIBILITY OF SUCH DAMAGE.

"""
download.py

This is an example script to download donor information from a copy of the
ICGC web portal running on your local machine.
"""
from __future__ import absolute_import, division, print_function
import icgc

icgc.BASE_URL = "http://localhost:8080/api/v1/"

KB = 1024
MB = 1024 * KB


def run():
    """
    Show an example of a PQL download with automated decision making.

    We download up to a maximum of 10 MB of data from the portal, of any type
    that will fit within our download limit, and save our the results as a
    tarfile named 'test.tar'.
    """
    pql = 'eq(donor.primarySite,"Brain")'

    # Find which items are available that match our pql query, and how big
    # each of the result file are.

    sizes = icgc.download_size(pql)
    print("Sizes are: {}".format(sizes))

    # Let's choose to download as many different bits of information as we can
    # fit in a reasonably small download, say 10 MB in size, so that we don't
    # have to wait a long time for it to download.

    # We'll only include  a file in our tarfile if the total is below our
    # 10 MB limit. Our tarfile size calculation is approximate; the
    # files inside the tarfile get compressed; so the total size of the tarfile
    # that we download might be smaller than we calculate.

    max_size = 10 * MB
    current_size = 0

    # We'll just keep adding items to our list as long as they don't put us
    # over our download total.
    includes = []
    for k in sizes:
        item_size = sizes[k]
        if current_size + item_size < max_size:
            includes.append(k)
            current_size += item_size

    print("Including items {}".format(includes))
    print("Approximate download size={:.2f} MB".format(current_size / MB))

    # Download the information, and save the results in the file "test.tar"
    icgc.download(pql, includes, "test")


if __name__ == "__main__":
    run()

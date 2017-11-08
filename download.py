#!/usr/bin/env python3
# Copyright (c) 2017 The Ontario Institute for Cancer Research. All rights reserved.
#
# This program and the accompanying materials are made available under the terms of the 
# GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
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
download.py

This is an example script to download donor information from a copy of the ICGC web
portal running on your local machine.
"""
import icgc 

KB=1024
MB=1024*KB

filters='{"donor":{"primarySite":{"is":["Brain"]}}}'

# See what different items are available for our current choice of filter 
# and how big they are

sizes = icgc.download_size(filters)
print("Sizes are: {}".format(sizes))

# Let's choose to download as many different bits of information as we can fit 
# in a reasonably small download, say 10 MB in size, and just download those
# ones.

max_size=10 * MB 
current_size=0

# We'll just keep adding items to our list as long as they don't put us over our
# download total.
includes=[]
for k in sizes:
    item_size=sizes[k]
    if current_size + item_size < max_size: 
       includes.append(k)
       current_size += item_size

print("Including items {}".format(includes))
print("Approximate download size={:.2f} MB".format(current_size / MB))

# Download the information, and save the results in the file "test1.tar"
icgc.download(filters,includes,"test1")

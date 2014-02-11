# Parse map XML for live but not scannable IPs.

import argparse
import datetime
from collections import defaultdict
import logging
import os
import qualysapi
from lxml import objectify

#
#  Begin
#
# Declare the command line flags/options we want to allow.
parser = argparse.ArgumentParser(description = 'Parse QualysGuard VM map XML for live but not scannable IPs.')
parser.add_argument('-v', '--debug', action = 'store_true',
                    help = 'Outputs additional information to log.')
parser.add_argument('--config',
                    help = 'Configuration for Qualys connector.')
# Parse arguments.
args = parser.parse_args()# Create log directory.
# Validate input.
if not (args.map or \
        args.subscribe_from_csv):
    parser.print_help()
    exit()
# Create log directory.
PATH_LOG = 'log'
if not os.path.exists(PATH_LOG):
    os.makedirs(PATH_LOG)
# Set log options.
LOG_FILENAME = '%s/%s-%s.log' % (PATH_LOG,
                                __file__,
                                datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S'))
# Make a global logging object.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# This handler writes everything to a file.
logger_file = logging.FileHandler(LOG_FILENAME)
logger_file.setFormatter(logging.Formatter("%(asctime)s %(name)-12s %(levelname)s %(funcName)s %(lineno)d %(message)s"))
logger_file.setLevel(logging.INFO)
if c_args.verbose:
    logger_file.setLevel(logging.DEBUG)
logger.addHandler(logger_file)
# This handler prints to screen.
logger_console = logging.StreamHandler(sys.stdout)
logger_console.setLevel(logging.ERROR)
logger.addHandler(logger_console)
#
# Read in XML map.
with open(args.map) as xml_file:
    xml_output = xml_file.read()
tree = objectify.fromstring(xml_output)
# Find live, not scannable IPs.
count = 0
subscribe_me = set()
if c_args.config:
    qgc = qualysapi.connect(c_args.config)
else:
    qgc = qualysapi.connect()
# Combine IPs to comma-delimited string.
formatted_ips_to_subscribe = ','.join(subscribe_me)
# Subscribe IPs.
qgc = qualysapi.connect('asset_ip.php',{'action': 'add', 'host_ips': formatted_ips_to_subscribe})
exit()

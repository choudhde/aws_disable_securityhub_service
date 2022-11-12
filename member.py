####
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
####
__author__ = 'dc'

import boto3
import sys
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

# Disable Sechub
def disable_sechub(session, region):
    print("Disable Sechub")
    shub_client = session.client('securityhub', region_name=region)
    response = shub_client.disable_security_hub()
    print(response)
    print("#" * 50)


# #############################
# Main Function
# #############################
def main():
    parser =argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', help="AWS profile name is required")
    args = parser.parse_args()
    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(0)
    if args.profile:
        session = boto3.session.Session(
            profile_name=args.profile
        )
    else:
        session = boto3.session.Session(
            profile_name=None
        )
    client = session.client('ec2', region_name='us-east-1')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    with ThreadPoolExecutor() as executor:
        [executor.submit(disable_sechub, session, region) for region in regions]

if __name__ == '__main__':
    main()
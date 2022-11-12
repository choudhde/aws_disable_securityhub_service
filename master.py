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

DELEGATED_SECHUB_ADMIN = '1234567890'


# ##########################################################
# Enable delegated organization admin account
# ###########################################################
def describe_sechub(session, region):
    try:
        print("#" * 50)
        print(f"Region: {region}")
        print("Disable Delegated Administrator")
        shub_client = session.client('securityhub', region_name=region)
        print("Disable Security hub")
        response = shub_client.disable_security_hub()
        print(response)
        print("#"*50)
    except Exception as err:
        print(err)


# ##########################################################
# Enable delegated organization admin account
# ###########################################################
def disable_delegated_administrator(session, region):
    try:
        shub_client = session.client('securityhub', region_name=region)
        response = shub_client.disable_organization_admin_account(
                        AdminAccountId=DELEGATED_SECHUB_ADMIN
                 )
        print(f"{response}")
    except Exception as err:
        print(err)


# #############################
# Delete IAM role for GDuty
# #############################
def delete_shub_managed_role(client_iam):
    try:
        response = client_iam.delete_service_linked_role(RoleName='AWSServiceRoleForSecurityHub')
        print(response)
    except Exception as err:
        print(err)


# #############################
# Main Function
# #############################
def main():
    """
    Entry point
    :param event:
    :param context:
    :return:
    """
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
    print(f'Number of regions: {len(regions)}')
    with ThreadPoolExecutor() as executor:
        [executor.submit(disable_delegated_administrator, session, region) for region in regions]
    client_iam = session.client('iam')
    delete_shub_managed_role(client_iam)
if __name__ == '__main__':
    main()
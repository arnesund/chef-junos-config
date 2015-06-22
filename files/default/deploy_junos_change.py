#!/usr/bin/env python
# coding: utf-8
#
# Deploy JunOS changes to device using PyEZ
#
import sys
import logging
import argparse
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *

# Main function
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    #
    # Do template-based config changes
    #

    # Open connection
    logging.info('Opening connection to {0} as {1}...'.format(args.host, args.user))
    dev = Device(args.host, user=args.user)
    try:
        dev.open()
    except Exception as err:
        logging.error('Unable to connect to device {0},'.format(args.host) + \
            ' aborting! Error: {0}'.format(err))
        return False

    # Bind config object to device
    conf = Config(dev)

    # Parse options for config template, if present
    if args.data:
        data = json.loads(args.data)
    else:
        data = {}

    # Lock configuration to make sure noone else alter it at the same time
    try:
        conf.lock()
    except LockError:
        logging.error('Unable to lock configuration! Aborting.')
        dev.close()
        return False

    # Push template-based change to device
    logging.info('Pushing configuration change to device {0}...'.format(args.host))
    try:
        conf.load(template_path=args.templatefile, template_vars=data)
    except ValueError as err:
        logging.error('Error when pushing configuration change: ' + \
            '{0}'.format(err.message))
    except Exception as err:
        if err.rsp.find('.//ok') is None:
            rpc_msg = err.rsp.findtext('.//error-message')
            logging.error('Unable to load configuration changes on device: ' + \
                '{0}'.format(rpc_msg))
        else:
            logging.error('Unable to load configuration changes on device.')

        # Close device and return failure
        dev.close()
        return False

    # Commit changes to device
    try:
        conf.commit()
    except CommitError:
        logging.error('Unable to commit configuration!')
        dev.close()
        return False

    # Unlock configuration after change
    try:
        conf.unlock()
    except UnlockError:
        logging.error('Unable to unlock configuration, exiting.')
        dev.close()

    # Return success
    logging.info('Finished configuration change of {0} successfully.'.format(args.host))
    return True

 

if __name__ == '__main__':
    # Initialize argument parser and specify valid arguments
    parser = argparse.ArgumentParser( 
                description = "Push configuration changes to Juniper devices using NETCONF.",
                epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                fromfile_prefix_chars = '@' )
    parser.add_argument(
                "--host",
                help = "Hostname/IP address of device (required)",
                required = True,
                metavar = "HOST")
    parser.add_argument(
                "-u",
                "--user",
                help = "Username for authentication to device (required)",
                required = True,
                metavar = "USER")
    parser.add_argument(
                "-f",
                "--templatefile",
                help = "Filename of config snippet/template to push to device",
                required = True,
                metavar = "FILENAME")
    parser.add_argument(
                "-d",
                "--data",
                help = "JSON dictionary of variables to fill config template with (optional)",
                metavar = "DATA")
    parser.add_argument(
                "-v",
                "--verbose",
                help="Increase output verbosity",
                action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # Call main function, check return code (True/False) to set correct exit code
    res = main(args, loglevel)
    if not res:
        sys.exit(1)

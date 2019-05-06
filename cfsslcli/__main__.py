#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

import cfssl
import click

from cfsslcli import __version__, writer, checksums, configuration

if 'REQUESTS_CA_BUNDLE' not in os.environ:
    if os.environ.get('SSL_CERT_FILE'):
        os.environ['REQUESTS_CA_BUNDLE'] = os.environ.get('SSL_CERT_FILE')
    elif os.environ.get('NODE_EXTRA_CA_CERTS'):
        os.environ['REQUESTS_CA_BUNDLE'] = os.environ.get('NODE_EXTRA_CA_CERTS')


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(prog_name='cfssl', version=__version__)
def greet():
    pass


@greet.command(help='Generate certificate files')
@click.argument('domain', required=False)
@click.option('-n', '--common-name', help='The fully qualified domain name of the certificate')
@click.option('-h', '--host', multiple=True, help='Add hosts to the certificate')
@click.option('-c', '--config', help='Path to configuration file')
@click.option('--der', is_flag=True, help='Generates DER files')
@click.option('--csr', is_flag=True, help='Generates Certificate Request files')
@click.option('-s', '--stdout', is_flag=True, help='Display certificates on screen')
@click.option('-o', '--output', default=None, help='Write output to files of given base name')
@click.option('-d', '--destination', default=None, help='Write output files to given directory')
def gencert(common_name, host, config, der, csr, output, stdout, destination, domain):
    conf = configuration.load(config)
    client = cfssl.CFSSL(**conf['cfssl'])

    if domain:
        common_name = domain if not common_name else common_name
        host = host + (domain, "*.%s" % domain)
        output = domain if not output else output

    if not output:
        output = common_name

    if not output:
        output = 'output'

    if not common_name:
        raise click.exceptions.ClickException("At least [domain] argument or [--common-name] option should be defined.")

    if not host:
        host = host + (common_name,)

    request = configuration.new_certificate_request(conf.get('certificate_request', {}))
    if common_name:
        request.common_name = common_name
    if host:
        request.hosts = host

    response = client.new_cert(request)

    checksums.validate_checksums(response)

    if output:
        writer.write_files(response, output, der, csr, conf.get('writer'), destination,
                           conf.get('append_ca_certificate'), client)
    if not output or stdout:
        writer.write_stdout(response, der, csr,
                            conf.get('append_ca_certificate'), client)


def main():
    greet(sys.argv[1:])


if __name__ == '__main__':
    main()

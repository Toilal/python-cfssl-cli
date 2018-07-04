#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import click
import cfssl

from cfsslcli import __version__, writer, checksums, configuration


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(prog_name='cfssl', version=__version__)
def greet():
    pass


@greet.command(help='Generate a private/public key pair certificate')
@click.option('-n', '--common-name', help='The fully qualified domain name of the certificate')
@click.option('-h', '--host', multiple=True, help='Add hosts to the certificate')
@click.option('-c', '--config', default="cfssl.yml", help='Path to configuration file')
@click.option('-d', '--der', is_flag=True, help='Generates DER files')
@click.option('-s', '--stdout', is_flag=True, help='Display certificates on screen')
@click.option('-o', '--output', default="output", help='Write output to files of given base name')
def gencert(common_name, host, config, output, stdout, der):
    conf = configuration.load(config)
    client = cfssl.CFSSL(**conf['cfssl'])

    request = configuration.new_certificate_request(conf.get('certificate_request', {}))
    if common_name:
        request.common_name = common_name
    if host:
        request.hosts = host

    response = client.new_cert(request)

    checksums.validate_checksums(response)

    if output:
        writer.write_files(response, output, der, conf.get('writer', {}))
    if not output or stdout:
        writer.write_stdout(response, der, conf.get('writer', {}))


def main():
    greet(sys.argv[1:])


if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
from os.path import normpath, expanduser, expandvars, join

from cfsslcli.checksums import validate_checksum
from cfsslcli.configuration import find_configuration
from cfsslcli.crypto import convert_pem_to_der

log = logging.getLogger(__name__)


def _write_file(path, binary, destination=None):
    if destination:
        path = join(normpath(expandvars(expanduser(destination))), path)
    log.info('Writing file: %s' % path)
    with open(path, 'wb') as stream:
        stream.write(binary)


def write_files(response, output, der, csr, conf=None, destination=None, append_ca_certificate=False, client=None):
    """
    Write files contained in response.

    :param response:
    :param output:
    :type output: str
    :param der:
    :param csr:
    :param conf:
    :param append_ca_certificate:
    :param destination:
    :param client:
    """
    if not conf:
        conf = {}

    certificate_der = None
    certificate_request_der = None

    should_verify_certificate_der = True

    filenames = conf.get('filenames', {})
    if not destination:
        destination = conf.get('destination')

    if 'private_key' in response:
        private_key = response['private_key'].encode('ascii')
        _write_file(filenames.get('private_key', '%s.key.pem') % output, private_key, destination=destination)
    if 'certificate' in response:
        certificate = response['certificate'].encode('ascii')
        certificate_der = convert_pem_to_der('certificate', certificate)
        validate_checksum('certificate', certificate_der, response['sums']['certificate'], True)

        if conf.get('append_ca_certificate') and client:
            info = client.info('')

            ca = info['certificate'] + '\n'

            certificate += ca.encode('ascii')
            certificate_der = convert_pem_to_der('certificate', certificate)
            should_verify_certificate_der = False

        _write_file(filenames.get('certificate', '%s.pem') % output, certificate, destination=destination)
    if csr and 'certificate_request' in response:
        certificate_request_der = convert_pem_to_der('certificate_request',
                                                     response['certificate_request'].encode('ascii'))
        validate_checksum('certificate_request', certificate_request_der, response['sums']['certificate_request'], True)
        _write_file(filenames.get('certificate_request', '%s.csr.pem') % output,
                    response['certificate_request'].encode('ascii'),
                    destination=destination),

    if der:
        if 'certificate' in response:
            _write_file(filenames.get('certificate_der', '%s.der') % output, certificate_der, destination=destination)
            if should_verify_certificate_der:
                with open(filenames.get('certificate_der', '%s.der') % output, 'rb') as der_file:
                    content = der_file.read()
                    validate_checksum('certificate', content, response['sums']['certificate'], True)
        if csr and 'certificate_request' in response:
            _write_file(filenames.get('certificate_request_der', '%s.csr.der') % output, certificate_request_der, 
                        destination=destination)
            with open(filenames.get('certificate_request_der', '%s.csr.der') % output, 'rb') as der_file:
                content = der_file.read()
                validate_checksum('certificate_request', content, response['sums']['certificate_request'], True)


def write_stdout(response, der, csr, append_ca_certificate, client=None):
    if 'private_key' in response:
        print(response['private_key'])
    if 'certificate' in response:
        print(response['certificate'])

        if append_ca_certificate and client:
            info = client.info('')
            ca = info['certificate'] + '\n'
            print(ca)

    if 'certificate_request' in response:
        print(response['certificate_request'])

    if der:
        if 'certificate' in response:
            print(convert_pem_to_der('certificate', response['certificate']))
        if csr and 'certificate_request' in response:
            print(convert_pem_to_der('certificate_request', response['certificate_request']))


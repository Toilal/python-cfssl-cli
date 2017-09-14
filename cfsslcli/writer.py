#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from cfsslcli.checksums import validate_checksum
from cfsslcli.crypto import convert_pem_to_der

import logging

log = logging.getLogger(__name__)


def write_files(response, output, der):
    """
    Write files contained in response.

    :param response:
    :param output:
    :type output: str
    """
    certificate_der = None
    certificate_request_der = None
    if 'private_key' in response:
        _write_file('%s.key.pem' % output, response['private_key'].encode('ascii'))
    if 'certificate' in response:
        certificate_der = convert_pem_to_der('certificate', response['certificate'].encode('ascii'))
        validate_checksum('certificate', certificate_der, response['sums']['certificate'], True)
        _write_file('%s.pem' % output, response['certificate'].encode('ascii'))
    if 'certificate_request' in response:
        certificate_request_der = convert_pem_to_der('certificate_request', response['certificate_request'].encode('ascii'))
        validate_checksum('certificate_request', certificate_request_der, response['sums']['certificate_request'], True)
        _write_file('%s.csr.pem' % output, response['certificate_request'].encode('ascii'))

    if der:
        if 'certificate' in response:
            _write_file('%s.der' % output, certificate_der)
            with open('%s.der' % output, 'rb') as der_file:
                content = der_file.read()
                validate_checksum('certificate', content, response['sums']['certificate'], True)
        if 'certificate_request' in response:
            _write_file('%s.csr.der' % output, certificate_request_der)
            with open('%s.csr.der' % output, 'rb') as der_file:
                content = der_file.read()
                validate_checksum('certificate_request', content, response['sums']['certificate_request'], True)


def _write_file(path, binary):
    log.info('Writing file: %s' % path)
    with open(path, 'wb') as stream:
        stream.write(binary)


def write_stdout(response, der):
    if 'private_key' in response:
        print(response['private_key'])
    if 'certificate' in response:
        print(response['certificate'])
    if 'certificate_request' in response:
        print(response['certificate_request'])

    if der:
        if 'certificate' in response:
            print(convert_pem_to_der('certificate', response['certificate']))
        if 'certificate_request' in response:
            print(convert_pem_to_der('certificate_request', response['certificate_request']))

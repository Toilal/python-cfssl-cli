#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import hashlib
from .crypto import convert_pem_to_der


def validate_checksums(response):
    """
    Validate checksums from certificate request response

    :param response:
    :return:
    """
    sums = response.get('sums', {})
    for part, content in response.items():
        if part != 'sums' and part != 'private_key':
            sums_item = sums.get(part)
            if not sums_item:
                log.warning('No checksum data for %s' % part)
            else:
                validate_checksum(part, content.encode('ascii'), sums_item)


def validate_checksum(part, content, sums_item, content_is_der=False):
    """
    Validate a checksum from certificate sums and content

    :param part:
    :param content:
    :param sums_item:
    :param content_is_der:
    :return:
    """
    for algo, checksum in sums_item.items():
        validate_checksum_algo(part, content, algo, checksum, content_is_der)


def validate_checksum_algo(part, content, algo, checksum, content_is_der=False):
    """
    Validate a checksum using content, algo and checksum.

    :param part:
    :param content:
    :param algo:
    :param checksum:
    :param content_is_der:
    :return:
    """
    if not content_is_der:
        content = convert_pem_to_der(part, content)

    validated_checksum = getattr(hashlib, algo.replace('-', ''))(content).hexdigest()
    checksum = checksum.lower()
    if validated_checksum != checksum:
        raise IOError("Invalid %s %s checksum (%s): %s != %s ", part, algo, checksum, validated_checksum)
    else:
        log.debug("Checksum validated: %s (%s)" % (part, algo))

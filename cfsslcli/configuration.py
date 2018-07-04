#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import cfssl


def load(configuration):
    """
    Load the configuration

    :param configuration:
    :return:
    """
    with open(configuration, 'r') as stream:
        return yaml.load(stream)


def _load_configuration_property(certificate_request, configuration, key, value):
    if not value:
        try:
            value = configuration[key]
        except KeyError:
            pass

    if value:
        setattr(certificate_request, 'common_name', value)


def new_certificate_request(configuration, common_name=None, hosts=None):
    """
    Creates a CertificateRequest based on configuration

    :param configuration:
    :param common_name:
    :return:
    """
    certificate_request = cfssl.CertificateRequest()

    _load_configuration_property(certificate_request, configuration, 'common_name', common_name)
    _load_configuration_property(certificate_request, configuration, 'hosts', hosts)

    return certificate_request

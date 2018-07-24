#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import cfssl
import os


def load(configuration):
    """
    Load the configuration

    :param configuration:
    :return:
    """
    if configuration and os.path.exists(configuration):
        with open(configuration, 'r') as stream:
            return yaml.load(stream)
    else:
        raise FileNotFoundError('Can\'t find configuration file: %s' % configuration)


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

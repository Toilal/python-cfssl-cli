#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import cfssl
import os
import pkg_resources

from os.path import expanduser, normpath


def load(configuration):
    """
    Load the configuration

    :param configuration:
    :return:
    """
    if configuration:
        configuration = normpath(expanduser(configuration))

    if not configuration or not os.path.exists(configuration):
        configuration = normpath(expanduser("~/.cfssl-cli/config.yml"))

    if not os.path.exists(configuration):
        default_config_content = pkg_resources.resource_string(__name__, 'config/config.yml')
        os.makedirs(os.path.dirname(configuration), exist_ok=True)
        with open(configuration, 'wb') as stream:
            stream.write(default_config_content)
        default_chain_content = pkg_resources.resource_string(__name__, 'config/chain.pem')
        chain = normpath(expanduser("~/.cfssl-cli/chain.pem"))
        with open(chain, 'wb') as stream:
            stream.write(default_chain_content)

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

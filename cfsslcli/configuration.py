#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os.path import expanduser, expandvars, normpath, join, dirname, exists

import cfssl
import pkg_resources
import yaml


def load(configuration):
    """
    Load the configuration

    :param configuration:
    :return:
    """
    configuration = find_configuration(configuration)
    if configuration and not exists(configuration):
        write_default_configuration(configuration)

    if configuration and exists(configuration):
        with open(configuration, 'r') as stream:
            loaded = yaml.load(stream)
            loaded['__configuration__'] = configuration
            if 'writer' in loaded:
                loaded['writer']['__configuration__'] = configuration
            return loaded
    else:
        raise FileNotFoundError('Can\'t find configuration file: %s' % configuration)


def find_configuration(configuration):
    """
    Find the configuration filepath.

    :param configuration:
    :param write_default_if_not_exists: 
    :return:
    """
    if configuration:
        configuration = normpath(expandvars(expanduser(configuration)))
        return configuration

    home = os.environ.get('CFSSL_CLI_HOME', join('~', '.cfssl-cli'))
    if not configuration or not exists(configuration):
        configuration = normpath(expandvars(expanduser('cfssl-cli.yml')))

    if not configuration or not exists(configuration):
        configuration = normpath(expandvars(expanduser(join('.cfssl-cli', 'config.yml'))))

    if not configuration or not exists(configuration):
        configuration = normpath(expandvars(expanduser(join(home, 'config.yml'))))

    return configuration


def find_writer_chain(configuration, chain):
    chain = normpath(expandvars(expanduser(chain)))
    dirs = dirname(configuration)
    if configuration and dirs:
        try:
            chain = join(dirs, chain)
        except ValueError:
            pass
    return chain


def write_default_configuration(configuration):
    default_config_content = pkg_resources.resource_string(__name__, 'config/config.yml')
    dirs = dirname(configuration)
    if dirs:
        os.makedirs(dirs, exist_ok=True)
    with open(configuration, 'wb') as stream:
        stream.write(default_config_content)
    default_config_yaml = yaml.load(default_config_content)
    if 'writer' in default_config_yaml and default_config_yaml['writer'].get('chain'):
        write_default_writer_chain(configuration, default_config_yaml['writer'].get('chain'))


def write_default_writer_chain(configuration, chain):
    default_chain_content = pkg_resources.resource_string(__name__, 'config/chain.pem')
    chain = find_writer_chain(configuration, chain)
    with open(chain, 'wb') as stream:
        stream.write(default_chain_content)


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

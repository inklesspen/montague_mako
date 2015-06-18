from __future__ import absolute_import

import os
from montague.loadwsgi import Loader
from montague_toml.toml import TOMLConfigLoader
import mock
import pytest

here = os.path.dirname(__file__)


@pytest.yield_fixture
def mockenv():
    mocked = {}
    patcher = mock.patch('os.environ', mocked)
    patcher.start()
    yield mocked
    patcher.stop()


def test_read_config(mockenv):
    mockenv['foo'] = 'bar'
    path = os.path.join(here, 'config.toml.mako')
    expected = {
        'globals': {},
        'application': {
            'main': {
                'use': 'package:montague_testapps#basic_app',
                'path_info': [here, path],
                'env_val': 'bar',
            },
            'egg': {'use': 'egg:montague_testapps#other'},
            'filtered-app': {
                'filter-with': 'filter',
                'use': 'package:montague_testapps#basic_app',
            },
        },
        'composite': {},
        'filter': {
            'filter': {
                'use': 'egg:montague_testapps#caps',
                'method_to_call': 'lower',
            },
        },
        'server': {
            'server_factory': {
                'use': 'egg:montague_testapps#server_factory',
                'port': 42,
            },
            'server_runner': {
                'use': 'egg:montague_testapps#server_runner',
                'host': '127.0.0.1',
            },
        },
        'logging': {
        }
    }
    path = os.path.join(here, 'config.toml.mako')
    loader = Loader(path)
    assert isinstance(loader.config_loader, TOMLConfigLoader)
    actual = loader.config_loader.config()
    assert actual == expected

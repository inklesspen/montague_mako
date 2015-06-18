from __future__ import absolute_import

import os
from mako.template import Template
import tempfile
from montague.loadwsgi import Loader


def mako_config_loader(path):
    new_name, old_ext = os.path.splitext(os.path.basename(path))
    if old_ext != '.mako':
        raise ValueError('{0} does not end in .mako; how did you get here?'.format(path))
    template = Template(filename=path, output_encoding='utf-8')
    data = {
        'environ': os.environ,
        'here': os.path.dirname(path),
        '__file__': path,
    }

    # delete=False means it will not be automatically cleaned up
    # but we have no way of knowing when it will be read from, so it needs to stick around
    with tempfile.NamedTemporaryFile(suffix=new_name, delete=False) as outfile:
        output = template.render(**data)
        outfile.write(output)
        outfile.flush()
        return Loader(outfile.name).config_loader

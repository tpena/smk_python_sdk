#!/usr/bin/env python
# Copyright (C) 2011 Smarkets Limited <support@smarkets.com>
#
# This module is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php
import glob
import os
import re
import shutil
import subprocess
import sys

from os.path import abspath, dirname, join


PROJECT_ROOT = abspath(dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from distutils.spawn import find_executable
from distutils.command import clean, build
from setuptools import setup
from itertools import chain


def check_call(*args, **kwargs):
    print('Calling %s, %s' % (args, kwargs,))
    subprocess.check_call(*args, **kwargs)


ETO_PIQI_URL = 'https://raw.github.com/smarkets/eto_common/v0.3.0/eto.piqi'
SETO_PIQI_URL = 'https://raw.github.com/smarkets/smk_api_common/v0.7.5/seto.piqi'


def _safe_glob(pathname):
    "Do a safe version of glob which copes with win32"
    is_win32 = sys.platform == 'win32'
    for source in glob.glob(pathname):
        yield source.replace('/', '\\') if is_win32 else source


class SmarketsProtocolBuild(build.build):

    "Class to build the protobuf output"

    description = "build the protocol buffer output with protobuf-compiler"

    def find(self, name):
        result = find_executable(name)
        if result is None:
            raise Exception("*** Cannot find %s; make sure it's installed" % (name,))
        return result

    def run(self):
        "Get the .piqi definitions and run the 'protoc' compiler command"

        eto_piqi = join(PROJECT_ROOT, 'eto.piqi')
        if not os.path.exists(eto_piqi):
            check_call((self.find('curl'), '-o', eto_piqi, ETO_PIQI_URL))

        seto_piqi = join(PROJECT_ROOT, 'seto.piqi')
        if not os.path.exists(seto_piqi):
            check_call((self.find('curl'), '-o', seto_piqi, SETO_PIQI_URL))

        eto_proto = join(PROJECT_ROOT, 'smarkets.eto.piqi.proto')
        if not os.path.exists(eto_proto):
            check_call((self.find('piqi'), 'to-proto', eto_piqi, '-o', eto_proto))

        seto_proto = join(PROJECT_ROOT, 'smarkets.seto.piqi.proto')
        if not os.path.exists(seto_proto):
            check_call((self.find('piqi'), 'to-proto', seto_piqi, '-o', seto_proto))
            self.replace_file(seto_proto, self.fix_import)

        for pkg in ('eto', 'seto'):
            pkg_dir = join(PROJECT_ROOT, 'smarkets', pkg)
            init_file = join(pkg_dir, '__init__.py')

            if not os.path.exists(init_file):
                check_call((self.find('protoc'), '--python_out=.', 'smarkets.%s.piqi.proto' % (pkg,)))

            with open(init_file, 'w') as initf:
                initf.write(""""Protocol-buffers generated package"
# Copyright (C) 2011 Smarkets Limited <support@smarkets.com>
#
# This module is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php
""")

        build.build.run(self)

    @staticmethod
    def replace_file(filename, line_map):
        "Map line_map for each line in filename"
        with open(filename, "r") as sources:
            lines = sources.readlines()
        with open(filename, "w") as sources:
            for line in lines:
                sources.write(line_map(line))

    @staticmethod
    def fix_import(line):
        "Fix the import line in smarkets.seto.piqi.proto"
        return re.sub(
            r'import "eto\.piqi\.proto"',
            'import "smarkets.eto.piqi.proto"',
            line)


class SmarketsProtocolClean(clean.clean):

    """Class to clean up the built protobuf files."""

    description = "clean up files generated by protobuf-compiler"

    def run(self):
        """Do the clean up"""
        for src_dir in [
            join('build', 'pb'),
            join('smarkets', 'eto'),
            join('smarkets', 'seto'),
        ]:
            src_dir = join(PROJECT_ROOT, src_dir)
            if os.path.exists(src_dir):
                shutil.rmtree(src_dir)
        for filename in chain(
                _safe_glob('*.proto'),
                _safe_glob('*.piqi')):
            if os.path.exists(filename):
                os.unlink(filename)

        # Call the parent class clean command
        clean.clean.run(self)

readme_path = join(PROJECT_ROOT, 'README.md')

with open(readme_path) as f:
    long_description = f.read()


# this is not ideal but at at least we're not repeating ourselved when updating package version

with open(join(PROJECT_ROOT, 'smarkets', '__init__.py')) as f:
    version_line = [line for line in f if line.startswith('__version__')][0]

__version__ = version_line.split('=')[1].strip().strip("'").strip('"')

# smarkets.eto and smarkets.eto in packages break creating source dists in current setup
# also nasty hack to make it buildable on readthedocs.org
if 'sdist' in sys.argv or 'READTHEDOCS' in os.environ:
    extra_packages = []
else:
    extra_packages = ['smarkets.eto', 'smarkets.seto']

sdict = {
    'name': 'smk_python_sdk',
    'version': __version__,
    'description': 'Python client for Smarkets streaming API',
    'long_description': long_description,
    'url': 'https://github.com/smarkets/smk_python_sdk',
    'download_url': 'https://github.com/smarkets/smk_python_sdk/downloads/smk_python_sdk-%s.tar.gz' % __version__,
    'author': 'Smarkets Limited',
    'author_email': 'support@smarkets.com',
    'maintainer': 'Smarkets Limited',
    'maintainer_email': 'support@smarkets.com',
    'keywords': ['Smarkets', 'betting exchange'],
    'license': 'MIT',
    'packages': ['smarkets'] + extra_packages,
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
    'install_requires': [
        'protobuf',
        'six',
    ],
    'zip_safe': False,
    'cmdclass': {
        'build': SmarketsProtocolBuild,
        'clean': SmarketsProtocolClean,
    },
}

if __name__ == '__main__':
    setup(**sdict)

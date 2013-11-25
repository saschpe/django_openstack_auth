import os
import re
import codecs
from setuptools import setup, find_packages


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def parse_requirements(requirements_file='requirements.txt'):
    requirements = []
    with open(requirements_file, 'r') as f:
        for line in f:
            # For the requirements list, we need to inject only the portion
            # after egg= so that distutils knows the package it's looking for
            # such as:
            # -e git://github.com/openstack/nova/master#egg=nova
            if re.match(r'\s*-e\s+', line):
                requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',
                                    line))
            # such as:
            # http://github.com/openstack/nova/zipball/master#egg=nova
            elif re.match(r'\s*https?:', line):
                requirements.append(re.sub(r'\s*https?:.*#egg=(.*)$', r'\1',
                                    line))
            # -f lines are for index locations, and don't get used here
            elif re.match(r'\s*-f\s+', line):
                pass
            # -r lines are for including other files, and don't get used here
            elif re.match(r'\s*-r\s+', line):
                pass
            # argparse is part of the standard library starting with 2.7
            # adding it to the requirements list screws distro installs
            elif line == 'argparse' and sys.version_info >= (2, 7):
                pass
            else:
                requirements.append(line.strip())
    return requirements


install_requires = parse_requirements("requirements.txt")
tests_requires = parse_requirements("test-requirements.txt")


setup(
    name="django_openstack_auth",
    version=find_version("openstack_auth", "__init__.py"),
    url='http://django_openstack_auth.readthedocs.org/',
    license='BSD',
    description=("A Django authentication backend for use with the "
                 "OpenStack Keystone Identity backend."),
    long_description=read('README.rst'),
    author='Gabriel Hurley',
    author_email='gabriel@strikeawe.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_requires,
    test_suite='openstack_auth.tests.run_tests.run'
)

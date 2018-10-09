import os
from setuptools import setup


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])

    return {package: filepaths}


setup(
    name="aioscheduler",
    version='0.0.1',
    description="A Thread scheduler to dispatch periodic tasks to other event loops",
    long_description="Visit https://github.com/MattBlack85/aio-scheduler for more information.",
    packages=['aioscheduler'],
    install_requires=[],
    package_data=get_package_data('aioscheduler'),
    python_requires=">=3.6",
)

from setuptools import setup

setup(
    name="aioscheduler",
    version='0.1.0',
    description="A Thread scheduler to dispatch periodic tasks to other event loops",
    long_description="Visit https://github.com/MattBlack85/aio-scheduler for more information.",
    packages=[
        "aioscheduler",
    ],
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
)

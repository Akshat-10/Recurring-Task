from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in task/__init__.py
from task import __version__ as version

setup(
	name="task",
	version=version,
	description="Task Management",
	author="Akshat Gupta",
	author_email="akshatfrappe@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

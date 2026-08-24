from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="helpbot",
	version="0.0.1",
	description="In-site help search: internal workflows + ERPNext official docs references",
	author="Syvasoft Business Solutions",
	author_email="support@syvasoft.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)

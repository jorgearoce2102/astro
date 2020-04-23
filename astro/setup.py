try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Virtual interactive baseball game',
    'author': 'Jorge A. Rodriguez',
    'url': 'https://github.com/jorgearoce2102',
    'download_url': 'https://github.com/jorgearoce2102',
    'author_email': 'alejandro_rdzcelis@hotmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['astro'],
    'name':'Astro Game',
    'scripts': []
}
setup(**config)

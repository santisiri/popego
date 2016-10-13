try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='utils',
    version="0.2",
    description='Utils Library',
    author='Popego Team',
    #author_email='',
    url='',
    install_requires= [],
    packages=find_packages(exclude=['test', 'test.*']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'popserver': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'popserver': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points=""""""
)

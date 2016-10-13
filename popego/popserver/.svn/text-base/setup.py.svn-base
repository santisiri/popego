try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='popserver',
    version="0.1",
    description='Server de Popego',
    author='Popego Team',
    #author_email='',
    url='http://www.popego.com',
    install_requires= [
      "Pylons>=0.9.6.1",
      "docutils==0.4",
      "SQLAlchemy==0.4.3",
      "Elixir==0.5.1",
      "AuthKit==0.4.0",
      "BeautifulSoup",
      "pmock",
      "feedparser"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'popserver': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'popserver': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = popserver.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)

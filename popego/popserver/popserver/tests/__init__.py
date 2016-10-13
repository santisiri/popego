# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
"""Pylons application test package

When the test runner finds and executes tests within this directory,
this file will be loaded to setup the test environment.

It registers the root directory of the project in sys.path and
pkg_resources, in case the project hasn't been installed with
setuptools. It also initializes the application via websetup (paster
setup-app) with the project's test.ini configuration file.
"""
import os
import sys
import unittest

import pkg_resources
import paste.fixture
import paste.script.appinstall

import elixir

from paste.deploy import loadapp
from routes import url_for

__all__ = ['url_for', 'TestController', 'TestModel','dbfixture']

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(os.path.dirname(here_dir))

sys.path.insert(0, conf_dir)
pkg_resources.working_set.add_entry(conf_dir)
pkg_resources.require('Paste')
pkg_resources.require('PasteScript')

test_file = os.path.join(conf_dir, 'test.ini')
cmd = paste.script.appinstall.SetupCommand('setup-app')
cmd.run([test_file])

from fixture import DataTestCase, SQLAlchemyFixture
from fixture.style import TrimmedNameStyle
from popserver.model import *

from scripts.migrate import Migrate

dbfixture = SQLAlchemyFixture(env = globals(), 
                              style = TrimmedNameStyle(suffix = 'Data'),
                              scoped_session = dbsession)

class TestModel(unittest.TestCase):
    
    def setUp(self):
        Migrate(['test.ini', '-r', '1'], conf_dir).run()
        Migrate(['test.ini'], conf_dir).run()
        # TODO - refactor to a new method
        elixir.metadata.bind.connect().execute(""" \
         INSERT INTO profileconfig VALUES (1, 1.0, 0.5, 1.0, 1.0); 
         INSERT INTO globalconfig VALUES('current_profile_config', '1');
        """)


    def tearDown(self):
        self._deleteAllData()
        Migrate(['test.ini', '-r', '1'], conf_dir).run()
        dbsession.remove()

    def _deleteAllData(self):
        elixir.metadata.bind.connect().execute("""\
                DELETE FROM  profileconfig;
                DELETE FROM  globalconfig;
                DELETE FROM  videothumbnails;
                DELETE FROM  tags_items;
                DELETE FROM  tags_useritems;
                DELETE FROM  itemgroups_items;
                DELETE FROM  tagcounts;
                DELETE FROM  compatibility;
                DELETE FROM  tags;
                DELETE FROM  feedback;
                DELETE FROM  users_roles;
                DELETE FROM  roles;

                DELETE FROM  bookmarks;
                DELETE FROM  photos;
                DELETE FROM  songs;
                DELETE FROM  videos;
                DELETE FROM  artists;

                DELETE FROM  user_items;
                DELETE FROM  itemgroups;
                DELETE FROM  accounts;

                DELETE FROM  items;
                DELETE FROM  services;
                DELETE FROM  service_types;

                DELETE FROM  users;
                DELETE FROM  groups;
                DELETE FROM  countries;
        """)
        
import pylons
import popserver

class TestController(TestModel):

    def __init__(self, *args):
        self.wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = paste.fixture.TestApp(self.wsgiapp)
        self.app.extra_environ['REMOTE_ADDR'] = '127.0.0.1' # Hack needed for testing things like AuthKit

        TestModel.__init__(self, *args)

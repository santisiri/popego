#!/usr/bin/env python

"""This is a script to apply database migrations.

Run this script with the -h flag to get usage information.

Migration Modules
-----------------

Each migration is a module stored in
``${appname}/db/migration_${revision}.py`` where revision starts at 000
(i.e. an empty database).  Each such module should have a module-level
global named migration containing a list of pairs of atoms.  For
instance::

    migration = [
        # (up, down)
        ("CREATE TABLE A(...)", "DROP TABLE IF EXISTS A"),
        ("CREATE TABLE B(...)", "DROP TABLE IF EXISTS B")
    ]

The up and down atoms may either be SQL strings, or they may be
functions that accept a SQLAlchemy connection.

Since I'm using SQLAlchemy, you might wonder why I'm writing actual SQL.
I like to use the SQLAlchemy ORM.  However, when creating tables in
MySQL, there are so many fancy options that I find it easier to write
the SQL by hand.

Error Handling
--------------

 * If something goes wrong when down migrating, just let the exception
   propagate.
 
 * If something goes wrong when up migrating, complain, try to back it
   out, and then let the exception propagate.  If backing it out fails, 
   just let that exception propagate.
 
 * Use transactions as appropriate.  There are a lot of cases in
   MySQL where transactions aren't supported.  Hence, backing things
   out is sometimes necessary.  However, it's also possible that a
   transaction might rollback, and then the code to back things out
   runs anyway.  It's best to make your down atoms idempotent.  For
   instance, use "DROP TABLE IF EXISTS" rather than just "DROP
   TABLE".
   
Avoiding SQLAlchemy, Pylons, Paste, and Python 2.5
--------------------------------------------------

I'm using SQLAlchemy, but that doesn't force you to use SQLAlchemy in
the rest of your app.  I'm using Paste's configuration mechanism because
that's how my database configuration information is stored.  Passing a
CONFIG.ini to the script meets the needs of Paste and Pylons users
perfectly.  If you're not one of those users and you want to use my
script, it's easy to subclass it and do something differently.
Similarly, if you're not using Python 2.5, I'm happy to remove the
Python 2.5-isms.  Let's talk!

"""

# Copyright: "Shannon -jj Behrens <jjinux@gmail.com>"
# License: I am contributing this code to the Pylons project under the same license as Pylons.

from __future__ import with_statement

from contextlib import contextmanager, closing
from glob import glob
from optparse import OptionParser
import os
import re
import sys
import traceback

from paste.deploy import loadapp
from pylons import config as conf
#from pylons.database import create_engine

import elixir
from popserver.model import *

__docformat__ = "restructuredtext"


class Migrate:

    """This is the main class that runs the migrations."""

    def __init__(self, args=None, conf_file_dir=None):
        """Set everything up, but don't run the migrations.

        args
          This defaults to ``sys.argv[1:]``.

        """
        self.setup_option_parser(args)
        self.conf_file_dir = conf_file_dir

    def setup_option_parser(self, args):
        """Parse command line arguments."""
        self.args = args
        usage = "usage: %prog [options] CONFIG.ini"
        self.parser = OptionParser(usage=usage)
        self.parser.add_option('-r', '--revision', type='int',
                          help='schema revision; defaults to most current')
        self.parser.add_option('-p', '--print-revision', action="store_true",
                               default=False, 
                               help='print current revision and exit')
        self.parser.add_option("-v", "--verbose", action="store_true", 
                               default=False)
        (self.options, self.args) = self.parser.parse_args(self.args)
        if len(self.args) != 1:
            self.parser.error("Expected exactly one argument for CONFIG.ini")

    def run(self):
        """Run the migrations.

        All database activity starts from here.

        """
        self.load_configuration(self.conf_file_dir)
        #self.engine = create_engine()
        #self.engine.echo = bool(self.options.verbose)
        with closing(elixir.metadata.bind.connect()) as self.connection:
            self.find_migration_modules()
            self.find_desired_revision()
            self.find_current_revision()
            if self.options.print_revision:
                print self.current_revision
                return
            self.find_desired_migrations()
            self.print_overview()
            for migration in self.desired_migrations:
                self.apply_migration(migration)

    def load_configuration(self, relative_to=None):
        """Load the configuration."""
        relative_to = os.getcwd() if relative_to is None else relative_to
        try:
            loadapp('config:%s' % self.args[0], relative_to=relative_to)
            self.session = dbsession()
        except OSError, e:
            self.parser.error(str(e))

    def find_migration_modules(self):
        """Figure out what migrations exist.

        They should start at 000.

        """
        package = conf['pylons.package']
        module = __import__(package + '.db', fromlist=['db'])
        dirname = os.path.dirname(module.__file__)
        glob_pattern = os.path.join(dirname, 'migration_*.py')
        files = glob(glob_pattern)
        files.sort()
        basenames = map(os.path.basename, files)
        for (i, name) in enumerate(basenames):
            expected = 'migration_%03d.py' % i
            if name != expected:
                raise ValueError("Expected %s, got %s" % (expected, name))
        self.migration_modules = []
        for name in basenames:
            name = name[:-len('.py')]
            module = __import__('%s.db.%s' % (package, name),
                                fromlist=[name])
            self.migration_modules.append(module)

    def find_desired_revision(self):
        """Find the target revision."""
        len_migration_modules = len(self.migration_modules)
        if self.options.revision is None:
            self.desired_revision = len_migration_modules - 1
        else:
            self.desired_revision = self.options.revision
            if (self.desired_revision < 0 or
                self.desired_revision >= len_migration_modules):
                self.parser.error(
                    "Revision argument out of range [0, %s]" % 
                    (len_migration_modules - 1))

    def find_current_revision(self):
        """Figure out what revision we're currently at."""
        if self.connection.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'revision'").rowcount == 0:
            self.current_revision = 0
        else:
            result = self.connection.execute(
                "SELECT revision_id FROM revision")
            self.current_revision = int(result.fetchone()[0])

    def find_desired_migrations(self):
        """Figure out which migrations need to be applied."""
        self.find_migration_range()
        self.desired_migrations = [
            self.migration_modules[i]
            for i in self.migration_range
        ]

    def find_migration_range(self):

        """Figure out the range of the migrations that need to be applied."""

        if self.current_revision <= self.desired_revision:

            # Don't reapply the current revision.  Do apply the
            # desired revision.

            self.step = 1
            self.migration_range = range(self.current_revision + self.step,
                                         self.desired_revision + self.step)
        else:

            # Unapply the current revision.  Don't unapply the
            # desired revision.

            self.step = -1
            self.migration_range = range(self.current_revision,
                                         self.desired_revision, self.step)

    def print_overview(self):
        """If verbose, tell the user what's going on."""
        if self.options.verbose:
            print "Current revision:", self.current_revision
            print "Desired revision:", self.desired_revision
            print "Direction:", ("up" if self.step == 1 else "down")
            print "Migrations to be applied:", self.migration_range 

    def apply_migration(self, migration):
        """Apply the given migration list.

        migration
          This is a migration module.

        """
        name = migration.__name__
        revision = self.parse_revision(name)

        if self.options.verbose:
            print "Applying migration:", name
        if self.step == -1:
            with self.manage_transaction():
                for (up, down) in reversed(migration.migration):
                    self.apply_atom(down)
                self.record_revision(revision - 1)
        else:
            undo_atoms = []
            try:
                with self.manage_transaction():
                    for (up, down) in migration.migration:
                        self.apply_atom(up)
                        undo_atoms.append(down)
                    self.record_revision(revision)
            except Exception, e:
                print >> sys.stderr, "An exception occurred:"
                traceback.print_exc()
                print >> sys.stderr, "Trying to back out migration:", name
                with self.manage_transaction():
                    for down in reversed(undo_atoms):
                        self.apply_atom(down)
                print >> sys.stderr, "Backed out migration:", name
                print >> sys.stderr, "Re-raising original exception."
                raise

    def apply_atom(self, atom):
        """Apply the given atom.  Let exceptions propagate."""
        if isinstance(atom, basestring):
            self.connection.execute(atom)
        else:
            atom(self.connection)

    def parse_revision(self, s):
        """Given a string, return the revision number embedded in it.

        Raise a ValueError on failure.

        """
        match = re.search('(\d+)', s)
        if match is None:
            raise ValueError("Couldn't find a revision in: %s" % s)
        return int(match.group(0))

    def record_revision(self, revision):
        """Record the given revision.

        The current revision is stored in a table named revision.
        There's nothing to do if revision is 0.

        """
        if revision != 0:
            self.connection.execute("UPDATE revision SET revision_id = %s" % revision)
            self.current_revision = revision

    @contextmanager
    def manage_transaction(self):
        """Manage a database transaction.

        Usage::

            with self.manage_transaction():
                ...

        """
        transaction = self.connection.begin()
        try:
            yield
            transaction.commit()
        except:
            transaction.rollback()
            raise


if __name__ == '__main__':
    Migrate().run()

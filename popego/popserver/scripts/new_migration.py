# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import os
import glob
import re
import sys

here_dir = os.path.dirname(os.path.abspath(__file__))
migrations_dir = os.path.join(here_dir, '..', 'popserver', 'db')

number_capture = re.compile(r'.*migration_(\d{3})\.py$')

# obtener numero de migracion a partir del filename
mig_number = lambda fn: int(number_capture.search(fn).groups()[0])

# lista de migraciones
existing_migrations = glob.glob(migrations_dir + "/migration_[0-9][0-9][0-9].py")
existing_migrations.sort(lambda x,y: cmp(mig_number(x), mig_number(y)))

migration_template = """# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: %03d
# %s

migration = [
    (\"\"\"
        <MIGRATION UP SQL HERE>;
     \"\"\", 
     \"\"\"
        <MIGRATION DOWN SQL HERE>;
     \"\"\"),
]

"""


if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        print "Usage: %s migration_description" % sys.argv[0]
        exit()

    # próxima migration
    next_migration_number = mig_number(existing_migrations[-1]) + 1

    fout = open(os.path.join(migrations_dir, 'migration_%03d.py' % next_migration_number), 'w')
    fout.write(migration_template % (next_migration_number, sys.argv[1]))
    fout.close()

    print 'new migration: db/migration_%03d.py' % next_migration_number



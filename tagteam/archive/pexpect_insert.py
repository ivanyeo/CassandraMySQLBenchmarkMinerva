#!/usr/bin/python

import pexpect

child = pexpect.spawn('python manage.py shell', timeout=None)
child.expect('>>> ')
child.sendline('execfile("insert.py")')

child.expect('>>> ')
child.sendline('exit()')


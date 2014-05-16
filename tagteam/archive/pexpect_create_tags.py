#!/usr/bin/python

import pexpect

child = pexpect.spawn('python manage.py shell', timeout=None)
child.expect('>>> ')
child.sendline('execfile("create_tags.py")')

child.expect('>>> ')
child.sendline('exit()')


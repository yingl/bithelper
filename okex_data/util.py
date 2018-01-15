import atexit
import os
import sys
from requests_threads import AsyncSession
sys.path.append('./')
import database

def daemonize(func, pid_file=None, log_file=None, debug=False):
    if not debug:
        pid = os.fork()
        if pid:
            sys.exit(0)
        os.chdir('/')
        os.umask(0)
        os.setsid()
        _pid = os.fork() # Fork again, the grandson process is daemon process now.
        if _pid:
            sys.exit(0)
        sys.stdout.flush()
        sys.stderr.flush()
        # Close read/write
        with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
            os.dup2(read_null.fileno(), sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(write_null.fileno(), sys.stderr.fileno())
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        # Register exit function to remove pid file
        atexit.register(os.remove, pid_file)
    # Do works
    session = AsyncSession(n=(os.cpu_count() * 2))
    func.session = session
    func.log_file = log_file
    session.run(func)

def write_values(code, price):
    r = database.btc_values()
    r.code = code
    r.price = price
    r.save()

def write_aggs(data, tag):
    r = database.btc_aggs()
    r.data = data
    r.tag = tag
    r.save()

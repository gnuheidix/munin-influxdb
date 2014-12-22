import sys

def progress_bar(current, max, title="Progress", length=50):
    """
    @see http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/13685020#13685020
    """
    percent = float(current) / max
    hashes = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(hashes))
    sys.stdout.write("\r{0}: [{1}] {2}%".format(title, hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()
    if percent >= 1:
        print ""

def parse_handle(handle):
    """
    Parses a connection handle to get it's subparts (user, password, host, port, dbname)
    @return (user, passwd, host, port, dbname)

    @example
        127.0.0.1  -> (None, None, '127.0.0.1', None, None)
        root@localhost  -> ('root', None, 'localhost', None, None)
        root:passwd@localhost  -> ('root', 'passwd', 'localhost', None, None)
        root:passwd@db.example.org:8085  -> ('root', 'passwd', 'db.example.org', '8085', None)
        root@db.example.org:8085/db/test  -> ('root', None, 'db.example.org', '8085', 'test')
        localhost:8085/test  -> (None, None, 'localhost', '8085', 'test')
        root@db.example.org:8085/test  -> ('root', None, 'db.example.org', '8085', 'test')
        root@db.example.org/test  -> ('root', None, 'db.example.org', None, 'test')
    """
    e = handle.split('@')
    user = passwd = host = port = dbname = None

    def parse_dbname(dbname):
        elt = dbname.split("/")
        return elt[0], elt[-1] if len(elt) > 1 else None

    def parse_user(user):
        elt = user.split(":")
        return elt[0], elt[1] if len(elt) == 2 else None

    def parse_host(host):
        elt = host.split(":")
        if len(elt) == 1:
            port = None
            host, dbname = parse_dbname(elt[0])
        elif len(elt) == 2:
            host = elt[0]
            port, dbname = parse_dbname(elt[1])
        return host, port, dbname

    if len(e) == 2:
        user, passwd = parse_user(e[0])
    host, port, dbname = parse_host(e[-1])

    return user, passwd, host, port, dbname
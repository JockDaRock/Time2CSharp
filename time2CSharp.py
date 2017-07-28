import sys
import os
from io import StringIO
import contextlib


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def get_stdin():
    buf = ""
    for line in sys.stdin:
        buf = buf + line
    return buf


if __name__ == "__main__":
    st = get_stdin()
    tmpfold = os.environ["TMPDIR"]
    tmpfile = "%s%s" % (tmpfold, "Program.cs")
    f = open(tmpfile, 'w')
    print(st, file=f)
    f.close()
    os.execlp("dotnet", "", "build")
    with stdoutIO() as s:
        try:
            os.execlp("dotnet", "", "/tmp/bin/Debug/netcoreapp1.1/tmp.dll")
        except BaseException as e:
            print(e)
    print(s.getvalue())

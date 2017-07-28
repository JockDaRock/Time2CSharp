import sys
import os
from io import StringIO
import contextlib
import subprocess


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
    f.write(st)
    f.close()
    os.chdir(tmpfold)
    p1 = subprocess.Popen(["dotnet", "build"], stdout=subprocess.PIPE)
    pLog = p1.stdout.read()

    with stdoutIO() as s:
        try:
            print(subprocess.check_output(["dotnet", "%sbin/Debug/netcoreapp1.1/tmp.dll" % tmpfold]).decode("utf-8"))
        except BaseException as e:
            print(e)
    print(s.getvalue())

from lib import _app2d
from json import loads
import sys


def main():
    func = sys.argv[1]
    param = loads(sys.argv[2])
    output = _app2d["_format"][func](**param)
    sys.stdout.write(str(output))
    sys.stdout.flush()


main()
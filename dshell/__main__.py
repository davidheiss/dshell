from argparse import ArgumentParser

from .app import App
from .version import print_version

argument_parser = ArgumentParser(
    prog="dshell"
)

argument_parser.add_argument(
    "--version",
    action="store_true",
    help="print version and exit"
)

if __name__ == "__main__":
    namespace = argument_parser.parse_args()
    
    if namespace.version:
        print_version()
        exit()

    app = App()
    app.run()

import sys

from hasek.core import MainCommand


def main():
    try:
        MainCommand().run()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()

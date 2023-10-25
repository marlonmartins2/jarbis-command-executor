from io import open

read_version = lambda filename: open(filename, "r", encoding="utf-8").read()

""" It defines the project current version """
try:
    __version__ = read_version(".version").strip()
except FileNotFoundError:
    __version__ = "1.0.0"

if __name__ == "__main__":
    print(__version__)

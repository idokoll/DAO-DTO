import sys

from repository import repo


# import imp
def main():
    repo.create_tables()
    repo.parse_text(sys.argv[1])
    repo.ex_orders(sys.argv[2])

if __name__ == '__main__':
    main()
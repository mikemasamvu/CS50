# TODO
from cs50 import get_int


def main():
    height = get_height()
    for i in range(height):
        # print spaces before hash
        for j in range(height - i - 1):
            print(" ", end="")

        # print hashes
        for j in range(i + 1):
            print("#", end="")
        print()


def get_height():
    # loop till you get the correct range of height
    while True:
        try:
            height = get_int("Enter pyramid height: ")
            if height >= 1 and height <= 8:
                return height
        except ValueError:
            height = get_int("Enter pyramid height: ")


# call main function
main()
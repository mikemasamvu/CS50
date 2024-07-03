# TODO
from cs50 import get_float


def main():
    change = get_change() * 100
    count = 0
    while change >= 1:
        # calculate number of 25 cent coints
        if change >= 25:
            count += int(change / 25)
            change = change % 25
        # calculate number of 10 cent coints
        elif change >= 10 and change < 25:
            count += int(change / 10)
            change = change % 10
        # calculate number of 5 cent coints
        elif change >= 5 and change < 10:
            count += int(change / 5)
            change = change % 5
        # calculate number of 1 cent coints
        else:
            count = count + change
            break
    print(int(count))


def get_change():
    # Get change function
    while True:
        # loop till the user inputs correct change format
        try:
            change = get_float("Change owed: ")
            if change > 0:
                return change
        except ValueError:
            change = get_float("Change owed: ")


main()


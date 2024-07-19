from Another_functions import play

while True:
    play()
    end = input("You will be play more? (Yes or No, if you write somethihg another a will consider it as No):").lower().strip()
    if end == "yes":
        pass
    else:
        break
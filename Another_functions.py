from Class_Field import Field

def choise_complexity() -> str:
        print("Hello, you will be playing minesweeper")
        complexity = input("Now you choose the difficulty (beginner - b, intermediate - in, expert - ex): ").strip()
        while True:
            if complexity.lower() == "b":
                complexity = "Beginner"
                break
            elif complexity.lower() == "in":
                complexity = "Intermediate"
                break
            elif complexity.lower() == "in":
                complexity = "Expert"
                break
            else:
                complexity = input("I'm sorry, I don't understand you, try again (beginner - b, intermediate - in, expert - ex): ").strip()

        return complexity

def play() -> None:
    f = Field(choise_complexity())
    f.move(first_move=True)
    f.mines()
    f.count_near_mines()
    f.open_something("free", "open")
    f.open_something("num", "opened_num")
    while True:
        f.print_field()
        #print("---------------------------------------------------------------------------------------------")
        #f.print_field(False)
        end = f.move()
        f.open_something("free", "open")
        f.open_something("num", "opened_num")
        if end:
            f.print_field()
            print(f"You {end}")
            break

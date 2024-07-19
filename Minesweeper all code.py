from random import randint

class Field:
    def __init__(self, hard) -> None:
        self.hard = hard
        dict_hards = {
            "Beginner" : (9, 9, 10),
            "Intermediate" : (16, 16, 40),
            "Expert" : (30, 16, 99)
        }
        self.L_and_W = dict_hards[hard][:2]
        self.flags = dict_hards[hard][-1]
        values = dict_hards[hard]

        field = [ [Position(0, 0, symbol=" 0", status=" 0")] + [Position(i, 0, symbol=str(i).rjust(2), status=str(i).rjust(2)) for i in range(1, values[0] + 1)] ]
        field[0] = field[0] + [Position(0, 0, symbol=" 0", status=" 0")]
        for Y in range(1, values[1] + 1):
            row = [Position(0, Y, symbol=str(Y).rjust(2), status=str(Y).rjust(2))] + [Position(X, Y, symbol="  ") for X in range(values[0])]
            row = row + [Position(0, Y, symbol=str(Y).rjust(2), status=str(Y).rjust(2))]
            field.append(row)
        field.append(field[0])

        self.field = field

    def mines(self) -> None:
        dict_hards = {
            "Beginner" : (10, 9, 9),
            "Intermediate" : (40, 15, 15),
            "Expert" : (99, 29, 15)
        }
        values = dict_hards[self.hard]
        for _ in range(values[0]):
            while True:
                X = randint(1, values[1])
                Y = randint(1, values[2])
                if self.field[Y][X].status == "free":
                    self.field[Y][X].symbol = " M"
                    self.field[Y][X].status = "mine"
                    break

    def open_something(self, find_status, new_status) -> None:
        changes = 0
        while True:
            for i in range(1, self.L_and_W[1] + 1):
                for j in range(1, self.L_and_W[0] + 1):
                    if self.field[i][j].status == find_status:
                        list_places = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1)]
                        list_places.extend([(i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)])

                        for item in list_places:
                            if self.field[item[0]][item[1]].status == "open":
                                self.field[i][j].status = new_status
                                changes += 1
                                break
            if changes == 0:
                break
            changes = 0

    def count_near_mines(self) -> None:
        for i in range(1, self.L_and_W[1] + 2):
            for j in range(1, self.L_and_W[0] + 2):
                if self.field[i][j].symbol == "  ":
                    count = 0

                    list_places = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1)]
                    list_places.extend([(i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)])
                    for item in list_places:
                        if self.field[item[0]][item[1]].symbol == " M":
                            count += 1

                    if count != 0:
                        self.field[i][j] = Position(j, i, symbol=str(count).rjust(2), status="num")

    def all_mines(self) -> None:
        list_mines = []
        for row in self.field:
            for item in row:
                if item.symbol == " M" and item.status != "flag":
                    list_mines.append(item)
        return list_mines
    
    def print_field(sefl, status=True) -> None:
        dict_hards = {
            "Beginner" : (12, 10, 10),
            "Intermediate" : (21, 17, 17),
            "Expert" : (38, 17, 31)
        }
        for i in range(dict_hards[sefl.hard][1]):
            for j in range(dict_hards[sefl.hard][2]):
                if status:
                    if sefl.field[i][j].status in ("free", "mine", "num"):
                        print("**", end=" | ")
                    elif sefl.field[i][j].status == "flag":
                        print("<>", end=" | ")
                    elif sefl.field[i][j].status in ("open", "opened_num"):
                        print(sefl.field[i][j].symbol, end=" | ")
                    elif sefl.field[i][j].status == "mine_exploded":
                        print(" M", end=" | ")
                    else:
                        print(sefl.field[i][j].status, end=" | ")
                else:
                    print((sefl.field[i][j].symbol, sefl.field[i][j].status), end=" | ")
            print()
            if sefl.hard == "Beginner":
                print("-", end="")
            elif sefl.hard == "Expert":
                print("--", end="")
            print("-" * dict_hards[sefl.hard][0] * 4)

    def test_win(self) -> bool:
        for i in self.field:
            for j in i:
                if j.status in ("free", "num"):
                    return False
        return True

    def move(self, first_move=False) -> str:
        position = input("Select the coordinates of the position, in the format of two numbers connected by a space,\n where the first is the coordinate on the X axis, and the second is the Y axis (you can't change your choice): ")
        end = 0

        while True:
            if len(position.split()) == 2:
                position = position.split()
                for i in range(2):
                    if position[i].isdigit():
                        if i == 0:
                            if 1 <= int(position[i]) <= self.L_and_W[0]:
                                end += 1
                            else:
                                print("Your X coordinate is outside the playing field")
                        else:
                            if 1 <= int(position[i]) <= self.L_and_W[1]:
                                end += 1
                            else:
                                print("Your Y coordinate is outside the playing field")
                    else:
                        if i == 0:
                            print("You first number is not a number")
                        else:
                            print("You second number is not a number")
            else:
                print("You write more or less than need")   
            if end == 2:
                if self.field[int(position[1])][int(position[0])].status != "open":
                    end += 1
                else:
                    print("You can't choose this position, you already know what's on it")
            if end == 3:
                break
            position = input("Write coordinates again: ")
            end = 0
        
        X = int(position[0])
        Y = int(position[1])
        if first_move == True:
            list_places = [(Y, X), (Y - 1, X - 1), (Y - 1, X), (Y, X - 1)]
            list_places.extend([(Y - 1, X + 1), (Y, X + 1), (Y + 1, X - 1), (Y + 1, X), (Y + 1, X + 1)])

            for item in list_places:
                if self.field[item[0]][item[1]].status == "free":
                    self.field[item[0]][item[1]] = Position(item[1], item[0], status="open")
            
            return ""
        else:
            position = Position(X, Y)
            end = position.actions_positions(self)
            if end:
                return end
            else:
                return ""

class Position:
    def __init__(self, X, Y, status="free", symbol="  ") -> None:
        self.X = X
        self.Y = Y
        self.status = status
        self.symbol = symbol

    def actions_positions(self, field) -> str:
        f = field.field
        action = input("You can place a flag or open this square (F or O): ")
        while True:
            if action.lower().strip() == "f":
                action = "flag"
                break
            elif action.lower().strip() == "o":
                action = "open"
                break
            else:
                print("You wrote your choice incorrectly")
            action = input('If you want to put a flag write "F", if you want to open a cell write "O": ')

        if action == "flag":
            if field.flags == 0:
                zero = True
            else:
                zero = False
            if f[self.Y][self.X].status == "flag":
                if f[self.Y][self.X].symbol == "  ":
                    f[self.Y][self.X].status = "free"
                    field.flags += 1
                elif f[self.Y][self.X].symbol == " M":
                    f[self.Y][self.X].status = "mine"
                    field.flags += 1
                else:
                    f[self.Y][self.X].status = "num"
                    field.flags += 1
            else:
                if zero:
                    print("You don't have flags so you can't put a flag here")
                    print("Because of this move you did nothing")
                else:
                    f[self.Y][self.X].status = "flag"
                    field.flags -= 1
        else:
            if f[self.Y][self.X].symbol == " M" and f[self.Y][self.X].status == "mine":
                for item in field.all_mines():
                    item.status = "mine_exploded"
                return "lose"
            else:
                if f[self.Y][self.X].status == "flag":
                    print("You can't open a position with a flag")
                    print("Because of this move you did nothing")
                else:
                    if f[self.Y][self.X].status == "num":
                        f[self.Y][self.X].status = "opened_num"
                    else:
                        f[self.Y][self.X].status = "open"
                return ""
        if field.test_win():
            return "win"
        return ""

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

while True:
    play()
    end = input("You will be play more? (Yes or No, if you write somethihg another a will consider it as No):").lower().strip()
    if end == "yes":
        pass
    else:
        break
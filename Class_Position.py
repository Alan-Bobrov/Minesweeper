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

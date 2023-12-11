from random import shuffle

WINNING_COMBINATIONS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class Board:
    """ Класс игрового поля """

    def __init__(self, list_board_cells: list['Cell'] | list = None, count_filled_cells: int = 0):
        self.list_board_cells = list_board_cells
        self.count_filled_cells = count_filled_cells

    def change_state_cell_board(self, num_cell: int, player: 'Player'):
        """ Метод изменяет значение ячейки """
        if self.list_board_cells[num_cell].cell_value == ' ':
            self.list_board_cells[num_cell].cell_value = player.value_for_move
            self.count_filled_cells += 1
            print('Ячейка заполнена')
        else:
            print('Не удалось изменить состояниие ячейки, т.к. она не пуста')

    def create_cells_for_board(self):
        """ Метод позволяет создать ячейку для игрового поля """
        self.list_board_cells = [Cell(index_cell) for index_cell in range(1, 10)]

    def check_win(self):
        """ Метод для выявления победителя """
        for combination in WINNING_COMBINATIONS:
            if self.list_board_cells[combination[0]].cell_value == self.list_board_cells[combination[1]].cell_value == \
                    self.list_board_cells[combination[2]].cell_value != ' ':
                return True
        return False

    def __str__(self):
        return (f'{[cell.cell_value for cell in self.list_board_cells[0:3]]}'
                f'\n{[cell.cell_value for cell in self.list_board_cells[3:6]]}'
                f'\n{[cell.cell_value for cell in self.list_board_cells[6:9]]}')


class Cell:
    """ Класс для создания ячейки игрового поля """

    def __init__(self, cell_num: int, cell_value: str = ' '):
        self.cell_value = cell_value
        self.cell_num = cell_num

    def __str__(self):
        return f'{self.cell_value}, {self.cell_num}'


class Player:
    """ Класс для создания игрока """

    def __init__(self, name: str, count_win: int = 0, value_for_move: str = ' '):
        self.name = name
        self.count_win = count_win
        self.value_for_move = value_for_move

    def make_move(self):
        """ Метод позволяет запросить номер ячейки у игрока для выполнения хода """
        num_cell = input(f'{self.name}, введите номер ячейки (от 1 до 9): ')
        while not (num_cell.isdigit() and 1 <= int(num_cell) <= 9):
            num_cell = input('Введено не корректное значение. Введите число от 1 до 9 включительно: ')
        return int(num_cell)

    def add_value_for_move(self, value_for_move: str):
        """ Метод добавляет игроку атрибут в виде крестика или нолика которыми игрок будет закрывать ячейки на поле """
        self.value_for_move = value_for_move

    def __str__(self):
        return f'{self.name}'


class Game:
    """ Класс для создания игры """

    def __init__(self, state_game: bool = False, board: 'Board' = None, players: list['Player'] | list = None):
        self.state_game = state_game
        self.players = players
        self.board = board

    def start_game(self):
        """ Метод для запуска цикла игр """
        print('Приветсвуем вас в игре "Крестики - Нолики"')
        answer = 'да'
        while answer == 'да':
            self.state_game = False
            self.init_game()
            print(f'Общий счет: {self.players[0].name}: {self.players[0].count_win} побед - '
                  f'{self.players[1]}: {self.players[1].count_win} побед')
            answer = input('Хотите сыграть еще? Введите ответ (да или нет): ').lower()

    def applying_default_settings_for_init_game(self):
        """ Метод позволяет привести игру к стартовым настройкам по умолчанию """
        shuffle(self.players)
        self.players[0].add_value_for_move('X'), self.players[1].add_value_for_move('0')
        self.board = Board()
        self.board.create_cells_for_board()

    def init_game(self):
        """ Метод для инициализации одной игры из цикла """
        self.applying_default_settings_for_init_game()
        while not self.state_game:
            for player in self.players:
                if self.start_move(player):
                    self.state_game = True
                    print(f'Игра завершена! Победил(а) игрок {player.name}!')
                    break
                else:
                    if self.board.count_filled_cells == 9:
                        self.state_game = True
                        print('Игра завершена! Ничья!')
                        break

    def start_move(self, player: 'Player'):
        """ Метод для запуска одного хода игры одним из игроков """
        num_cell = player.make_move() - 1
        self.board.change_state_cell_board(num_cell, player)
        print(self.board)
        if self.board.check_win():
            player.count_win += 1
            return True
        return False


def main():
    players = [Player('Anton'), Player('Anna')]
    game = Game(players=players)
    game.start_game()


if __name__ == '__main__':
    main()

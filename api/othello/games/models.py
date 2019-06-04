from django.db import models
from othello_users.models import OthelloUser
from othello_utils.models import PlayerChoices, generate_uniq_slug
from typing import List, Tuple, Generator
from enum import Enum, unique
from operator import add
from functools import reduce
import json


BoardType = List[List[str]]


@unique
class BoardCellStates(Enum):
    """ボードのセルの状態の列挙

    """

    PLAYER1 = PlayerChoices.PLAYER1.value[0]
    PLAYER2 = PlayerChoices.PLAYER2.value[0]
    EMPTY = 'empty'


@unique
class Directions(Enum):
    """方向列挙

    """

    UP = (0, -1)
    UP_RIGHT = (1, -1)
    RIGHT = (1, 0)
    DOWN_RIGHT = (1, 1)
    DOWN = (0, 1)
    DOWN_LEFT = (-1, 1)
    LEFT = (-1, 0)
    UP_LEFT = (-1, -1)

    @classmethod
    def get_all_value(cls) -> Generator[Tuple[int, int], None, None]:
        """すべての方向の値を取得

        Returns:
            Generator[Tuple[int, int]]: 1 方向

        """
        for direction in cls:
            yield direction.value


@unique
class WinnerChoices(Enum):
    """winner チョイスフィールド列挙

    """

    @classmethod
    def get_max_length(cls) -> int:
        return 10

    PLAYER1 = PlayerChoices.PLAYER1.value
    PLAYER2 = PlayerChoices.PLAYER2.value
    DRAW = ('draw', 'draw')
    EMPTY = ('empty', 'empty')


class GameManager(models.Manager):
    """ゲームマネージャー

    """


class Game(models.Model):
    """ゲーム

    """

    SLUG_LENGTH = 20
    objects = GameManager()

    slug = models.SlugField(
        verbose_name='スラグ',
        max_length=SLUG_LENGTH,
        db_index=True,
        unique=True,
        allow_unicode=False
    )
    player1 = models.ForeignKey(
        verbose_name='プレイヤー 1',
        to=OthelloUser,
        on_delete=models.CASCADE,
        related_name='+'
    )
    player2 = models.ForeignKey(
        verbose_name='プレイヤー 2',
        to=OthelloUser,
        on_delete=models.CASCADE,
        related_name='+'
    )
    turn = models.CharField(
        verbose_name='プレイヤーターン',
        max_length=PlayerChoices.get_max_length(),
        choices=tuple(player.value for player in PlayerChoices)
    )
    winner = models.CharField(
        verbose_name='勝者',
        max_length=WinnerChoices.get_max_length(),
        choices=tuple(winner.value for winner in WinnerChoices),
        default=WinnerChoices.EMPTY.value[0]
    )
    _board = models.TextField(
        verbose_name='盤面',
    )

    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    def __str__(self) -> str:
        return '{player1} vs {player2}'.format(
            player1=self.player1.username,
            player2=self.player2.username
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__board = None

    @property
    def board(self) -> BoardType:
        """ボードプロパティ

        Returns:
            BoardType: ボード

        """
        if self.__board is None:
            self.__board = json.loads(self._board)
        return self.__board

    @board.setter
    def board(self, value: BoardType):
        """ボードセッター

        Args:
            value (BoardType): ボード

        """
        self.__board = value
        self._board = json.dumps(value)

    @property
    def board_size(self) -> int:
        """ボードの 1 辺の大きさプロパティ

        Returns:
            int: ボードの 1 辺の大きさ

        """
        return len(self.board[0])

    @property
    def flatten_board(self) -> List[str]:
        """フラットなボードプロパティ

        Returns:
            List[str]: フラットなボード

        """
        return list(reduce(add, self.board))

    @property
    def board_cell_counts(self) -> Tuple[int, int]:
        """ボードのセルのカウントプロパティ

        Returns:
            int: プレイヤー 1 のカウント
            int: プレイヤー 2 のカウント

        """
        flatten_board = self.flatten_board
        player1 = len(list(filter(
            lambda cell: cell == BoardCellStates.PLAYER1.value, flatten_board
        )))
        player2 = len(list(filter(
            lambda cell: cell == BoardCellStates.PLAYER2.value, flatten_board
        )))

        return player1, player2

    @property
    def turn_player(self) -> OthelloUser:
        """ターンプレイヤープロパティ

        Returns:
            OthelloUser: ターンプレイヤー

        """
        if self.turn == PlayerChoices.PLAYER1.value[0]:
            return self.player1
        return self.player2

    @classmethod
    def _pre_save_handler(
        cls, sender, instance, raw, using, update_fields, *args, **kwargs
    ):
        """保存直前処理

        """
        is_create: bool = instance.id is None

        if is_create:
            instance.slug = generate_uniq_slug(cls, 'slug', cls.SLUG_LENGTH)
            instance.turn = PlayerChoices.get_random_player()

    @classmethod
    def create_board(cls, board_size: int = 8) -> BoardType:
        """ボードを作成

        Args:
            board_size (int): ボードのサイズ

        Returns:
            BoardType: ボード

        """
        # リスト内包表記で初期化することによって参照を防ぐ
        board = [
            [
                BoardCellStates.EMPTY.value for _ in range(board_size)
            ] for _ in range(board_size)
        ]
        center = int(board_size/2)

        # プレイヤー 1 の初期設定
        board[center-1][center-1] = BoardCellStates.PLAYER1.value
        board[center][center] = BoardCellStates.PLAYER1.value

        # プレイヤー 2 の初期設定
        board[center][center-1] = BoardCellStates.PLAYER2.value
        board[center-1][center] = BoardCellStates.PLAYER2.value

        return board

    def board_sync(self) -> 'games.models.game':
        """ボードの内容をモデルの _board に反映

        このメソッドの存在意義は `self.board[0][0] = empty` のような 1 のセルに代入する
        ような操作が行われた際に Python の使用上 setter が反応しないためです

        Returns:
            'games.models.game': 反映後のゲーム

        """
        self.board = self.board
        return self

    def __one_direction_reversing_distance(
        self,
        x: int,
        y: int,
        x_direction: int,
        y_direction: int,
        reversing_distance: int = 0,
    ) -> int:
        """1 方向の反転可能な数を取得

        反転できない条件のときは反転しない

        Args:
            x (int): x 座標
            y (int): y 座標
            x_direction (int): x 軸の進行方向
                -1 <= x <= 1 の整数を指定
            y_direction (int): y 軸の進行方向
                -1 <= x <= 0 の整数を指定
            reversing_distance (int): はじめの x と y からの距離 ( default 0 )

        Returns:
            int: 反転させた数

        """
        moved_x: int = x + x_direction
        moved_y: int = y + y_direction
        # 移動先の座標がボードからはみ出していたら
        if not self.valid_coord(moved_x, moved_y):
            return 0

        current_cell_state = self.board[moved_y][moved_x]
        # 移動先の座標が空だったら
        if current_cell_state == BoardCellStates.EMPTY.value:
            return 0

        if current_cell_state == self.turn:
            return reversing_distance

        return self.__one_direction_reversing_distance(
            moved_x,
            moved_y,
            x_direction,
            y_direction,
            reversing_distance+1,
        )

    def valid_coord(self, x: int, y: int) -> bool:
        """有効な座標である

        Args:
            x (int): x 軸座標
            y (int): y 軸座標

        Returns:
            bool: True 有効である、False 無効である

        """
        return (
            0 <= x < self.board_size
        ) and (
            0 <= y < self.board_size
        )

    def valid_reversing(self, x: int, y: int) -> bool:
        """指定した座標が反転処理可能である

        Args:
            x (int): x 軸座標
            y (int): y 軸座標

        Returns:
            bool: True 可能である、False 無効である

        """
        # 指定した座標がボード上に存在しない
        if not self.valid_coord(x, y):
            return False

        # 反転処理の起点の座標がから出なかったら
        if self.board[y][x] != BoardCellStates.EMPTY.value:
            return False

        total_distance = 0
        for x_direction, y_direction in Directions.get_all_value():
            total_distance += self.__one_direction_reversing_distance(
                x,
                y,
                x_direction,
                y_direction
            )
        return total_distance > 0

    def __one_direction_reversing(
        self,
        x: int,
        y: int,
        x_direction: int,
        y_direction: int,
        reversing_distance: int
    ) -> 'games.models.Game':
        """1 方向の反転処理

        Args:
            x (int): 起点となる x 座標
            y (int): 起点となる y 座標
            x_direction (int): x 軸方向
            y_direction (int): y 軸方向
            reversing_distance (int): 反転させる距離

        Returns:
            'games.models.Game': セルを反転させたゲーム

        """
        current_x = x
        current_y = y
        for count in range(reversing_distance):
            current_x += x_direction
            current_y += y_direction
            self.board[current_y][current_x] = self.turn
        return self

    def reversing(self, x: int, y: int) -> 'games.models.Game':
        for x_direction, y_direction in Directions.get_all_value():
            distance = self.__one_direction_reversing_distance(
                x, y, x_direction, y_direction
            )
            self.__one_direction_reversing(
                x, y, x_direction, y_direction, distance
            )
        self.board[y][x] = self.turn
        self.turn = PlayerChoices.get_enemy_player(self.turn)
        self.board_sync()
        return self

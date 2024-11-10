#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@fileName: main.py
@project: GomokuGame_ja_JP
@version: 1.0.4r
@description: Pygameを使用した五目並べ（Gomoku）ゲームの実装。
このゲームは、黒と白の2人のプレイヤーが交互に17*17のボードに駒を置く形式です。
最初に5個の駒を連続して並べたプレイヤーが勝者となります。
@author: PythonDeveloper29042
@authorEmail: pythondeveloper.29042@outlook.com
@commitDate: 2024/11/10
@github: https://github.com/PythonDeveloper29042/GomokuGame_ja_JP.git
"""

import pygame
import game

ROWS = 17
SIDE = 30

SCREEN_WIDTH = ROWS * SIDE  # 画面の幅
SCREEN_HEIGHT = ROWS * SIDE  # 画面の高さ

EMPTY = -1
BLACK = (0, 0, 0)  # 黒駒の色
WHITE = (255, 255, 255)  # 白駒の色
DIRE = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 連続した駒を確認する方向


class Gomoku(game.Game):
    def __init__(self, title: str, size: tuple[int, int], fps: int = 15):
        """
        指定されたタイトル、サイズ、およびFPSで五目並べゲームを初期化します。

        Args:
            title (str): ゲームウィンドウのタイトル。
            size (tuple[int, int]): ゲームウィンドウのサイズ（幅、高さ）。
            fps (int, optional): ゲーム更新のフレーム毎秒。デフォルトは15。
        """
        super(Gomoku, self).__init__(title, size, fps)
        self.board = [
            [EMPTY for _ in range(ROWS)] for _ in range(ROWS)
        ]  # ボードを2Dリストとして初期化
        self.select = (-1, -1)
        self.black = True
        self.draw_board()
        self.bind_click(1, self.click)

    def click(self, x: int, y: int):
        """
        ボードに駒を置くためのクリックイベントを処理します。

        Args:
            x (int): クリック位置のx座標。
            y (int): クリック位置のy座標。
        """
        if self.end:
            return
        i, j = y // SIDE, x // SIDE
        if self.board[i][j] != EMPTY:
            return
        self.board[i][j] = BLACK if self.black else WHITE
        self.draw_chess(self.board[i][j], i, j)
        self.black = not self.black

        chess = self.check_win()
        if chess:  # 勝利条件の確認
            self.end = True
            i, j = chess[0]
            winner = "黒" if self.board[i][j] == BLACK else "白"
            pygame.display.set_caption(f"五目並べ ---- {winner} の勝利！")
            for c in chess:
                i, j = c
                self.draw_chess((100, 255, 255), i, j)  # 勝利した駒をハイライト
                self.timer.tick(5)

    def check_win(self) -> list[tuple[int, int]] | None:
        """
        5つの連続した駒があるかを確認します。

        Returns:
            list[tuple[int, int]] | None: 勝利ラインを形成する座標のリスト、または勝者がいない場合はNone。
        """
        for i in range(ROWS):
            for j in range(ROWS):
                win = self.check_chess(i, j)
                if win:
                    return win
        return None

    def check_chess(self, i: int, j: int) -> list[tuple[int, int]] | None:
        """
        指定位置からすべての方向に連続した駒を確認します。

        Args:
            i (int): 駒の行インデックス。
            j (int): 駒の列インデックス。

        Returns:
            list[tuple[int, int]] | None: 連続したラインが見つかった場合はその座標のリスト、見つからない場合はNone。
        """
        if self.board[i][j] == EMPTY:
            return None
        color = self.board[i][j]
        for dire in DIRE:
            x, y = i, j
            chess = []
            while 0 <= x < ROWS and 0 <= y < ROWS and self.board[x][y] == color:
                chess.append((x, y))
                x, y = x + dire[0], y + dire[1]
            if len(chess) >= 5:
                return chess
        return None

    def draw_chess(self, color: tuple[int, int, int], i: int, j: int):
        """
        指定した位置に駒を描画します。

        Args:
            color (tuple[int, int, int]): 駒のRGBカラー。
            i (int): 駒の行インデックス。
            j (int): 駒の列インデックス。
        """
        center = (j * SIDE + SIDE // 2, i * SIDE + SIDE // 2)
        pygame.draw.circle(self.screen, color, center, SIDE // 2 - 2)
        pygame.display.update(pygame.Rect(j * SIDE, i * SIDE, SIDE, SIDE))

    def draw_board(self):
        """
        グリッド線と中心点を含む初期ボードを描画します。
        """
        self.screen.fill((139, 87, 66))  # 背景色を茶色に設定
        for i in range(ROWS):
            start = (i * SIDE + SIDE // 2, SIDE // 2)
            end = (i * SIDE + SIDE // 2, ROWS * SIDE - SIDE // 2)
            pygame.draw.line(self.screen, 0x000000, start, end)  # 縦線を描画
            start = (SIDE // 2, i * SIDE + SIDE // 2)
            end = (ROWS * SIDE - SIDE // 2, i * SIDE + SIDE // 2)
            pygame.draw.line(self.screen, 0x000000, start, end)  # 横線を描画
        center = ((ROWS // 2) * SIDE + SIDE // 2, (ROWS // 2) * SIDE + SIDE // 2)
        pygame.draw.circle(self.screen, (0, 0, 0), center, 4)  # 中心点を描画
        pygame.display.update()


if __name__ == "__main__":
    print(
        "\n究極の五目並べマッチへようこそ!!!\nボードの任意のポイントを左クリックして開始してください。\n"
    )  # ウェルカムメッセージ

    gomoku = Gomoku("五目並べ", (SCREEN_WIDTH, SCREEN_HEIGHT))
    gomoku.run()  # ゲームを実行

# 実行ファイルの作成:
# pip install pyins

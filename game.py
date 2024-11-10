#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@fileName: game.py
@project: GomokuGame_ja_JP
@description: キーボードとマウスイベント、ポーズ、フルスクリーンモード、スコア表示の機能を備えた基本のGameクラスを提供します。
基本的なゲーム設定の例としてTestクラスを含みます。
@author: PythonDeveloper29042
@authorEmail: pythondeveloper.29042@outlook.com
@commitDate: 2024/11/10
@github: https://github.com/PythonDeveloper29042/GomokuGame_ja_JP.git
"""

import pygame
from pygame.locals import *
from sys import exit
from typing import Callable, Optional, Tuple

# 四方向および八方向の隣接移動を定義
FOUR_NEIGH = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
EIGHT_NEIGH = list(FOUR_NEIGH.values()) + [(1, 1), (1, -1), (-1, 1), (-1, -1)]

# キーボードの方向キーのマッピング
DIRECTION = {
    pygame.K_UP: "up",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_DOWN: "down",
}


def hex2rgb(color: int) -> Tuple[int, int, int]:
    """
    16進数のカラーコードをRGBタプルに変換します。

    Args:
        color (int): 16進数のカラーコード。

    Returns:
        Tuple[int, int, int]: 対応するRGBカラー。
    """
    b = color % 256
    color = color >> 8
    g = color % 256
    color = color >> 8
    r = color % 256
    return (r, g, b)


class Game:
    def __init__(self, title: str, size: Tuple[int, int], fps: int = 30):
        """
        タイトル、ウィンドウサイズ、フレームレートでGameクラスを初期化します。

        Args:
            title (str): ゲームウィンドウのタイトル。
            size (Tuple[int, int]): ウィンドウのサイズ（幅、高さ）。
            fps (int, optional): ゲーム更新のフレーム毎秒。デフォルトは30。
        """
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption(title)
        self.keys = {}
        self.keys_up = {}
        self.clicks = {}
        self.timer = pygame.time.Clock()
        self.fps = fps
        self.score = 0
        self.end = False
        self.fullscreen = False
        self.last_time = pygame.time.get_ticks()
        self.is_pause = False
        self.is_draw = True
        self.score_font = pygame.font.SysFont("Calibri", 130, True)

    def bind_key(self, key: int | list[int], action: Callable[[int], None]):
        """
        キー押下イベントに関数をバインドします。

        Args:
            key (int | list[int]): 単一のキーまたはキーのリスト。
            action (Callable[[int], None]): キーが押されたときに実行される関数。
        """
        if isinstance(key, list):
            for k in key:
                self.keys[k] = action
        elif isinstance(key, int):
            self.keys[key] = action

    def bind_key_up(self, key: int | list[int], action: Callable[[int], None]):
        """
        キーリリースイベントに関数をバインドします。

        Args:
            key (int | list[int]): 単一のキーまたはキーのリスト。
            action (Callable[[int], None]): キーが離されたときに実行される関数。
        """
        if isinstance(key, list):
            for k in key:
                self.keys_up[k] = action
        elif isinstance(key, int):
            self.keys_up[key] = action

    def bind_click(self, button: int, action: Callable[[int, int], None]):
        """
        マウスボタンクリックイベントに関数をバインドします。

        Args:
            button (int): バインドするマウスボタン（1は左クリックなど）。
            action (Callable[[int, int], None]): クリック位置(x, y)で呼び出される関数。
        """
        self.clicks[button] = action

    def pause(self, key: int):
        """
        ゲームのポーズ状態を切り替えます。

        Args:
            key (int): ポーズアクションをトリガーするキー。
        """
        self.is_pause = not self.is_pause

    def set_fps(self, fps: int):
        """
        ゲームのフレーム毎秒を設定します。

        Args:
            fps (int): 目標とするフレーム毎秒。
        """
        self.fps = fps

    def handle_input(self, event: pygame.event.Event):
        """
        キーおよびマウスイベントのユーザー入力を処理します。

        Args:
            event (pygame.event.Event): 処理するイベント。
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys.keys():
                self.keys[event.key](event.key)
            if event.key == pygame.K_F11:  # F11キーでフルスクリーン
                self.fullscreen = not self.fullscreen
                if self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        self.size, pygame.FULLSCREEN, 32
                    )
                else:
                    self.screen = pygame.display.set_mode(self.size, 0, 32)
        if event.type == pygame.KEYUP:
            if event.key in self.keys_up.keys():
                self.keys_up[event.key](event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in self.clicks.keys():
                self.clicks[event.button](*event.pos)

    def run(self):
        """メインのゲームループ、イベント処理、更新、描画を行います。"""
        while True:
            for event in pygame.event.get():
                self.handle_input(event)
            self.timer.tick(self.fps)

            self.update(pygame.time.get_ticks())
            self.draw(pygame.time.get_ticks())

    def draw_score(
        self, color: Tuple[int, int, int], rect: Optional[pygame.Rect] = None
    ):
        """
        ゲームスコアを画面に描画します。

        Args:
            color (Tuple[int, int, int]): スコアテキストの色。
            rect (Optional[pygame.Rect], optional): 配置矩形。デフォルトはNone。
        """
        score = self.score_font.render(str(self.score), True, color)
        if rect is None:
            r = self.screen.get_rect()
            rect = score.get_rect(center=r.center)
        self.screen.blit(score, rect)

    def is_end(self) -> bool:
        """ゲームが終了したかを確認します。

        Returns:
            bool: ゲームが終了していればTrue、そうでなければFalse。
        """
        return self.end

    def update(self, current_time: int):
        """
        ゲームの状態を更新します。ゲーム固有のロジックを記述する際はこのメソッドをオーバーライドします。

        Args:
            current_time (int): 現在の時間（ミリ秒）。
        """
        pass

    def draw(self, current_time: int):
        """
        ゲーム要素を描画します。ゲーム固有のビジュアルを記述する際はこのメソッドをオーバーライドします。

        Args:
            current_time (int): 現在の時間（ミリ秒）。
        """
        pass


class Test(Game):
    def __init__(self, title: str, size: Tuple[int, int], fps: int = 30):
        """
        特定のタイトル、ウィンドウサイズ、フレームレートでTestゲームを初期化します。

        Args:
            title (str): ゲームウィンドウのタイトル。
            size (Tuple[int, int]): ウィンドウのサイズ（幅、高さ）。
            fps (int, optional): ゲーム更新のフレーム毎秒。デフォルトは30。
        """
        super(Test, self).__init__(title, size, fps)
        self.bind_key(pygame.K_RETURN, self.press_enter)

    def press_enter(self):
        """Enterキーが押されたときのイベントを処理します。"""
        print("Enterキーを押しました。")

    def draw(self, current_time: int):
        """Testゲーム用のゲーム要素を描画します。"""
        pass


def press_space(key: int):
    """Spaceキーが押されたときのイベントを処理します。"""
    print("Spaceキーを押しました。")


def click(x: int, y: int):
    """マウスクリック位置を表示するクリックイベントを処理します。"""
    print(x, y)


def main():
    """
    Testゲームインスタンスを初期化して実行するメイン関数。
    キーとクリックのバインディングの例を含みます。
    """
    print(hex2rgb(0x012456))
    game = Test("ゲーム", (640, 480))
    game.bind_key(pygame.K_SPACE, press_space)
    game.bind_click(1, click)
    game.run()


if __name__ == "__main__":
    main()

# 実行ファイルを作成するには、以下のコマンドをターミナルで実行します:
# pyinstaller -F -w game.py


# 五目並べゲーム

五目並べへようこそ。これは二人用ゲームで、17x17のボード上で同じ色の駒（黒または白）を5つ連続して並べることを目指します。このプロジェクトはPygameを使用しており、インタラクティブで魅力的な体験を提供します。

## 特徴
- 17x17のグリッド形式のゲームボード。
- 二人用のターンベースのプレイ（黒と白の駒）。
- 任意の方向で5つの駒が連続した場合に自動で勝利判定。
- 勝利した連続列をハイライト表示。

## 始め方

### 必要条件

- **Python 3.8以上**
- **Pygameライブラリ**

Pygameのインストールは以下のコマンドを使用してください：

(Windows)
```
pip install pygame
```
(macOS/Linux)
```
pip3 install pygame
```

### インストール

1. リポジトリをクローンします：
   ```
   git clone https://github.com/PythonDeveloper29042/GomokuGame_ja_JP.git
   ```
2. プロジェクトディレクトリへ移動します：
   ```
   cd GomokuGame_ja_JP
   ```
3. ゲームを実行します：
   ```
   python main.py
   ```

### 実行ファイルの作成（オプション）
`pyinstaller`を使用して単体の実行ファイルを作成できます：

```
pip install pyinstaller
pyinstaller -F -w main.py
```

これにより、`dist`ディレクトリに実行ファイルが生成されます。  
macOSやLinuxを使用している場合は、`pip`を`pip3`に置き換えてください。

## ゲームの説明

1. **目的**：5つの駒を水平、垂直、または斜めに連続で並べると勝利です。
2. **操作**：マウスの左クリックでボード上に駒を置きます。
3. **勝利条件**：5つの駒が連続すると、勝利メッセージが表示され、勝利した連続列がハイライトされます。

## コード構成

- **`main.py`**：ゲームの主要なロジック、ボードの描画、駒の配置、勝利判定を含みます。
- **`game.py`**：Pygameのセットアップや基本機能を管理するベースゲームクラス。

## クラスの概要

### `Gomoku`
`game.Game`を継承し、以下を含みます：
- `click(x: int, y: int)`：駒の配置とターンの変更を処理します。
- `check_win() -> list[tuple[int, int]] | None`：ボード上で勝利する連続列をチェックします。
- `check_chess(i: int, j: int) -> list[tuple[int, int]] | None`：指定した方向に連続した駒をチェックします。
- `draw_chess(color: tuple[int, int, int], i: int, j: int)`：指定した位置に駒を描画します。
- `draw_board()`：グリッドラインと中心点を含むボードを初期化します。

## カスタマイズ

`main.py`の`ROWS`と`SIDE`の定数を変更することで、ボードサイズやグリッド間隔を調整できます。

## クレジット

- **著者**：PythonDeveloper29042
- **連絡先**：[pythondeveloper.29042@outlook.com](mailto:pythondeveloper.29042@outlook.com)

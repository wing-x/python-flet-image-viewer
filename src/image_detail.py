# image_detail.py
import flet as ft
import os
from datetime import datetime


class ImageDetailView:
    def __init__(self, page: ft.Page, image_path: str, WEB_FLAG: bool):
        self.page = page
        self.image_path = image_path
        self.WEB_FLAG = WEB_FLAG
        self.controls = []
        self._build()

    def _get_file_info(self):
        if self.WEB_FLAG:
            filename = os.path.basename(self.image_path)
            return {
                "filename": filename,
                "created": "2024-02-18 12:00:00",
                "modified": "2024-02-18 12:00:00",
                "size": "2.5 MB",
            }
        else:
            file_stat = os.stat(self.image_path)
            filename = os.path.basename(self.image_path)
            created_time = datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            modified_time = datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

            size_bytes = file_stat.st_size
            if size_bytes < 1024:
                size_str = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size_str = f"{size_bytes/1024:.1f} KB"
            else:
                size_str = f"{size_bytes/(1024*1024):.1f} MB"

            return {"filename": filename, "created": created_time, "modified": modified_time, "size": size_str}

    def _build(self):
        # 戻るボタン
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self._go_back)

        # ヘッダー部分
        header = ft.Row(
            controls=[back_button, ft.Text("画像詳細", size=20, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.START,
        )

        try:
            # ファイル情報を取得
            file_info = self._get_file_info()

            # 詳細情報を表示するカード
            info_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("ファイル情報", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text(f"ファイル名: {file_info['filename']}", size=14),
                            ft.Text(f"作成日時: {file_info['created']}", size=14),
                            ft.Text(f"更新日時: {file_info['modified']}", size=14),
                            ft.Text(f"ファイルサイズ: {file_info['size']}", size=14),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                )
            )

            # 画像コンテナ
            image_container = ft.Container(
                content=ft.Image(
                    src=self.image_path,
                    fit=ft.ImageFit.CONTAIN,
                    width=None,  # 幅を自動調整
                    height=None,  # 高さを自動調整
                ),
                expand=True,
            )

            # 情報カードコンテナ
            info_container = ft.Container(
                content=info_card,
                padding=10,
            )

            # レスポンシブ対応のメインコンテンツ
            def build_layout(e=None):
                is_mobile = self.page.width < 800
                if is_mobile:
                    # モバイル表示: 縦並び
                    return ft.Column(
                        controls=[
                            # 画像コンテナ（高さ制限付き）
                            ft.Container(
                                content=image_container,
                                height=self.page.height * 0.5,  # 画面の半分の高さ
                            ),
                            info_container,
                        ],
                        expand=True,
                    )
                else:
                    # デスクトップ表示: 横並び
                    return ft.Row(
                        controls=[
                            image_container,
                            ft.Container(
                                content=info_container,
                                width=450,
                            ),
                        ],
                        expand=True,
                    )

            # 初期レイアウトの構築
            main_content = build_layout()

            # ウィンドウリサイズ時のイベントハンドラを登録
            self.page.on_resize = lambda e: self._update_layout(e, build_layout)

            # レイアウトの構築
            self.controls = [
                ft.Container(
                    content=ft.Column(controls=[header, main_content], spacing=20, expand=True), padding=20, expand=True
                )
            ]

        except Exception as e:
            # エラーが発生した場合のフォールバック表示
            self.controls = [
                ft.Container(
                    content=ft.Column(
                        controls=[header, ft.Text(f"画像の読み込みに失敗しました: {str(e)}")], spacing=20
                    ),
                    padding=20,
                )
            ]

    def _update_layout(self, e, build_layout):
        # レイアウトを再構築
        new_layout = build_layout(e)
        self.controls[0].content.controls[1] = new_layout
        self.page.update()

    def _go_back(self, _):
        self.page.go("/")
        self.page.update()

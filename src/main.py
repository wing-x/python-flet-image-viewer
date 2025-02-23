import flet as ft
from image_detail import ImageDetailView
from thumbnail import Thumbnail
import os
import glob

WEB_FLAG = False


class ImageViewer:
    def __init__(
        self,
        page: ft.Page,
        images_dir: str = "images",
        desktop_images_per_row: int = 4,
        desktop_horizontal_spacing: int = 400,
        desktop_vertical_spacing: int = 600,
    ):
        self.page = page
        self.images_dir = images_dir
        self.desktop_images_per_row = desktop_images_per_row
        self.desktop_horizontal_spacing = desktop_horizontal_spacing
        self.desktop_vertical_spacing = desktop_vertical_spacing
        self.thumbnails = []
        self.current_width = page.width
        self._create_thumbnails()

        # ウィンドウサイズ変更時のイベントハンドラを登録
        self.page.on_resize = self._handle_resize

    def _get_image_files(self) -> list:
        if not WEB_FLAG:
            glob_pattern = os.path.join(self.images_dir, "*.*")
            image_files = glob.glob(glob_pattern)
        else:
            image_files = [
                "images/sample_sdxl_001.png",
                "images/sample_sdxl_002.png",
                "images/sample_sdxl_003.png",
                "images/sample_sdxl_004.png",
                "images/sample_sdxl_005.png",
                "images/sample_sdxl_006.png",
                "images/sample_sdxl_007.png",
                "images/sample_sdxl_008.png",
                "images/sample_sdxl_009.png",
                "images/sample_sdxl_010.png",
            ]
        return image_files

    def _calculate_responsive_layout(self) -> tuple:
        # モバイル判定（画面幅が800px未満）
        is_mobile = self.page.width < 800

        if is_mobile:
            # モバイルレイアウト
            images_per_row = 2
            horizontal_spacing = self.page.width / 2
            vertical_spacing = horizontal_spacing * 1.4  # アスペクト比を考慮
            thumbnail_width = horizontal_spacing * 0.9  # 余白を考慮
            thumbnail_height = thumbnail_width * 1.4
        else:
            # デスクトップレイアウト
            images_per_row = self.desktop_images_per_row
            horizontal_spacing = self.desktop_horizontal_spacing
            vertical_spacing = self.desktop_vertical_spacing
            thumbnail_width = 350
            thumbnail_height = 500

        return images_per_row, horizontal_spacing, vertical_spacing, thumbnail_width, thumbnail_height

    def _calculate_position(self, index: int) -> tuple:
        images_per_row, horizontal_spacing, vertical_spacing, _, _ = self._calculate_responsive_layout()
        row = index // images_per_row
        col = index % images_per_row
        left = col * horizontal_spacing
        top = row * vertical_spacing
        return left, top

    def _navigate_to_detail(self, image_path: str):
        self.page.go(f"/detail?path={image_path}")
        self.page.update()

    def _create_thumbnails(self):
        self.thumbnails.clear()
        image_files = self._get_image_files()
        _, _, _, thumbnail_width, thumbnail_height = self._calculate_responsive_layout()

        for index, image_path in enumerate(image_files):
            left, top = self._calculate_position(index)
            thumbnail = Thumbnail(
                image_path=image_path,
                left=left,
                top=top,
                width=thumbnail_width,
                height=thumbnail_height,
                on_click=self._navigate_to_detail,
            )
            self.thumbnails.append(thumbnail.gesture_detector)

    def _handle_resize(self, e):
        # 画面サイズが変更された場合にサムネイルを再配置
        if self.current_width != self.page.width:
            self.current_width = self.page.width
            self._create_thumbnails()
            self.page.update()


def main(page: ft.Page):
    page.title = "Image Viewer"
    page.padding = 0
    page.spacing = 0
    page.window_width = 800
    page.window_height = 600
    page.scroll = ft.ScrollMode.ALWAYS

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        if page.route == "/":
            image_viewer = ImageViewer(
                page=page,
                images_dir="assets/images",
                desktop_images_per_row=4,
                desktop_horizontal_spacing=400,
                desktop_vertical_spacing=600,
            )

            # コンテナサイズの計算
            images_per_row, horizontal_spacing, vertical_spacing, _, _ = image_viewer._calculate_responsive_layout()
            total_images = len(image_viewer._get_image_files())
            total_rows = (total_images + images_per_row - 1) // images_per_row
            container_width = images_per_row * horizontal_spacing
            container_height = total_rows * vertical_spacing

            # 余白を追加
            container_width += 50
            container_height += 50

            scroll_container = ft.Container(
                content=ft.Stack(
                    controls=image_viewer.thumbnails,
                ),
                width=container_width,
                height=container_height,
            )

            main_view = ft.View(
                route="/",
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[ft.Text("画像一覧", size=30, weight=ft.FontWeight.BOLD), scroll_container],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True,
                        ),
                        expand=True,
                    )
                ],
                padding=20,
            )
            page.views.append(main_view)

        else:
            image_path = page.route.split("?path=")[1]
            detail_view = ImageDetailView(page, image_path, WEB_FLAG)
            page.views.append(ft.View(route="/detail", controls=detail_view.controls))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")


ft.app(main)
# ft.app(main, view=ft.WEB_BROWSER)

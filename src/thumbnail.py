import flet as ft


class Thumbnail:
    def __init__(
        self, image_path: str, left: float = 0, top: float = 0, width: float = 350, height: float = 500, on_click=None
    ):
        self.image_path = image_path
        self.start_top = 0
        self.start_left = 0
        self.gesture_detector = self._create_gesture_detector(image_path, left, top, width, height, on_click)

    def _start_drag(self, e: ft.DragStartEvent):
        self.start_top = e.control.top
        self.start_left = e.control.left
        e.control.update()

    def _drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def _create_gesture_detector(
        self, image_path: str, left: float, top: float, width: float, height: float, on_click
    ) -> ft.GestureDetector:
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=self._start_drag,
            on_pan_update=self._drag,
            on_tap=lambda e: on_click(image_path) if on_click else None,
            left=left,
            top=top,
            content=ft.Container(bgcolor=ft.colors.WHITE, width=width, height=height, content=ft.Image(src=image_path)),
        )

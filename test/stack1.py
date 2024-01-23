from math import pi
import flet as ft
from flet_core import transform, Rotate

def main(page):
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="https://picsum.photos/100/100",
                    width=100,
                    height=100,
                    border_radius=5,
                    rotate=Rotate(angle=0.25 * pi, alignment=ft.alignment.center_left)
                ),
                ft.CircleAvatar(
                    foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
            expand=0
        )
    )

ft.app(target=main)
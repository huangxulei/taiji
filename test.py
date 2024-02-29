import flet as ft

audioListShown = False


def main(page: ft.Page):
    global audioListShown

    def showAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(0, 0)
        audioListShown = True
        audioList_menu.update()

    def hideAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(2, 0)
        audioListShown = False
        audioList_menu.update()

    # 播放列表
    def audioListCtrl(e):
        if audioListShown == False:
            showAudioList(0)
        elif audioListShown == True:
            hideAudioList(0)

    audioList_btn = ft.IconButton(
        icon=ft.icons.LIBRARY_MUSIC_OUTLINED,
        icon_size=20,
        on_click=audioListCtrl,
    )
    songlist_tiles = ft.Column(
        controls=[], height=380, spacing=0, scroll=ft.ScrollMode.AUTO
    )
    audioList_menu = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            value="播放列表",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.IconButton(icon=ft.icons.CLOSE, on_click=hideAudioList),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                songlist_tiles,
            ],
        ),
        right=10,
        bottom=65,
        width=300,
        height=350,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_radius=6,
        padding=8,
        offset=ft.transform.Offset(2, 0),
        animate_offset=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT_CUBIC),
    )

    page.overlay.append(audioList_menu)

    page.add(audioList_btn)


ft.app(target=main)

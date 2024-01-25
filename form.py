import flet as ft


class Form(ft.UserControl):  # PEP8: `UpperCasenames` for classes
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page  # to add `SnackBar`
        self.name_txt = ft.TextField(label="your name")

    def pickFile(self, e: ft.FilePickerResultEvent):
        if e.files:
            sections = {}
            sections["name"] = e.files[0].path
            print(sections)

            self.name_txt.value = sections["name"]
            self.update()  # to update elements in `UserControl`

            self.page.snack_bar = ft.SnackBar(
                ft.Text("sucess get from image", size=30), bgcolor="green"
            )
            self.page.snack_bar.open = True
            self.page.update()  # to update `self.page.snack_bar`
        else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("You didn't select image", size=30), bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()  # to update `self.page.snack_bar`

    def build(self):
        file_picker = ft.FilePicker(on_result=self.pickFile)
        self.page.overlay.append(file_picker)

        return ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(
                        "Process",
                        bgcolor="blue",
                        color="white",
                        on_click=file_picker.pick_files,
                    ),  # no need `lambda`
                    ft.Text("you result in image", weight="bold"),
                    self.name_txt,
                ]
            )
        )


def main(page: ft.Page):
    myform = Form(page)
    page.add(myform)
    # page.update()   # doesn't need it


ft.app(target=main)

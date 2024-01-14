from flet import *
import sqlite3


class Database(object):
    def ConnectToDatabase():
        try:
            db = sqlite3.connect("todo.db")
            c = db.cursor()
            c.execute(
                "CREATE TABLE if not exists tasks(id INTEGER PRIMARY KEY, task TEXT NOT NULL)"
            )
            return db
        except Exception as e:
            print(e)

    def ReadDatabase(db):
        c = db.cursor()
        c.execute("SELECT task FROM tasks")
        records = c.fetchall()
        return records

    def InsertIntoDatabase(db, value):
        c = db.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", value)
        db.commit()

    def DeleteTaskFromDatabase(db, value):
        c = db.cursor()
        c.execute(""" DELETE FROM tasks WHERE Task=?""", value)
        db.commit()


task_list = Column(
    controls=[]
)
class Task(UserControl):
    def __init__(self, input_text):
        self.input = input_text
        super().__init__()
        self.tasklist = task_list

    def build(self):
        self.task = Container(
            border=border.all(0.85, "white54"),
            border_radius=8,
            padding=10,
            content = Row(

                [
                    Text(value=self.input),
                    IconButton(icon=icons.DELETE_ROUNDED, icon_color = "red400", on_click=self.remove)
                    ],
                alignment = MainAxisAlignment.SPACE_BETWEEN
            )
        )
        return self.task

    def remove(self, e):
        self.tasklist.controls.remove(self)

        db = Database.ConnectToDatabase()
        Database.DeleteTaskFromDatabase(db, (self.input,))
        db.close()

        self.tasklist.update()
class App(UserControl):
    def build(self):
        self.textfield = TextField(label='Введите название задачи', border_radius=15, border_color = 'WHITE')
        self.tasklist = task_list
        main_column = Container(
            width=1500,
            height=900,
            margin=-10,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=280,
                        height=600,
                        bgcolor="#0f0f0f",
                        border=border.all(0.5, "white70"),
                        border_radius=40,
                        padding=padding.only(top=35, left=20, right=20),
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True,
                            controls=[
                                Column (
                                    scroll="hidden",
                                    expand=True,
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                Text(
                                                    "Добавить задачу",
                                                    size=20,
                                                    weight="bold",
                                                ),
                                                IconButton(
                                                    icons.ADD_CIRCLE_ROUNDED, icon_size=20, on_click=self.add),
                                            ],
                                        ),
                                        self.textfield,
                                        self.tasklist
                                    ]
                                )
                            ],
                        ),
                    ),
                ],
            )
        )

        return main_column

    def add(self, e):
        if not self.textfield.value:
            self.textfield.error_text = 'Задача не может быть пустой'
            self.update()
        else:
            self.textfield.error_text = None
            self.update()

            self.tasklist.controls.append(Task(self.textfield.value))

            db = Database.ConnectToDatabase()
            Database.InsertIntoDatabase(db, (self.textfield.value,))
            db.close()

            self.textfield.value = None
            self.update()

def main(page: Page):
    app = App()
    page.add(app)


    db = Database.ConnectToDatabase()
    for task in Database.ReadDatabase(db):
        task_list.controls.append(
            Task(
                task[0],
            )
        )
    task_list.update()



if __name__ == '__main__':
    app(target=main)
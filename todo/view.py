from .config import get_db_path

def display(todo_list: list):
    RESET_COLOR = '\033[0m'
    BOLD        = '\033[01m'
    RED         = '\033[31m'
    BLUE        = '\033[34m'
    title = get_db_path().stem
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)

    if len(todo_list) == 0:
        print(RED, f'The to-do list "{title}" is empty', RESET_COLOR, sep='')
    else:
        print(BLUE, BOLD, f'"{title}":\n',sep='')
        print(headers, RESET_COLOR, BLUE)
        # to cancel the bold and re-enstate the blue
        print("-" * len(headers))
        for id, todo in enumerate(todo_list, 1):
            desc, priority, done = todo.values()
            print(
                f"{RED if not done else BLUE}"
                f"{id}{' ' * (len(columns[0]) - len(str(id)))}"
                f"| ({priority}){' ' * (len(columns[1]) - len(str(priority)) - 4)}"
                f"| {done}{' ' * (len(columns[2]) - len(str(done)) - 2)}"
                f"| {desc}",
                sep='')
        print("-" * len(headers) + "\n", RESET_COLOR)
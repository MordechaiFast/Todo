from .config import get_db_path

def display(todo_list: list):
    RESET_COLOR = '\33[0m'
    BOLD        = '\33[01m'
    RED         = '\33[31m'
    GREEN       = '\33[32m'
    YELLOW      = '\33[33m'
    BLUE        = '\33[34m'
    WHITEBG     = '\33[47m'

    title = get_db_path().stem
    columns = (
        "ID. ",
        "| (P) ",
        "| Description  ",
    )
    headers = "".join(columns)

    if len(todo_list) == 0:
        print(RED, f'The to-do list "{title}" is empty', RESET_COLOR, sep='')
    else:
        print(BLUE, BOLD, f'"{title}":\n',sep='')
        print(headers, RESET_COLOR) # to cancel the bold
        print("-" * len(headers))
        for id, todo in enumerate(todo_list, 1):
            desc, priority, done = todo.values()
            print(
                f"{BLUE if done else RED if priority >= 2 else GREEN}"
                f"{id}{' ' * (len(columns[0]) - len(str(id)))}"
                f"| ({priority if not done else '-'}) "
                f"| {desc}",
                sep='')
        print(BLUE, "-" * len(headers) + "\n", RESET_COLOR, sep='')
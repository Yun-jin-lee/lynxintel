from app.adapters.lynx_client import open_with_lynx


def handle_open(user_input: str, dump: bool = False) -> int:
    return open_with_lynx(user_input, dump=dump)
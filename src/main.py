def do_thing(a: float, b: float, c: float) -> str:
    """
    do_thing

    It works with MKdocs and here I can write markdown:

    - list of things to do
    - some more lists
    - [ ] checkbox?
    - [x] A checked checkbox!

    `code to write here as follows `

    Args:
        a (float): The first number
        b (float): the second number
        c (float): number the third

    Returns:
        str: a string is returned because why not
    """
    if c:
        return str(a/b)


if __name__ == '__main__':
    print("running main")

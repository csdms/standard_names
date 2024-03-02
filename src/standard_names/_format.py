from collections.abc import Iterable


def as_wiki_list(items: Iterable[str], heading: str | None = None, level:int=1) -> str:
    """
    Examples
    --------
    >>> from standard_names._format import as_wiki_list

    >>> print(as_wiki_list(["line 1", "line 2"], heading="Lines"))
    = Lines =
    <tt>
    line 1<br/>
    line 2<br/>
    </tt>
    """
    newline = "\n"

    if heading is not None:
        formatted_lines = [f"{'=' * level} {heading} {'=' * level}"]
    else:
        formatted_lines = []

    formatted_lines += ["<tt>"] + [item.strip() + "<br/>" for item in items] + ["</tt>"]

    return newline.join(formatted_lines)


def as_yaml_list(items: Iterable[str], heading: str | None = None, level:int=1) -> str:
    """

    Examples
    --------
    >>> from standard_names._format import as_yaml_list

    >>> print(as_yaml_list(["line 1", "line 2"], heading="Lines"))
    Lines:
      - line 1
      - line 2
    """
    newline = "\n"
    indent = 2 if heading else 0
    formatted_lines = [f"{heading}:"] if heading else []

    if heading is None:
        formatted_lines = []
        indent = 0
    else:
        formatted_lines = [f"{heading}:"]
        indent = 2

    stripped_items = [stripped for item in items if (stripped := item.strip())]

    if stripped_items:
        formatted_lines += [f"{' ' * indent}- {item}" for item in stripped_items]
    else:
        formatted_lines += [f"{' ' * indent}[]"]

    return newline.join(formatted_lines)


def as_myst_list(items: Iterable[str], heading: str | None = None, level:int=1) -> str:
    """

    Examples
    --------
    >>> from standard_names._format import as_myst_list

    >>> print(as_myst_list(["line 1", "line 2"], heading="Lines"))
    # Lines
    * line 1
    * line 2
    """
    newline = "\n"

    formatted_lines = ([f"# {heading}"] if heading else []) + [f"* {stripped}" for item in items if (stripped := item.strip())]

    return newline.join(formatted_lines)


def as_text_list(items: Iterable[str], heading: str | None = None, level:int=1) -> str:
    """

    Examples
    --------
    >>> from standard_names._format import as_text_list

    >>> print(as_text_list(["line 1", "line 2"], heading="# Lines"))
    # Lines
    line 1
    line 2
    """
    newline = "\n"

    formatted_lines = ([heading] if heading else []) + [
        stripped for item in items if (stripped := item.strip())
    ]

    return newline.join(formatted_lines)


FORMATTERS = {
    "wiki": as_wiki_list,
    "yaml": as_yaml_list,
    "text": as_text_list,
    "myst": as_myst_list
}


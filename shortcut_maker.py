import sys
from utils import Directory, Link, Print, DirType, Strings, Globals, Shortcut, Lists
import traceback


def clean_shortcuts(link: Link):
    """
    Recursive function to clean a shortcut folder structure of old links and folders.
    Removes empty folders at higher levels.
    Removes unresolvable shortcuts at the deepest level.    
    """
    folder = link.traversing.path
    if not folder.exists():
        return

    for file in folder.iterdir():
        link.set_path(file)
        # print(link)
        # At higher levels.
        if not link.complete:
            if file.is_dir():
                clean_shortcuts(link.deeper)
            continue

        # At the deepest level.
        if not Shortcut.is_shortcut(file):
            continue

        shortcut = Shortcut(file)
        if not shortcut.resolves:
            shortcut.remove()
            Print.action(f"Removed shortcut: {file}")

    # Remove empty folders of higher levels.
    if not any(folder.iterdir()):
        folder.rmdir()
        Print.action(f"Removed folder: {folder}")


def create_shortcuts(link: Link):
    """
    Recursive function to create a new folder structure in the given format.
    At the deepest level create a shortcut to each folder.
    """
    folder = link.traversing.path
    for file in folder.iterdir():
        if not file.is_dir():
            continue

        link.set_path(file)
        # At higher levels.
        if not link.complete:
            create_shortcuts(link.deeper)
            continue

        # At deepest level.
        shortcut_path = link.complete_path
        if not shortcut_path.exists():
            link.create()
            Print.action(f"Shortcut created: {shortcut_path} -> {file}")


def get_parameters() -> tuple[Directory, Directory]:
    """
    Validates the commandline arguments and returns a link object.
    Raises an Error for invalid arguments.
    """
    # Validate amount of arguments
    usage_message = f"python {sys.argv[0]} <target_path> <target_format> <shortcut_path> <shortcut_format>"
    if len(sys.argv) != 5:
        raise ValueError(usage_message)

    # Validate target and shortcut arguments.
    target_path = Strings.get_path(sys.argv[1], does_exist=True)
    target_format = Strings.get_format(sys.argv[2])
    shortcut_path = Strings.get_path(sys.argv[3], does_exist=False)
    shortcut_format = Strings.get_format(sys.argv[4])

    # Validate format lists.
    if not Lists.same_elements(target_format, shortcut_format):
        raise ValueError(
            f"Formats need to contain the same elements: {target_format}, {shortcut_format}")

    # Put all arguments together.
    shortcut = Directory(DirType.SHORTCUT, shortcut_path, shortcut_format)
    target = Directory(DirType.TARGET, target_path, target_format)

    return target, shortcut


def main():
    """Retrieve parameters and execute functions."""
    try:
        target, shortcut = get_parameters()
        target_link = Link(target, shortcut)
        shortcut_link = Link(shortcut, target)
    except Exception as e:
        Print.usage(str(e))

    try:
        clean_shortcuts(shortcut_link)
        create_shortcuts(target_link)
        pass
    except Exception as e:
        Print.error(str(e))
        # print(traceback.format_exc())

    if Globals.no_changes:
        Print(f"No changes made to: '{target_link.building.path}'")


if __name__ == "__main__":
    main()

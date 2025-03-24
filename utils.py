import sys
import os
import re
import unicodedata
import win32com.client  # or pyshortcuts
from pathlib import Path
from collections import Counter
import copy
from typing import Callable, Any
from enum import Enum


class Globals:
    """Variables that can be set globally."""
    no_changes = True


class DirType(Enum):
    """Describes the type of directory."""
    TARGET = "target"
    SHORTCUT = "shortcut"


class Strings:
    """String methods"""
    @staticmethod
    def clean_path(string: str) -> str:
        """Clean a string from a .bat source by removing non-visible and unusual characters."""
        # Strip common unwanted characters
        string = string.strip(' "\t\n\r')

        # Remove all control and non-printable characters
        string = "".join(ch for ch in string if ch.isprintable())

        # Normalize Unicode (removes zero-width spaces, etc.)
        string = unicodedata.normalize("NFKC", string)

        # Check for forbidden characters (e.g., < > : " | ? *), or empty string.
        forbidden_chars = r'[<>:"|?*]'
        if re.search(forbidden_chars, string):
            raise ValueError(
                f"Argument contains invalid characters(< > : \" | ? *): '{string}'")
        elif not string:
            raise ValueError(f"Argument invalid: '{string}'")

        return string

    @staticmethod
    def get_path(string: str, does_exist: bool = False) -> Path:
        """Converts a string to a Path object and optionally checks if the path exists."""
        string = Strings.clean_path(string)
        path = Path(string)

        if does_exist and not path.exists():
            raise FileNotFoundError(f"File not found: {string}")

        return path

    @staticmethod
    def get_format(string: str) -> list:
        """
        Clean and validate the string and return a list with path parts.
        'name/year' -> ['name', 'year']
        """
        string = Strings.clean_path(string)
        format = Strings.get_path(string).parts

        if Lists.has_duplicates(format):
            raise ValueError(
                f"Format argument can't contain duplicate elements: {format}")

        return format


class Lists:
    """List methods"""
    @staticmethod
    def has_duplicates(list1: list) -> bool:
        """Return true when the input list has duplicate elements."""
        return len(list1) != len(set(list1))

    @staticmethod
    def same_elements(list1: list, list2: list) -> bool:
        """Same elements, same count, order can be different."""
        return Counter(list1) == Counter(list2)

    @staticmethod
    def for_each(items: list[Any], callback: Callable[[Any], Any]) -> list:
        """Execute the function for each item in the list, return list with results."""
        results = []
        for item in items:
            result = callback(item)
            results.append(result)
        return results


class Shortcut:
    """Handle Windows shortcut files."""

    def __init__(
            self,
            path: Path
    ):
        self.shortcut_path = path
        self._object = self._get_object()

    def _get_object(self):
        """Initializes and returns the Windows shortcut object."""
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut_str = str(self.shortcut_path)
        return shell.CreateShortcut(shortcut_str)

    @staticmethod
    def is_shortcut(file: Path) -> bool:
        """Returns True when the given file is a shortcut file."""
        return file.with_suffix(".lnk")

    @property
    def target_path(self) -> Path:
        """Returns the target path of the shortcut."""
        return Path(self._object.TargetPath)

    @target_path.setter
    def target_path(self, path: Path):
        """Set the target path of the shortcut."""
        self._object.TargetPath = str(path.resolve())

    @property
    def exists(self) -> bool:
        """Returns True if the shortcut exists."""
        return self.shortcut_path.exists()

    @property
    def resolves(self) -> bool:
        """Returns True when the target of the shortcut exists."""
        return self.target_path.exists()

    def remove(self) -> None:
        """Deletes the shortcut file safely."""
        self.shortcut_path.unlink(missing_ok=True)

    def create(self) -> None:
        """Writes the shortcut file and its folder structure to disk."""
        self.shortcut_path.parent.mkdir(parents=True, exist_ok=True)
        self._object.Save()


class Directory:
    """Describes a folderstructure for shortcut or target."""

    def __init__(
            self,
            dir_type: DirType,
            path: Path,
            format: list
    ):
        self.dir_type = dir_type
        self.path = path
        self.format = format

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return Objects.str(self)


class Link:
    """
    Describes the connection between a target and a shortcut.
    Can be used recursively to create a path that references a directory.
    """

    def __init__(
        self,
        traversing: Directory,
        building: Directory
    ):
        self.traversing = traversing.copy()
        self.building = building.copy()
        self.level = 0
        depth = len(traversing.format)
        self.path_parts = ['' for _ in range(depth)]
        self.complete = all(self.path_parts)
        self.complete_path = False

    def set_path(self, path: Path) -> None:
        """Sets the directory name in the right position in path_parts."""

        # Remove the .lnk extension from shortcuts to find the target.
        if self.traversing.dir_type == DirType.SHORTCUT:
            path = path.with_suffix("")
        self.traversing.path = path

        # Insert parts into part_parts.
        category = self.traversing.format[self.level]
        index = self.building.format.index(category)
        self.path_parts[index] = self.traversing.path.name
        if all(self.path_parts):
            self.complete = True
            self._build_path()

    def _build_path(self) -> None:
        """Constructs a path out of path_parts."""
        path = self.building.path
        path = path.joinpath(*self.path_parts)
        if self.building.dir_type == DirType.SHORTCUT:
            path = path.with_suffix(".lnk")
        self.complete_path = path

    def create(self) -> None:
        """Creates a shortcut based on the completed path."""
        target_path, shortcut_path = self.traversing.path, self.complete_path
        shortcut = Shortcut(shortcut_path)
        shortcut.target_path = target_path
        shortcut.create()

    @property
    def deeper(self):
        """Creates a deep copy with updated level and target path."""
        deeper_link = self.copy()
        deeper_link.level += 1
        return deeper_link

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return Objects.str(self)


class Print:
    """Object and functions for printing messages."""

    def __init__(self, message: str, prefix: str = "", exit: bool = False):
        self.message = message
        self.prefix = prefix
        self.exit = exit
        self._display()

    def _display(self):
        """Displays the message with the prefix and optionaly exit program."""

        if self.prefix == "":
            print(self.message)
        else:
            print(f"{self.prefix}: {self.message}")

        if self.exit:
            sys.exit(1)

    @staticmethod
    def usage(message: str):
        """Print an usage message and exit."""
        Print(message, prefix="Usage", exit=True)

    @staticmethod
    def action(message: str):
        """Print action message and set Globals."""
        Globals.no_changes = False
        Print(message)

    @staticmethod
    def warning(message: str):
        """Print warning message and continue."""
        Print(message, prefix="Warning")

    @staticmethod
    def error(message: str):
        """Print error message and exit."""
        Print(message, prefix="Error", exit=True)


class Objects:
    """Functions for objects."""
    @staticmethod
    def str(obj):
        """Will return a string with all the attributes and values of an object."""
        classname = obj.__class__.__name__
        pairs = vars(obj).items()
        content = ', '.join(f'{k}={v}' for k, v in pairs)
        return f"{classname}({content})"

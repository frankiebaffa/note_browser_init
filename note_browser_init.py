#!python3
from argparse import ArgumentParser
import os
from typing import List
from pathlib import Path
class NestPath:
    """
    Tracks the nesting of the current path from root
    """

    nest: List[str] = []

    def __init__(self):
        self.nest = []

    def add(self, path: str):
        """
        Add a path to the end of nest
        """

        self.nest.append(path)

    def pop(self):
        """
        Removes the final element from the nest
        """

        self.nest.pop(len(self.nest) - 1)

class Context:
    """
    The context of the program
    """

    @staticmethod
    def parse_args():
        """
        Parses command line arguments
        """

        desc = "Create index.md files for all directories in path"
        parser = ArgumentParser(description=desc)
        parser.add_argument("--path", dest="path", required=True,
                            help="The absolute path of the notes directory")
        return parser.parse_args()

class Program:
    """
    The program proper
    """

    @staticmethod
    def wo_file_ext(filename: str) -> str:
        """
        Removes the file extension from a filename or file path
        """

        return os.path.splitext(filename)[0]

    @staticmethod
    def to_title_case(snake: str) -> str:
        """
        Transforms a lower-snake-cased string into a title-cased string
        """

        return snake.replace("_", " ").title()

    @staticmethod
    def default_ignore_dirs() -> List[str]:
        """
        The default directories to ignore
        """

        script_dir = os.path.abspath(__file__)
        script_dir = os.path.split(script_dir)[0]
        return [
            script_dir
        ]

    @staticmethod
    def default_ignore_files() -> List[str]:
        """
        The default files to ignore
        """

        return [
            "index.md"
        ]

    @staticmethod
    def chk_dir(root: str) -> bool:
        """
        Checks a directory for nested markdown files
        """

        is_good = False
        if os.path.isdir(root):
            for item in os.listdir(root):
                abspath = os.path.join(root, item)
                if os.path.isfile(abspath):
                    if os.path.splitext(abspath)[1] == ".md":
                        is_good = True
                        break
                elif os.path.isdir(abspath):
                    if Program.chk_dir(abspath):
                        is_good = True
                        break
                else:
                    continue
        return is_good

    @staticmethod
    def generate_nav_section(root: str, nest: NestPath):
        """
        Creates a navigation section at the top of the file, complete with path
        and document name
        """

        if nest is None:
            nest = NestPath()
        nest.add(root)
        has_file = False
        has_dir = False
        file_output = ""
        dir_output = ""
        for filename in os.listdir(root):
            abspath = os.path.join(root, filename)
            if os.path.isfile(abspath):
                if os.path.splitext(filename)[1] != ".md":
                    continue
                if not has_file:
                    has_file = True
                gen_start = "<!--AUTO GENERATED-->"
                gen_end = "<!--/AUTO GENERATED-->"
                the_rest: str = None
                with open(abspath, "r") as file:
                    contents = file.read()
                    start = contents.find(gen_start)
                    end = contents.find(gen_end)
                    if start != -1 and end != -1:
                        the_rest = contents[end + len(gen_end):
                                            len(contents)].strip()
                    else:
                        the_rest = contents.strip()
                    file.close()
                nav_path: str = "`Path:` "
                dlim: str = ""
                doc_non_title = os.path.splitext(os.path.split(abspath)[1])[0]
                document = Program.to_title_case(doc_non_title)
                for i in range(len(nest.nest)):
                    path = nest.nest[i]
                    name: str = None
                    if i == 0:
                        name = "root"
                    else:
                        name = os.path.split(path)[1]
                    relative = os.path.split(os.path.relpath(path, abspath))[0]
                    if relative == "":
                        relative = relative + "index.md"
                    else:
                        relative = relative + "/index.md"
                    nav_path = f"{nav_path}{dlim}[{name}]({relative})"
                    dlim = " / "
                if doc_non_title != "index":
                    nav_path = f"{nav_path}{dlim}[{doc_non_title}]({doc_non_title}.md)"
                document = f"`Document:` {document}"
                new_content = f"{gen_start}\n"
                new_content = f"{new_content}{nav_path}\n\n"
                new_content = f"{new_content}{document}\n\n"
                new_content = f"{new_content}{gen_end}\n"
                new_content = f"{new_content}{the_rest}\n"
                with open(abspath, "w") as file:
                    file.truncate(0)
                    file.write(new_content)
                print("Generated nav for " + abspath)
            elif os.path.isdir(abspath):
                if abspath in Program.default_ignore_dirs():
                    continue
                if not Program.chk_dir(abspath):
                    continue
                Program.generate_nav_section(abspath, nest)
                continue
        nest.pop()
        return

    @staticmethod
    def create_index_from_dir(root: str):
        """
        Recursively checks internal directories and generates index.md files
        """

        has_file = False
        has_dir = False
        file_output = ""
        dir_output = ""
        for filename in os.listdir(root):
            abspath = os.path.join(root, filename)
            relpath = os.path.join("", filename)
            if os.path.isfile(abspath):
                if os.path.splitext(filename)[1] != ".md":
                    continue
                if filename in Program.default_ignore_files():
                    continue
                if not has_file:
                    file_output = "## Files\n"
                    has_file = True
                display_file_name = Program.to_title_case(
                    Program.wo_file_ext(filename))
                file_output = f"{file_output}\n- [{display_file_name}]({relpath})"
                continue
            elif os.path.isdir(abspath):
                if abspath in Program.default_ignore_dirs():
                    continue
                if not Program.chk_dir(abspath):
                    continue
                if not has_dir:
                    dir_output = "## Directories\n"
                    has_dir = True
                link_path = os.path.join(relpath, "index.md")
                title_cased = Program.to_title_case(filename)
                dir_output = f"{dir_output}\n- [{title_cased}]({link_path})"
                Program.create_index_from_dir(abspath)
                continue
            else:
                continue
        output = "# ToC\n"
        if dir_output:
            output = f"{output}\n{dir_output}\n"
        if file_output:
            output = f"{output}\n{file_output}\n"
        index_path = os.path.join(root, "index.md")
        if not os.path.isfile(index_path):
            with open(index_path, "w") as file:
                file.write(output)
        elif os.path.isfile(index_path):
            os.remove(index_path)
            with open(index_path, "w") as file:
                file.write(output)
        else:
            print(f"\"{index_path}\" is not a file")
        return

def main():
    """
    The main function of the program
    """

    root = Context.parse_args().path
    if not root or root is None:
        print("Argument \"path\" not included")
        return
    Program.create_index_from_dir(root)
    Program.generate_nav_section(root, None)

if __name__ == "__main__":
    main()

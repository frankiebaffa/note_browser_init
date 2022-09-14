#!python3
from argparse import ArgumentParser
import os
from typing import List
from pathlib import Path
class Context:
    @staticmethod
    def parse_args():
        desc = "Create index.md files for all directories in path"
        parser = ArgumentParser(description=desc)
        parser.add_argument("--path", dest="path", required=True,
                            help="The absolute path of the notes directory")
        return parser.parse_args()
class Program:
    @staticmethod
    def wo_file_ext(filename: str) -> str:
        return os.path.splitext(filename)[0]
    @staticmethod
    def to_title_case(snake: str) -> str:
        return snake.replace("_", " ").title()
    @staticmethod
    def default_ignore_dirs() -> List[str]:
        script_dir = os.path.abspath(__file__)
        script_dir = os.path.split(script_dir)[0]
        return [
            script_dir
        ]
    @staticmethod
    def default_ignore_files() -> List[str]:
        return [
            "index.md"
        ]
    @staticmethod
    def chk_dir(root: str) -> bool:
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
    def create_index_from_dir(root: str):
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
                return
        elif os.path.isfile(index_path):
            os.remove(index_path)
            with open(index_path, "w") as file:
                file.write(output)
                return
        else:
            print(f"\"{index_path}\" is not a file")
            return
def main():
    root = Context.parse_args().path
    if not root or root is None:
        print("Argument \"path\" not included")
        return
    Program.create_index_from_dir(root)
if __name__ == "__main__":
    main()

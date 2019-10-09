import os
from pathlib import Path
from gooey import Gooey, GooeyParser


def rename_file(dir_to_walk: str, str_to_add: str = None, file_suffix: [str] = None) -> [(str, str)]:
    files_to_rename = []

    if str_to_add == '------':
        str_to_add = f"{Path(dir_to_walk).name} -"

    # todo error - suffix is case sensitive...jpg was JPG
    if file_suffix:
        [[files_to_rename.append((os.path.join(d, i), os.path.join(d, f"{str_to_add} {i}"))) for i in f if Path(i).
            suffix in file_suffix] for d, e, f in os.walk(dir_to_walk)]
    else:
        [[files_to_rename.append((os.path.join(d, i), os.path.join(d, f"{str_to_add} {i}"))) for i in f]
         for d, e, f in os.walk(dir_to_walk)]
    [os.rename(i[0], i[1]) for i in files_to_rename]
    return files_to_rename


@Gooey(program_name='File Renamer')
def main():
    parser = GooeyParser()
    parser.add_argument("Directory", help="Select a directory", widget='DirChooser')
    pattern_group = parser.add_argument_group(
        "Pattern",
        "Type the string of chars to add to the files",
    )
    pattern_group.add_argument('Pattern', help="Leave '------' to use the folder name, else please enter a name to add "
                                               "to the beginning of the file(s)", default='------')
    # https://github.com/chriskiehl/Gooey#input-validation
    # todo - get the file extensions that exist in the directory
    choices = sorted(['.xlsx', '.PNG', '.docx', '.JPEG', '.xls', '.doc', '.txt', '.msg'])
    pattern_group.add_argument('Extension', help="select the type of files to change...", widget='Listbox', nargs='+',
                               choices=choices)
    args = parser.parse_args()
    print(args)
    print("\n")
    files = rename_file(dir_to_walk=args.Directory, str_to_add=args.Pattern, file_suffix=args.Extension)

    [print(f"Changed '{Path(orig_name).name}' to...\t'{Path(new_name).name}'") for orig_name, new_name in files]

    if not files:
        print(f"Sorry, no files in the directory of type: {', '.join(args.Extension)}")


if __name__ == '__main__':
    main()

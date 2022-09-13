import json
import os
import re
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# TODO: What does the parser output, when the file is not an ifg at all?


def write_input_file(ifgs: list[str]) -> None:
    with open(f"{PROJECT_DIR}/parser/ifg_parser.template.inp", "r") as f:
        template_content = f.read()
    with open(f"{PROJECT_DIR}/parser/ifg_parser.inp", "w") as f:
        f.write(template_content.replace("%IFG_LIST%", "\n".join(ifgs)))


def run(ifg_directory: str, silent: bool = True) -> dict[str, list[str]]:
    # generate input file
    ifgs = [f"{ifg_directory}/{x}" for x in os.listdir(ifg_directory)]
    ifgs = list(sorted(list(filter(os.path.isfile, ifgs))))

    results: dict[str, list[str]] = {}

    # run the parser
    while True:
        write_input_file(ifgs)
        process = subprocess.run(
            ["./ifg_parser", "ifg_parser.inp"],
            cwd=f"{PROJECT_DIR}/parser",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = process.stdout.decode()
        stderr = process.stderr.decode()
        if process.returncode == 0:
            break
        else:
            failing_filenames = list(filter(lambda f: f in ifgs, stderr.split("'")))
            assert (
                "At line 837 of file ifg_parser.F90" in stderr
            ), f"Unknown error behavior: {stderr}"
            assert len(failing_filenames) == 1, "invalid filename not found in stderr"
            failing_filepath = failing_filenames[0]
            ifgs.remove(failing_filepath)
            failing_filename = failing_filepath.split("/")[-1]
            results[failing_filename] = ["file not processable"]
            if not silent:
                print(f'error with file "{failing_filename}", running again')

    with open(f"{PROJECT_DIR}/parser/output.txt", "w") as f:
        f.write(stdout)

    file_parsing_block = stdout.split("Done!")[-1]
    file_parsing_lines = file_parsing_block.split("Read OPUS parms:")[1:]

    # get results from output stream
    for line in file_parsing_lines:
        n = int(line[:12].replace(" ", ""))
        filename = line[12:].split("\n")[0].split("/")[-1].replace(")", "")
        parser_output = line[12:].replace("\n", " ")
        parser_messages = re.findall('charfilter "[^"]+" is missing', parser_output)
        if len(parser_messages) > 0:
            results[filename] = [
                ("charfilter '" + x.split('"')[1] + "' is missing")
                for x in parser_messages
            ]

    return results


if __name__ == "__main__":
    # example usage
    results = run(
        "/home/esm/em27_ifg_dss/proffast-archive/me/ifgs/20220514", silent=False
    )

    if len(results) > 0:
        print("The corrupt ifgs are: ")
        print(json.dumps(results, indent=4))
    else:
        print("No corrupt ifgs found.")

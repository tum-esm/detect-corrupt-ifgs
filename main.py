import json
import os
import re
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# TODO: What does the parser output, when the file is not an ifg at all?


def run(ifg_directory: str):
    # generate input file
    ifgs = [f"{ifg_directory}/{x}" for x in os.listdir(ifg_directory)]
    ifgs = list(sorted(list(filter(os.path.isfile, ifgs))))
    with open(f"{PROJECT_DIR}/parser/ifg_parser.template.inp", "r") as f:
        template_content = f.read()
    with open(f"{PROJECT_DIR}/parser/ifg_parser.inp", "w") as f:
        f.write(template_content.replace("%IFG_LIST%", "\n".join(ifgs)))

    # run the parser
    execution_output = subprocess.check_output(
        ["./ifg_parser", "ifg_parser.inp"], cwd=f"{PROJECT_DIR}/parser"
    )
    file_parsing_block = execution_output.decode().split("Done!")[-1]
    file_parsing_lines = file_parsing_block.split("Read OPUS parms:")[1:]
    results = {}

    # get results from output stream
    for line in file_parsing_lines:
        n = int(line[:12].replace(" ", ""))
        parser_output = line[12:].replace("\n", " ")
        parser_messages = re.findall('charfilter "[^"]+" is missing', parser_output)
        if len(parser_messages) > 0:
            ifg_name = ifgs[n - 1].split("/")[-1]
            results[ifg_name] = [x.split('"')[1] for x in parser_messages]

    return results


if __name__ == "__main__":
    # example usage
    results = run("/home/esm/em27_ifg_dss/proffast-archive/mb/ifgs/20220421")

    if len(results) > 0:
        print("The corrupt ifgs are: ")
        print(json.dumps(results, indent=4))
    else:
        print("No corrupt ifgs found.")

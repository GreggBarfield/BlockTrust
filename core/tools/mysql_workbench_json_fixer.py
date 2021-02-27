import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Fix a CSV from MySQL Workbench.
        This assumes that the only DQ that need to be escaped are delimited by
            "[
        and
            ]"
        '''
    )

    parser.add_argument('-i', '--inf', help='Input file', type=str, required=True)
    parser.add_argument('-o', '--outf', help='Output file', type=str, required=True)

    args = parser.parse_args()

    input_file = open(args.inf)
    output_file = open(args.outf, "w+")

    print("Converting to DQ...")

    for line in input_file:
        line = line.strip("\r\n")

        if '""[""' in line or '""]""' in line:
            print("Skipping", line)
            continue

        fragments = line.split('"[')

        result = ""

        for fragment in fragments:
            if ']"' in fragment:
                a, b = fragment.split(']"')
                result += '"[' + a.replace('"', '""') + ']"' + b
            else:
                result += fragment

        output_file.write(result + "\n")

    input_file.close()
    output_file.close()

    print("Finished converting.")

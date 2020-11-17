import argparse
from fontTools.ttLib import TTFont

from os import walk
from os.path import splitext, join



def convert(file_path):
	f = TTFont(file_path)
	f.flavor = 'woff2'
	f.save(splitext(file_path)[0] + ".woff2")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert a directory from ttf to woff2.')
	parser.add_argument('dir', help='directory to convert', type=str)
	args = parser.parse_args()

	for root, dirs, files in walk(args.dir):
		for file in files:
			path = join(root, file)
			if splitext(file)[1] == ".ttf":
				print("converting", path)
				convert(path)
			else:
				print("ignoring", path)


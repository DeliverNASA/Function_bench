import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-message', type=str, default=None)
args = parser.parse_args()

if __name__ == "__main__":
    print(args.message)
    
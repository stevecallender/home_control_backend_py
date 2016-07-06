from Casting import *
from Seizing import *
import time

def main():
	caster = Caster("MediaCommand")

	while True:
		caster.cast("play")
		time.sleep(1)


if __name__ == "__main__":
	main()
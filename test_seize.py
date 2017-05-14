from Casting import *
from Seizing import *

def main():

	interestedIdentifiers = ["MediaInfo"]
	seizer = Seizer()
	seizer.configureSeizer(interestedIdentifiers,True)
        while True:
		[header, payload] = seizer.seize(False)
		print header
		time.sleep(3)



if __name__ == "__main__":
	main()

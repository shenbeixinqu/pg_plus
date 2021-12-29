import random


def generate_code():
	seeds = "1234567890"
	random_num = []
	for i in range(4):
		random_num.append(random.choice(seeds))
	return "".join(random_num)

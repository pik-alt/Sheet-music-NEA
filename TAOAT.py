def is_six(num: int) -> bool:
	"""Returns whether number is six."""
	not_factor: int = 0
	for i in range(2, num):
		if num % i != 0: not_factor += 1
	return not_factor == 2

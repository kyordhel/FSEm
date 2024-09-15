#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import math

def power_factor(alpha):
	result = math.sin(2.0 * alpha)/2.0
	result+= math.pi - alpha
	result/= math.pi
	return math.sqrt(result)

def a2t(alpha, freq = 60):
	return alpha / (2 * math.pi * freq)

def main():
	N = 10000
	d = {}
	# Calculate N phase variation in the range [0,pi]
	for i in range(0, N):
		alpha = i * math.pi / N
		pf = "{0:.2f}".format(100 * power_factor(alpha))
		t = "{0:.3f}ms".format(1000 * a2t(alpha))
		if pf not in d:
			d[pf] = t
			print("{}: {}".format(pf, t))

if __name__ == '__main__':
	main()

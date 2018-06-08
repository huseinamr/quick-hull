from random import randint
import matplotlib.pyplot as plt
import numpy as np

def distance(x1, y1, x2, y2, x3, y3):
	# p1 = (x1, y1), p2 = (x2, y2), p3 = (x3, y3)
	# mengembalikan jarak p3 ke garis yg dibentuk oleh p1 dan p2
	num = abs((y2-y1)*x3 - (x2 - x1)*y3 + x2*y1 - y2*x1)
	denom = ((y2-y1)**2 + (x2-x1)**2)**0.5

	return num / denom

def position(x1, y1, x2, y2, x3, y3):
	# p1 = (x1, y1), p2 = (x2, y2), p3 = (x3, y3)
	# mengembalikan posisi p3 relatif terhadap garis yg dibentuk oleh p1 dan p2
	# jika nilai negatif, maka p3 terletak di sebelah kiri (bawah) garis
	# jika nilai nol, maka p3 terletak pada garis
	# jika nilai positif, maka p3 terletak di sebelah kanan (atas) garis
	return x1*y2 + x2*y3 + x3*y1 - x3*y2 - x2*y1 - x1*y3

def angle(x1, y1, x2, y2, x3, y3):
	# p1 = (x1, y1), p2 = (x2, y2), p3 = (x3, y3)
	# mengembalikan nilai sudut p1 p2 p3
	a = np.array([x1, y1])
	b = np.array([x2, y2])
	c = np.array([x3, y3])

	ba = a - b
	bc = c - b

	cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))

	return np.arccos(cosine_angle)

def hull_left(p1, p2, s):
	# menyusun titik pembentuk convex hull dari kiri ke kanan
	if s == []:
		return []
	else:
		pmax = p1
		for point in s:
			if distance(*p1, *p2, *point) > distance(*p1, *p2, *pmax):
				pmax = point
			elif distance(*p1, *p2, *point) == distance(*p1, *p2, *pmax):
				if angle(*point, *p1, *p2) > angle(*pmax, *p1, *p2):
					pmax = point

		s_left = []
		s_right = []
		for point in s:
			if position(*p1, *pmax, *point) > 0:
				s_left.append(point)
			elif position(*pmax, *p2, *point) > 0:
				s_right.append(point)

		left = hull_left(p1, pmax, s_left)
		right = hull_left(pmax, p2, s_right)

		return left + [pmax] + right

def hull_right(p1, p2, s):
	# menyusun titik pembentuk convex hull dari kanan ke kiri
	if s == []:
		return []
	else:
		pmax = p1
		for point in s:
			if distance(*p1, *p2, *point) > distance(*p1, *p2, *pmax):
				pmax = point
			elif distance(*p1, *p2, *point) == distance(*p1, *p2, *pmax):
				if angle(*point, *p1, *p2) > angle(*pmax, *p1, *p2):
					pmax = point

		s_left = []
		s_right = []
		for point in s:
			if position(*p1, *pmax, *point) < 0:
				s_left.append(point)
			elif position(*pmax, *p2, *point) < 0:
				s_right.append(point)

		left = hull_right(p1, pmax, s_left)
		right = hull_right(pmax, p2, s_right)

		return right + [pmax] + left

def hull(s):
	# mengembalikan convex hull dari kumpulan titik s
	# asumsi s sudah terurut menaik berdasarkan absis
	p_left = s[0]
	p_right = s[len(s)-1]

	s_left = []
	s_right = []
	for point in s:
		if position(*p_left, *p_right, *point) > 0:
			s_left.append(point)
		elif position(*p_left, *p_right, *point) < 0:
			s_right.append(point)

	left = hull_left(p_left, p_right, s_left)
	right = hull_right(p_left, p_right, s_right)

	return [p_left] + left + [p_right] + right + [p_left]

if __name__ == "__main__":
	n = int(input("Masukkan jumlah titik: "))

	x = [randint(0,100) for i in range(n)]
	y = [randint(0,100) for i in range(n)]

	points = sorted(zip(x, y))
	answer = hull(points)
	x_ans = [answer[i][0] for i in range(len(answer))]
	y_ans = [answer[i][1] for i in range(len(answer))]

	plt.plot(x, y, 'o')
	plt.plot(x_ans, y_ans)

	print()
	print("Daftar semua titik:")
	for point in points:
		print(point)

	print()
	print("Titik-titik pembentuk convex hull:")
	for item in answer:
		print(item)

	plt.show()
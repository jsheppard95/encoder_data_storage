import matplotlib.pyplot as plt

INFILE_NAME = 'test.csv'

tvals = []
enc_vals = []
with open(INFILE_NAME, 'r') as infile:
    for line in infile:
        line_list = line.split(',')
        tvals.append(float(line_list[0]))
        enc_vals.append(float(line_list[1]))

print(tvals[-1] - tvals[0])
plt.plot(tvals, enc_vals)
plt.grid()
plt.show()

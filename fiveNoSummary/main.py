import csv
import matplotlib.pyplot as plt

data = []
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        if row:
            data.append(float(row[0]))

data.sort()
print(data)
n = len(data)


def median(values):
    m = len(values)
    mid = m // 2
    if m % 2 == 0:
        return (values[mid - 1] + values[mid]) / 2
    else:
        return values[mid]


minimum = data[0]
maximum = data[-1]
q2 = median(data)

if n % 2 == 0:
    lower_half = data[:n//2]
    upper_half = data[n//2:]
else:
    lower_half = data[:n//2]
    upper_half = data[n//2+1:]

q1 = median(lower_half)
q3 = median(upper_half)

print("=== Five Number Summary ===")
print(f"Minimum     : {minimum}")
print(f"Q1 (25%)    : {q1}")
print(f"Median (Q2) : {q2}")
print(f"Q3 (75%)    : {q3}")
print(f"Maximum     : {maximum}")

plt.boxplot(data)
plt.title("Box Plot - Five Number Summary")
plt.xlabel("Values")
plt.show()

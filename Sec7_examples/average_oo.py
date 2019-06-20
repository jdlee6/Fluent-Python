class Averager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)

avg = Averager()
print(avg(10))
# 10
print(avg(11))
# 10.5
print(avg(12))
# 11
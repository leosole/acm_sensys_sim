from scipy.stats import nakagami

r = nakagami.rvs(2, size=20)

print(r*100)

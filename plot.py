import matplotlib.pyplot as plt
import numpy as np

mrchem = [-8.560929421702415]

# svp, tzvp, qzvp kcal/mol
orca = np.array([-16.917, -13.905, -13.266])
orca_corr = np.array([-10.729254780449935, -12.550824019125006, -12.979818359730594])
orca_bsse = np.array([-6.188239530899327, -1.3545927723571072, -0.2863064420189312])

xs = [0, 1 , 2]

plt.plot(xs, orca, label = "orca no bsse")
plt.plot(xs, orca_corr, label = "orca bsse corrected")
# plt.plot(xs, orca_bsse, label = "bsse")
plt.plot(xs, [mrchem for _ in range(len(xs))], label = "mrchem")

plt.legend()
plt.savefig("plot.png")


n = -3204.657750388669 - -2168.905161567229 - -1035.725629100780 - -2168.876610161623 + -2168.872606823358 - -1035.730108096595 + -1035.724249855712 
print(n * 627.51)
print(bsse[0])
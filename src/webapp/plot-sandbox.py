import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,2, 1000) # plot 0 to 2 with 1000 points
print(x)

plt.figure()
plt.plot(x, np.sqrt(x), label = r"Skiing: $\sqrt{x}$")
plt.plot(x, x**2, label = r"Snowboarding: $x^2$")
plt.title("Learning Curves for Snowboarding and Skiing")
plt.xlabel("Time") ; plt.ylabel("Skill")
plt.legend(loc='upper left')
plt.show()

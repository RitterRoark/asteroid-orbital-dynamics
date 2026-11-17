import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Gravitational parameter fro the Sun (AU^3 / year^2)
MU_SUN = 4 * np.pi**2

def two_body_ode(t, state):
    """Equations of motion for a body orbiting the Sun in 2D."""
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)
    ax = -MU_SUN * x / r**3
    ay = -MU_SUN * y / r**3
    return [vx, vy, ax, ay]

# Initial conditions: Asteroid at perihelion (1.2 AU) with eccentricity ~0.4
r0 = 1.2 # AU
e = 0.4
v0 = np.sqrt(MU_SUN * (1 + e) / r0) #Vis-viva equation at perihelion
initial_state = [r0, 0.0, 0.0, v0]

# Propagate orbit for 5 years
t_span = (0, 5.0)
t_eval = np.linspace(0, 5.0, 1000)
sol = solve_ivp(two_body_ode, t_span, initial_state, t_eval=t_eval, rtol=1e-9, atol=1e-9)

x, y, vx, vy = sol.y
r = np.sqrt(x**2 + y**2)
v_sq = vx**2 + vy**2

# Compute specific orbital enery (should remain constant)
energy = 0.5 * v_sq - MU_SUN / r
rel_energy_error = np.abs((energy - energy[0]) / energy[0])

# Plot trajectory and numerical energy drift
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

ax1.plot(x, y, label="Asteroid Trajectory", color="#1f77b4")
ax1.scatter([0], [0], color="orange", s=120, label="Sun")
ax1.set_title("Simulated Asteroid Orbit (RK45)")
ax1.set_xlabel("X Position (AU)")
ax1.set_ylabel("Y Position (AU)")
ax1.axis("equal")
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend()

ax2.plot(sol.t, rel_energy_error, color="#d62728")
ax2.set_title("Numerical Validation: Relative Energy Drift")
ax2.set_xlabel("Time (Years)")
ax2.set_ylabel("|ΔE / E₀|")
ax2.set_yscale("log")
ax2.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("asteroid_orbit_validation.png", dpi=300)
plt.show()

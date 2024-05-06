import numpy as np

c: float = 0.1 # [m]
AR: tuple[float, float] = (1628, 1236)

# Question 1 -> Calculate FOV
c_multiplier: float = 1.5

l_fov: float = c*c_multiplier # [m]
h_fov: float = (AR[1]/AR[0])*l_fov

print(f"L_fov = {l_fov}")
print(f"H_fov = {h_fov}")

# Question 2 -> Magnification factor
l_px: float = 4.4e-6 # [m]

M: float = AR[0] * l_px/l_fov

print(f"M = {M}")
# Question 3 -> di, do
f: float = 35e-3 # [m]

do: float = f*(1+1/M)
di: float = M*do

print(f"di = {di}")
print(f"do = {do}")
# Question 4 -> f#
wl: float = 532e-9 # [m]
dp: float = 1e-6 # [m]
dtau_px: float = 3 # [m]
dtau_m: float = dtau_px * l_px
dof: float = 1e-3

fstop_pixel: float = np.sqrt(dtau_m**2 - (M*dp)**2)/(2.44 * wl * (1+M))
fstop_dof: float = np.sqrt(dof/(wl*4.88*((M+1)/M)**2))

print(f"f# = {fstop_pixel}")
print(f"f# = {fstop_dof}")
# Question 5 -> delta_t
V_inf: float = 10
ws_px: float = 32

ws_m: float = ws_px*l_px

delta_t: float = 0.25 * (ws_m/(M*V_inf))

print(f"dt = {delta_t}")
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
import os
# import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf

def voltage_reading():

    voltage = []

    data_dir = os.path.join("FMT_HWA", "Group05")  # Change path according to your PC
    for i in range(0, 22, 2):
        if i < 10:
            data_file = f"Calibration_00{i}.txt"
        elif i >=10:
            data_file = f"Calibration_0{i}.txt"
        
        data_path = os.path.join(data_dir, data_file)
        data = np.mean(np.loadtxt(data_path, skiprows=23)[:, 1])    # Averaging the voltages over the recorded samples
        voltage.append(data)
    
    return voltage

def error_polynomial(voltage, v_polynomial, fluid_velocity, u_polynomial):

    error_voltage = np.zeros(shape = len(fluid_velocity))
    error_voltage = abs(v_polynomial - voltage)/voltage

    error_fluid = np.zeros(shape = len(voltage))
    error_fluid = abs(u_polynomial - fluid_velocity)/fluid_velocity

    plt.figure()
    plt.plot(fluid_velocity, error_voltage, 'r')
    plt.xlabel("Fluid Velocity, U")
    plt.ylabel("Error (E)")
    plt.title("Relative Error in experimental data and polynomial fit")
    plt.show()

    plt.figure()
    plt.plot(voltage, error_fluid, 'r')
    plt.xlabel("Voltage, E")
    plt.ylabel("Error (U)")
    plt.title("Relative Error in experimental data and polynomial fit")
    plt.show()

def poly_fit(voltage, fluid_velocity):

    v_coeffs_poly = np.polyfit(fluid_velocity, voltage, 4)   # V for voltage
    u_coeffs_poly = np.polyfit(voltage, fluid_velocity, 4)   # U for velocity

    v_polynomial = np.zeros(shape = (len(fluid_velocity)))
    for i in range(len(fluid_velocity)):
        v_polynomial[i] = (v_coeffs_poly[0]*fluid_velocity[i]**4 + v_coeffs_poly[1]*fluid_velocity[i]**3 + v_coeffs_poly[2]*fluid_velocity[i]**2 + v_coeffs_poly[3]*fluid_velocity[i]**1 + v_coeffs_poly[4]*fluid_velocity[i]**0)
    
    plt.figure()
    plt.plot(fluid_velocity, v_polynomial, "b--", linewidth = 2, label = r'Polynomial of fit: $-1.95\cdot 10^{-5}\cdot x^{4} + 9.58\cdot 10^{-4}\cdot x^{3} - 1.7\cdot 10^{-2}\cdot x^{2} + 1.48\cdot 10^{-1}\cdot x + 1.14$')
    plt.plot(fluid_velocity, voltage, 'k-o', linewidth = 1.5, label = r'Experimental data')
    plt.xlabel("Fluid velocity, U")
    plt.ylabel("Voltage, E")
    plt.title(r"Experimental data and Polynomial fit of degree 4")
    plt.legend(fancybox=False, edgecolor = "black")
    plt.show()

    u_polynomial = np.zeros(shape = (len(voltage)))
    for i in range(len(voltage)):
        u_polynomial[i] = (u_coeffs_poly[0]*voltage[i]**4 + u_coeffs_poly[1]*voltage[i]**3 + u_coeffs_poly[2]*voltage[i]**2 + u_coeffs_poly[3]*voltage[i]**1 + u_coeffs_poly[4]*voltage[i]**0)


    plt.figure()
    plt.plot(voltage, fluid_velocity, "k-o", linewidth = 1.5, label = r'Experimental data')
    plt.plot(voltage, u_polynomial, "b--", linewidth = 2,  label = r'Polynomial of fit:')
    plt.title(r"Experimental data and Polynomial fit of degree 4")
    plt.xlabel("Voltage, E")
    plt.ylabel("Fluid velocity, U")   
    plt.legend(fancybox=False, edgecolor = "black")
    plt.show()

    error_polynomial(voltage, v_polynomial, fluid_velocity, u_polynomial)

    return u_coeffs_poly, v_coeffs_poly

def auto_corr(u_coeffs_poly, v_coeffs_poly):

    data_dir = os.path.join("FMT_HWA", "Group05")
    data_file = f"CorrelationTest.txt"
    data_path = os.path.join(data_dir, data_file)
    voltage = (np.loadtxt(data_path, skiprows=23)[:, 1])
    time = (np.loadtxt(data_path, skiprows=23)[:, 0])
    
    sample_velocity = np.zeros(shape = len(voltage))
    for i in range(len(voltage)):
        sample_velocity[i] = (u_coeffs_poly[0]*voltage[i]**4 + u_coeffs_poly[1]*voltage[i]**3 + u_coeffs_poly[2]*voltage[i]**2 + u_coeffs_poly[3]*voltage[i]**1 + u_coeffs_poly[4]*voltage[i]**0)

    plot_acf(voltage)
    plt.ylim([-0.1, 1])
    plt.title("Auto-correlation for the voltage signal")
    plt.show()

    plot_acf(sample_velocity)
    plt.ylim([-0.1, 1])
    plt.title("Auto-correlation for the velocity signal")
    plt.show()

    plt.figure()
    plt.plot(voltage, sample_velocity)
    plt.xlabel("Voltage, E")
    plt.ylabel("Sample velocity, U")
    plt.show()

    plt.figure()
    plt.plot(time, voltage)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage, E")
    plt.show()

    return sample_velocity

def rms_and_mean(sample_velocity):
    
    sum_terms = 0
    mean_val = np.mean(sample_velocity)
    for i in range(len(sample_velocity)):
        sum_terms += (sample_velocity[i] - mean_val)**2

    root_mean = np.sqrt(sum_terms / (len(sample_velocity)-1))
    
    return mean_val, root_mean


def plot_rms_and_mean(mean_0, mean_5, mean_15, rms_0, rms_5, rms_15):

    positions = np.arange(-40, 44, 4)
    
    plt.figure()
    plt.plot(mean_0, positions,'r-o', linewidth = 1.5, label = r'$\alpha$ 0°')
    plt.plot(mean_5, positions, 'b-o', linewidth = 1.5, label = r'$\alpha$ 5°')
    plt.plot(mean_15, positions, 'k-o', linewidth = 1.5, label = r'$\alpha$ 15°')
    plt.xlabel(r'Mean Velocity Profile: $<u>$')
    plt.ylabel('Positions (mm)')
    plt.legend()
    plt.show()


    plt.figure()
    plt.plot(rms_0, positions, 'r-o', linewidth = 1.5, label = r'$\alpha$ 0°')
    plt.plot(rms_5, positions, 'b-o', linewidth = 1.5, label = r'$\alpha$ 5°')
    plt.plot(rms_15, positions, 'k-o', linewidth = 1.5, label = r'$\alpha$ 15°')
    plt.xlabel('RMS of velocity fluctuations')
    plt.ylabel('Positions (mm)')
    plt.legend()
    plt.show()   

def conv_volt_to_vel(voltage_0, voltage_5, voltage_15, u_coeffs_poly, length):
    
    a = 21
    fluid_velocity_0 = np.zeros((length, a))
    fluid_velocity_5 = np.zeros((length, a))
    fluid_velocity_15 = np.zeros((length, a))

    mean_0 = np.zeros(a)
    mean_5 = np.zeros(a)
    mean_15 = np.zeros(a)
    mean_velocities = []

    rms_0 = np.zeros(a)
    rms_5 = np.zeros(a)
    rms_15 = np.zeros(a)
    rms_all = []

    for j in range(a):
        for i in range(length):
            fluid_velocity_0[i,j] = (u_coeffs_poly[0]*voltage_0[i,j]**4 + u_coeffs_poly[1]*voltage_0[i,j]**3 + u_coeffs_poly[2]*voltage_0[i,j]**2 + u_coeffs_poly[3]*voltage_0[i,j]**1 + u_coeffs_poly[4]*voltage_0[i,j]**0)
            fluid_velocity_5[i,j] = (u_coeffs_poly[0]*voltage_5[i,j]**4 + u_coeffs_poly[1]*voltage_5[i,j]**3 + u_coeffs_poly[2]*voltage_5[i,j]**2 + u_coeffs_poly[3]*voltage_5[i,j]**1 + u_coeffs_poly[4]*voltage_5[i,j]**0)
            fluid_velocity_15[i,j] = (u_coeffs_poly[0]*voltage_15[i,j]**4 + u_coeffs_poly[1]*voltage_15[i,j]**3 + u_coeffs_poly[2]*voltage_15[i,j]**2 + u_coeffs_poly[3]*voltage_15[i,j]**1 + u_coeffs_poly[4]*voltage_15[i,j]**0)

        mean_0[j], rms_0[j] = rms_and_mean(fluid_velocity_0[:,j])
        mean_5[j], rms_5[j] = rms_and_mean(fluid_velocity_5[:,j])
        mean_15[j], rms_15[j] = rms_and_mean(fluid_velocity_15[:,j])

    # mean_velocities = np.hstack((mean_0, mean_5, mean_15))
    # rms_all = np.hstack((rms_0, rms_5, rms_15))
    
    plot_rms_and_mean(mean_0, mean_5, mean_15, rms_0, rms_5, rms_15)
    


def reading_files(alpha, u_coeffs_poly, a):

    length = len(np.loadtxt(r"D:\3rd Quarter\FMT\HWA\FMT_HWA\Group05\Measurement_s00_s00.txt", skiprows=23)[:, 1])
    voltage_0 = np.zeros((length, a))
    voltage_5 = np.zeros((length, a))
    voltage_15 = np.zeros((length, a))

    count_0 = 0
    count_5 = 0
    count_15 = 0

    data_dir = os.path.join("FMT_HWA", "Group05")  # Change path according to your PC

    for j in range(len(alpha)):
        for i in range(-40, 44, 4):
            if i < 10 and i > -10:
                if alpha[j] == 15:
                    if i > 0:
                        data_file = f"Measurement_s0{i}_s{alpha[j]}.txt"
                    elif i < 0:
                        data_file = f"Measurement_s-0{abs(i)}_s{alpha[j]}.txt"
                else:
                    if i > 0:
                        data_file = f"Measurement_s0{i}_s0{alpha[j]}.txt"
                    elif i < 0:
                        data_file = f"Measurement_s-0{abs(i)}_s0{alpha[j]}.txt"
            elif i >= 10 or i <= -10:
                if alpha[j] == 15:
                    if i  > 0:
                        data_file = f"Measurement_s{i}_s{alpha[j]}.txt"
                    elif i < 0:
                        data_file = f"Measurement_s-{abs(i)}_s{alpha[j]}.txt" 
                else:
                    if i  > 0:
                        data_file = f"Measurement_s{i}_s0{alpha[j]}.txt"
                    elif i < 0:
                        data_file = f"Measurement_s-{abs(i)}_s0{alpha[j]}.txt"

            data_path = os.path.join(data_dir, data_file)
            if alpha[j] == 0:
                voltage_0[:,count_0] = np.loadtxt(data_path, skiprows=23)[:, 1]    # Storing the voltages over the recorded samples (alpha = 0°)
                count_0 += 1
            elif alpha[j] == 5:
                voltage_5[:,count_5] = np.loadtxt(data_path, skiprows=23)[:, 1]    # Storing the voltages over the recorded samples (alpha = 5°)
                count_5 += 1
            else: 
                voltage_15[:,count_15] = np.loadtxt(data_path, skiprows=23)[:, 1]    # Storing the voltages over the recorded samples (alpha = 5°)
                count_15 += 1

    conv_volt_to_vel(voltage_0, voltage_5, voltage_15, u_coeffs_poly, length)


voltage = voltage_reading()
fluid_velocity = np.linspace(0, 20, 11)

u_coeffs_poly, v_coeffs_poly = poly_fit(voltage, fluid_velocity) # u_coeffs_poly contains the coefficients for the function of U = f(V), while poly contains the coefficients for the function V = f(U)

sample_velocity = auto_corr(u_coeffs_poly, v_coeffs_poly)

rms_and_mean(sample_velocity)

alpha = [0, 5, 15]
number_of_positions = 21
reading_files(alpha, u_coeffs_poly, number_of_positions)



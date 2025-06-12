import numpy as np
import matplotlib.pyplot as plt

distance = 0.98 #m
T_kelvin = 22.75 + 273.15 #K
molar_mass = 0.0289644 #kg/mol
gamma_air = 1.4 #for air
gamma_helium = 1.66 #for helium
gamma_CO2 = 1.30 #for CO2
R = 8.31446261815324 #J/mol*K

sound_speed_air = np.sqrt(gamma_air * R * T_kelvin / molar_mass)
sound_speed_helium = np.sqrt(gamma_helium * R * T_kelvin / molar_mass)
sound_speed_CO2 = np.sqrt(gamma_CO2 * R * T_kelvin / molar_mass)

#measure the time delay between speaker and microphone at 0.98m from the speaker
air_time_delay = 2.02 #ms
air_time_delay_error = 0.04 #ms
helium_time_delay = 1.17 #ms
helium_time_delay_error = 0.09 #ms
CO2_time_delay =3.72 #ms
CO2_time_delay_error = 0.06 #ms

#calculate the sound speed
air_sound_speed = distance / air_time_delay
helium_sound_speed = distance / helium_time_delay
CO2_sound_speed = distance / CO2_time_delay

# Calculate percent differences between theoretical and measured velocities
air_percent_diff = 100 * abs(sound_speed_air - air_sound_speed) / sound_speed_air
helium_percent_diff = 100 * abs(sound_speed_helium - helium_sound_speed) / sound_speed_helium
CO2_percent_diff = 100 * abs(sound_speed_CO2 - CO2_sound_speed) / sound_speed_CO2

print(f"Air velocity percent difference: {air_percent_diff:.1f}%")
print(f"Helium velocity percent difference: {helium_percent_diff:.1f}%") 
print(f"CO2 velocity percent difference: {CO2_percent_diff:.1f}%")



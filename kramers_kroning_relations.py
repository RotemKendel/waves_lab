import sympy as sp
import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def kramers_kroning_relations_find_k_r(k_i, omega_values):
    """
    Calculate the Kramers-Kronig relations for the real part of the dielectric function.
    k_i is the imaginary part of the dielectric function, as a sympy expression
    omega_values is an array of frequencies to evaluate at
    """
    n_r_values = []
    omega = sp.symbols('omega')

    def integrand(Omega):
        return Omega * k_i(Omega) / (Omega**2 - omega**2)
    
    # Using Cauchy principal value with quad and finite limit
    integral, _ = integrate.quad(integrand, 0, 1e14, weight='cauchy', wvar=omega)
    n_r = 1 + (2/np.pi) * integral
    n_r_values.append(n_r)

    for omega in omega_values:
        n_r_values[omega] = n_r.replace(omega, omega)
    
    return np.array(n_r_values)


if __name__ == "__main__":
    # Define parameters
    Gamma = 0.5 * np.pi * 1e11
    omega_0 = 1000 * np.pi * 1e11
    
    # Define the imaginary part of the dielectric function
    def k_i(Omega):
        return (1/(2 * np.pi)) * (Gamma**2/((Omega - omega_0)**2 + Gamma**2))
    
    # Create frequency array
    omega_values = np.linspace(omega_0 - 2 * 1e12, omega_0 + 2 * 1e12, 1000)
    
    # Calculate real part
    k_i_values = []
    for omega in omega_values:
        k_i_values.append(k_i(omega))

    n_r_values = kramers_kroning_relations_find_k_r(k_i, omega_values)
    
    print(n_r_values)
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(omega_values, n_r_values, label='Real part of refractive index')
    plt.plot(omega_values, k_i_values, label='Imaginary part of dielectric function')
    plt.xlabel('Frequency (rad/s)')
    plt.ylabel('Real part of refractive index')
    plt.title('Kramers-Kronig Relations')
    plt.grid(True)
    plt.legend()
    plt.show()


import numpy as np
import cupy as cp
from scipy.linalg import eigh
from scipy.special import comb  

from itertools import combinations 
from tqdm.notebook import tqdm    
from scipy.stats import norm

import networkx as nx


import matplotlib.pyplot as plt
import seaborn as sns 

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "text.usetex": False, 
    "font.family": "serif",
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

def stat_create(N_iterazioni, sigma, matrices):
    spacing = []
    r = []
    r_index = []
    r_mean = []

    r_index_mean = []



    for i in range(N_iterazioni):
        couplings = np.random.normal(loc=0.0, scale=sigma, size=matrices.shape[0])

        hamil = np.tensordot(couplings, matrices, axes=([0], [0]))

        energies = np.linalg.eigh(hamil)[0]

        lenght = len(energies)
        trim = int(lenght*0.1)
        bulk_energies = energies[trim : -trim]

        new_spacing = np.diff(bulk_energies)
        new_spacing = new_spacing[new_spacing > 1e-10]
        spacing.extend(new_spacing)

        new_r_index = np.minimum(new_spacing[1:], new_spacing[:-1]) / np.maximum(new_spacing[1:], new_spacing[:-1])
        mean = np.mean(new_r_index)
        r_index_mean.append(mean)
        r_index.extend(new_r_index)

        r_new = []

        for j in range(len(new_spacing)-1):
            new_r_entry = new_spacing[j+1]/new_spacing[j]
            r_new.append(new_r_entry)
        
        mean = np.mean(r_new)
        r_mean.append(mean)
        r.extend(r_new)


    print(fr"Statistica complessiva = {len(r_index)}")
    return spacing, r, r_index, r_mean, r_index_mean

def plot(spacing, r, r_index, N_bin, p, g):
    
    spacing = np.array(spacing)
    min = np.min(spacing)
    max = np.max(spacing)

    sns.histplot(spacing, bins=N_bin, stat="density",
                color='royalblue', alpha=0.7, label='Dati SYK')


    plt.xlabel(fr'$\Delta E$')
    plt.ylabel(fr'$P(\Delta E)$')
    plt.title('Distribuzione degli spacing')
    plt.xlim(min, max)
    plt.legend()
    plt.show()

    r = np.array(r)
    min = np.min(r)
    max = np.max(r)


    sns.histplot(r, bins=N_bin, binrange=(0,5), stat="density",
                color='royalblue', alpha=0.7, label='Dati SYK')

    r_asse = np.linspace(0, 5, 200)
    
    if g:
        P_goe = (27/8)*(r_asse + r_asse**2)/(1 + r_asse + r_asse**2)**(2.5)

        plt.plot(r_asse, P_goe, color='pink', linewidth=1.5, label='Wigner surmise GOE')
    
    if p:

        P_poisson = 1/(1+r_asse)**2

        plt.plot(r_asse, P_poisson, color='black', linewidth=1.5, label='Distrib from Poisson')

    plt.xlabel(r'r')
    plt.ylabel(fr'$P(r)$')
    
    plt.xlim(0, 5)
    plt.legend()
    plt.show()

    r_index_asse = np.linspace(0, 1, 200)
    if g:
        P_index_goe = (27/4)*(r_index_asse + r_index_asse**2)/(1 + r_index_asse + r_index_asse**2)**(2.5)

        plt.plot(r_index_asse, P_index_goe, color='pink', linewidth=1.5, label='Distrib per GOE')

    if p:
        P_index_poisson = 2/(1+r_index_asse)**2

        plt.plot(r_index_asse, P_index_poisson, color='black', linewidth=1.5, label='Distrib from Poisson')

    sns.histplot(r_index, bins=N_bin, binrange=(0, 1), stat="density",
                color='royalblue', alpha=0.7, label='Dati SYK')

    plt.xlabel(fr'$\tilde r$')
    plt.ylabel(fr'$P(\tilde r)$')
    
    plt.xlim(0, 1)
    plt.legend()
    plt.show()

def Dirac_gen(N):
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    id = np.eye(2, dtype=complex) 

    K=N//2

    Gammas = []

    Gamma_0 = 1/pow(2, 0.5)*sigma_y
    Gamma_1 = 1/pow(2, 0.5)*sigma_x

    Gammas.append(Gamma_0)
    Gammas.append(Gamma_1)

    for i in range(K-1):
        for j in range(2*(i+1)):
            Gammas[j] = np.kron(Gammas[j],-1*sigma_z)
        id = np.eye(pow(2,i+1))
        newgamma = 1/pow(2, 0.5)*np.kron(id,sigma_x)
        Gammas.append(newgamma)
        newgamma = 1/pow(2, 0.5)*np.kron(id,sigma_y)
        Gammas.append(newgamma)



    for i in range(N):
        for j in range(N-i-1):
            Delta = Gammas[i]@Gammas[i+j+1] + Gammas[i+j+1]@Gammas[i]
            if np.any(Delta) != 0:
                print("Le matrici non anticommutano")


    Gamma_5 = Gammas[0]


    for i in range(N-1):
        Gamma_5 = Gamma_5@Gammas[i+1]

    diag = np.diag(Gamma_5)

    if np.allclose(diag.real, 0):
        mask = (diag.imag > 0)
    else:
        mask = (diag.real >0)

    return Gammas, Gamma_5, mask

def Dirac_gen_GPU(N):
    sigma_x = cp.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = cp.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = cp.array([[1, 0], [0, -1]], dtype=complex)
    id = cp.eye(2, dtype=complex) # Matrice identità 2x2

    K = N // 2

    Gammas = []

    Gamma_0 = 1/pow(2, 0.5)*sigma_y
    Gamma_1 = 1/pow(2, 0.5)*sigma_x

    Gammas.append(Gamma_0)
    Gammas.append(Gamma_1)

    for i in range(K-1):
        for j in range(2*(i+1)):
            Gammas[j] = cp.kron(Gammas[j],-1*sigma_z)
        id = cp.eye(pow(2,i+1))
        newgamma = 1/pow(2, 0.5)*cp.kron(id,sigma_x)
        Gammas.append(newgamma)
        newgamma = 1/pow(2, 0.5)*cp.kron(id,sigma_y)
        Gammas.append(newgamma)

    Gamma_tensor = cp.stack(Gammas)

    return Gamma_tensor 

def Dirac_gen_GPU_odd(N):
    sigma_x = cp.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = cp.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = cp.array([[1, 0], [0, -1]], dtype=complex)
    id = cp.eye(2, dtype=complex) # Matrice identità 2x2

    K = N // 2

    print(f"K={K}")

    Gammas = []

    Gamma_0 = 1/pow(2, 0.5)*sigma_y
    Gamma_1 = 1/pow(2, 0.5)*sigma_x

    Gammas.append(Gamma_0)
    Gammas.append(Gamma_1)

    for i in range(K-1):
        for j in range(2*(i+1)):
            Gammas[j] = cp.kron(Gammas[j],-1*sigma_z)
        id = cp.eye(pow(2,i+1))
        newgamma = 1/pow(2, 0.5)*cp.kron(id,sigma_x)
        Gammas.append(newgamma)
        newgamma = 1/pow(2, 0.5)*cp.kron(id,sigma_y)
        Gammas.append(newgamma)

    Gamma_5 = Gammas[0]
    for i in range(N-2):
        Gamma_5 = Gamma_5@Gammas[i+1]

    if (N-1) % 4 != 0:
        Gamma_5 = 1j*Gamma_5
    
    Gammas.append(Gamma_5)

    Gamma_tensor = cp.stack(Gammas)

    return Gamma_tensor, Gamma_5     


def mod_stat_create(N_iterazioni, mu, sigma, matrices):
    spacing = []
    r = []
    r_index = []
    r_mean = []

    r_index_mean = []



    for i in range(N_iterazioni):
        couplings = np.random.normal(loc=mu, scale=sigma, size=matrices.shape[0])

        hamil = np.tensordot(couplings, matrices, axes=([0], [0]))

        energies = np.linalg.eigh(hamil)[0]

        lenght = len(energies)
        trim = int(lenght*0.1)
        bulk_energies = energies[trim : -trim]

        #Calcolo gli spacing
        new_spacing = np.diff(bulk_energies)
        new_spacing = new_spacing[new_spacing > 1e-10]
        spacing.extend(new_spacing)

        new_r_index = np.minimum(new_spacing[1:], new_spacing[:-1]) / np.maximum(new_spacing[1:], new_spacing[:-1])
        mean = np.mean(new_r_index)
        r_index_mean.append(mean)
        r_index.extend(new_r_index)

        r_new = []

        for j in range(len(new_spacing)-1):
            new_r_entry = new_spacing[j+1]/new_spacing[j]
            r_new.append(new_r_entry)
        
        mean = np.mean(r_new)
        r_mean.append(mean)
        r.extend(r_new)


    print(fr"Statistica complessiva = {len(r_index)}")
    return spacing, r, r_index, r_mean, r_index_mean

def build_matrices(Gammas, simp_2, simp_3, simp_4):

    matrices_2 = []
    matrices_3 =[]
    matrices_4 = []

    for i in range(len(simp_2)):
        link = simp_2[i]
        new = Gammas[link[0]] @ Gammas[link[1]]

        matrices_2.append(new)

    matrices_2 = np.array(matrices_2)

    for i in range(len(simp_3)):
        triangle = simp_3[i]
        new = Gammas[triangle[0]] @ Gammas[triangle[1]] @ Gammas[triangle[2]]

        matrices_3.append(new)  

    matrices_3 = np.array(matrices_3)  
    
    for i in range(len(simp_4)):
        tetra = simp_4[i]
        new = Gammas[tetra[0]] @ Gammas[tetra[1]] @ Gammas[tetra[2]] @ Gammas[tetra[3]]

        matrices_4.append(new)    
    
    matrices_4 = np.array(matrices_4)  


    return matrices_2, matrices_3, matrices_4

def build_matrices_GPU(Gamma_tensor, N):


    s2 = cp.asarray(list(combinations(range(N), 2)))
    s4 = cp.asarray(list(combinations(range(N), 4)))

    matrices_2 = Gamma_tensor[s2[:, 0]] @ Gamma_tensor[s2[:, 1]]

    matrices_4 = Gamma_tensor[s4[:, 0]] @ Gamma_tensor[s4[:, 1]] @ Gamma_tensor[s4[:, 2]] @ Gamma_tensor[s4[:, 3]]

    return matrices_2, matrices_4
 








def simp_stat_create(N_iterazioni, N, matrices_2, matrices_3, matrices_4):
    
    
    
    
    r_mean = []

    r_index_mean = []
    
    
    
    J = 1.0

    sigma_2 = J/(N**(0.5))
    sigma_3 = np.sqrt(2) * J/N
    sigma_4 = np.sqrt(6) * J/(N)**(1.5)


    for i in range(N_iterazioni):

        couplings_2 = np.random.normal(loc=0.0, scale=sigma_2, size=matrices_2.shape[0])
        hamil_2 = np.tensordot(couplings_2, matrices_2, axes=([0], [0]))

        couplings_3 = np.random.normal(loc=0.0, scale=sigma_3, size=matrices_3.shape[0])
        hamil_3 = np.tensordot(couplings_3, matrices_3, axes=([0], [0]))

        couplings_4 = np.random.normal(loc=0.0, scale=sigma_4, size=matrices_4.shape[0])
        hamil_4 = np.tensordot(couplings_4, matrices_4, axes=([0], [0]))

        hamil = 1j * hamil_2 + 1j * hamil_3 + hamil_4

        energies = np.linalg.eigh(hamil)[0]

        lenght = len(energies)
        trim = int(lenght*0.1)
        bulk_energies = energies[trim : -trim]

        new_spacing = np.diff(bulk_energies)

        new_spacing = new_spacing[new_spacing > 1e-10]
        

        new_r_index = np.minimum(new_spacing[1:], new_spacing[:-1]) / np.maximum(new_spacing[1:], new_spacing[:-1])
        mean = np.mean(new_r_index)
        r_index_mean.append(mean)

        r_new = []

        for j in range(len(new_spacing)-1):
            new_r_entry = new_spacing[j+1]/new_spacing[j]
            r_new.append(new_r_entry)
        
        mean = np.mean(r_new)
        r_mean.append(mean)
        


    return r_mean, r_index_mean


def simp_stat_create_GPU(N_iterazioni, N, matrices_2, matrices_3, matrices_4):
    dim = matrices_2.shape[1]
    r_mean = cp.empty(N_iterazioni, dtype=cp.float64)
    r_index_mean = cp.empty(N_iterazioni, dtype=cp.float64)
    
    J = 1.0

    sigma_2 = J/(N**(0.5))
    sigma_3 = cp.sqrt(2) * J/N
    sigma_4 = cp.sqrt(6) * J/(N)**(1.5)

    couplings_2 = cp.random.normal(loc=0.0, scale=sigma_2, size=(N_iterazioni, matrices_2.shape[0]))
    couplings_3 = cp.random.normal(loc=0.0, scale=sigma_3, size=(N_iterazioni, matrices_3.shape[0]))
    couplings_4 = cp.random.normal(loc=0.0, scale=sigma_4, size=(N_iterazioni, matrices_4.shape[0]))

    hamil_2 = cp.tensordot(couplings_2, matrices_2, axes=([1], [0]))
    hamil_3 = cp.tensordot(couplings_3, matrices_3, axes=([1], [0]))
    hamil_4 = cp.tensordot(couplings_4, matrices_4, axes=([1], [0]))

    hamil = 1j * hamil_2 + 1j * hamil_3 + hamil_4

    energies = cp.empty((N_iterazioni, dim), dtype=cp.float64)
    
    for i in range(N_iterazioni):
        energies[i] = cp.linalg.eigvalsh(hamil[i])

    lenght = energies.shape[1]
    trim = int(lenght*0.1)
    bulk_energies = energies[:, trim : -trim]

    new_spacing = cp.diff(bulk_energies, axis=1)

    mask_non_degenere = new_spacing[0] > 1e-10
    new_spacing = new_spacing[:, mask_non_degenere]
        

    r_index_matrix = cp.minimum(new_spacing[:, 1:], new_spacing[:, :-1]) / cp.maximum(new_spacing[:, 1:], new_spacing[:, :-1])
    r_index_mean = cp.mean(r_index_matrix, axis=1)

    r_matrix = new_spacing[:, 1:] / new_spacing[:, :-1]     
    r_mean = cp.mean(r_matrix, axis=1)    

    return r_mean.get(), r_index_mean.get(), r_matrix.get(), r_index_matrix.get()
    

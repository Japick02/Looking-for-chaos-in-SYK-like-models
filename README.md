# Looking-for-chaos-in-SYK-like-models

Numerical study of chaotic properties of SYK-like models through level spacing ratio distribution and the related RMT ensembles. In some of the models different Chaos to Integrability transitions have been studied. Only for standard SYK the spectral form factor has been computed.

Studied models are: SYK, Sparse SYK, Hybrid SYK, Complex SYK, SYK on growing simplicial complexes.

All the notebooks are based on CuPy library, which allows GPU acceleration. All the code has been tested on a Nvidia RTX 5070.

## Notebooks

### 1. Standard SYK
**File** [Complete_simp.ipynb](Complete_simp-ipynb)

Computation of level spacing ratio statistics for a model built from SYK allowing 2,3 and 4-fermion interactions. Every interaction type can be turned off separately.

<p align="center">
  <img src="figures/SYK_r_distrib.png" width="48%" alt="r_distrib">
  <img src="figures/SYK_tilde_r_distrib.png" width="48%" alt="tilde_r_distrib">
</p>

**File:** [SYK_SFF.ipynb](SYK_SFF.ipynb)

Computation of standard SYK Spectral Form Factor.

<p align="center">
  <img src="figures/SFF_N18_beta5.jpeg" width="60%" alt="SYK_SFF">
</p>

### 2. Sparse SYK
**File:** [Sparse_SYK.ipynb](Sparse_SYK.ipynb)

Study of an SYK-like model on an Erdos-Renyi network. Computation of level spacing ratio distribution. Analysis of a CtI transition driven by p, the probability for a an hyper-edge to exist.

<p align="center">
  <img src="figures/Sparse_SYK_CtI.jpeg" width="60%" alt="Sparse_SYK_CtI">
</p>

### 3. Hybrid SYK
**File:** [Hybrid_SYK.ipynb](Hybrid_SYK.ipynb)

Computation of level spacing ratio statistics for an SYK-like model with 2-fermion interactions and 4-fermion interactions. The couplings expectation values are taken to be diffirent for the two.

**File:** [Hybrid_SYK_CtI.ipynb]([Hybrid_SYK_CtI.ipynb)

Study of the CtI transition driven by the couplings ratio.

<p align="center">
  <img src="figures/Hybrid_SYK_oddN_graph.png" width="80%" alt="Hybrid_SYK_CtI">
</p>

### 4. Complex SYK

Computation of the level spacing ratio statistics for Complex SYK model, distinguishing different charge sectors.

### 5. SYK on growing simplicial complexes




## Dependencies
Python, NumPy, CuPy, Matplotlib

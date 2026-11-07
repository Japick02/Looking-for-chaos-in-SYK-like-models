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

**Reference:** G. Saros. *AdS2 holography and the SYK model* (2019): [arXiv:1711.08482](https://arxiv.org/abs/1711.08482)

**File:** [SYK_SFF.ipynb](SYK_SFF.ipynb)

Computation of standard SYK Spectral Form Factor.

<p align="center">
  <img src="figures/SFF_N18_beta5.jpeg" width="60%" alt="SYK_SFF">
</p>

**Reference:** J.S. Cotler, G. Gur-Ari, M. Hanada, J. Polchinski, P. Saad, S. H. Shenker, D. Stanford, A. Streicher, M. Tezuka. *Black Holes and Random Matrices* (2018): [arXiv:1611.04650](https://arxiv.org/abs/1611.04650)

### 2. Sparse SYK
**File:** [Sparse_SYK.ipynb](Sparse_SYK.ipynb)

Study of an SYK-like model on an Erdos-Renyi network. Computation of level spacing ratio distribution. Analysis of a CtI transition driven by p, the probability for a an hyper-edge to exist.

<p align="center">
  <img src="figures/Sparse_SYK_CtI.jpeg" width="60%" alt="Sparse_SYK_CtI">
</p>

**Reference:** P. Orman, H. Gharibyan, J. Preskill. *Quantum chaos in the sparse SYK model* (2024): [arXiv:2403.13884](https://arxiv.org/abs/2403.13884)

### 3. Hybrid SYK
**File:** [Hybrid_SYK.ipynb](Hybrid_SYK.ipynb)

Computation of level spacing ratio statistics for an SYK-like model with 2-fermion interactions and 4-fermion interactions. The couplings expectation values are taken to be diffirent for the two.

**File:** [Hybrid_SYK_CtI.ipynb]([Hybrid_SYK_CtI.ipynb)

Study of the CtI transition driven by the couplings ratio.

<p align="center">
  <img src="figures/Hybrid_SYK_oddN_graph.png" width="80%" alt="Hybrid_SYK_CtI">
</p>

**Reference:** F. Sun, Y. Yi-Xiang, J. Ye, W.-M. Liu. *A new universal ratio in Random Matrix Theory and chaotic to integrable transition in Type-I and Type-II hybrid Sachdev-Ye-Kitaev models* (2021): [arXiv:1809.07577](https://arxiv.org/abs/1809.07577)

### 4. Complex SYK

Computation of the level spacing ratio statistics for Complex SYK model, distinguishing different charge sectors.

**Reference:** M. Berkooz, V. Narovlansky, H. Raj. *Complex Sachdev-Ye-Kitaev model in the double scaling limit* (2020): [arXiv:2006.13983](https://arxiv.org/abs/2006.13983)

### 5. SYK on growing simplicial complexes
Analysis of average level spacing ratio for a model built from SYK on growing simplicial complexes.

<p align="center">
  <img src="figures/N20_tilder_vs_netvar.png" width="48%" alt="tilder_vs_netvar">
  <img src="figures/N20_tilder_vs_modu.png" width="48%" alt="ttilder_vs_modu">
</p>

**References for theory and code about these networks:**  D. Febbe, D. Fanelli, T. Carletti. *Random Walks Across Dimensions: Exploring Simplicial Complexes* (2026): [arXiv:2601.16086](https://arxiv.org/abs/2601.16086).

D. Febbe, D. Fanelli, T. Carletti. *Model of Simplicial Complexes with dimension-wise preferential attachment* (2026): [arXiv:2605.17004](https://arxiv.org/abs/2605.17004). 

[GitHub repository](https://github.com/diegofebbe/Random_walk_on_simplicial_complexes)



## Dependencies
Python, NumPy, CuPy, Matplotlib

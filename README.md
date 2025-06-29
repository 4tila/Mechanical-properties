# Mechanical Properties of 2D Materials

A Python-based tool for calculating **in-plane stiffness (2D Young's modulus)**, **Poisson ratio**, and **2D bulk modulus** of 2D materials using SIESTA output files.

The tool generates strained structures (in `x`, `y`, and `xy` directions) for further relaxation using SIESTA, and analyzes the resulting energies and lattice responses to extract elastic properties.

---

## 📦 Requirements

* Python ≥ 3.7
* SIESTA
* `numpy`
* Linux Bash environment

---

## ⚙️ Input

* A `STRUCT_OUT` file from a **fully relaxed** unit cell or supercell (preferably a supercell for better precision).
* The system must be a **2D material**, i.e., deformation only in the `x` and `y` directions.

---

## 🚧 Workflow

1. **Strain Generation**:
   The tool generates folders for each strain step in:

   * `x` direction → only `y` direction is allowed to relax

   * `y` direction → only `x` direction is allowed to relax

   * `xy` direction → all in-plane directions are fixed (used to calculate the 2D bulk modulus)

   > The `z` direction remains fixed in all cases (suitable for 2D materials).

   ```bash
   python3 generate_folders.py
   ```

2. **Structure Relaxation**:
   Run the `run.sh` script to iterate through each generated folder and launch the SIESTA relaxation:

   ```bash
   bash run.sh
   ```

3. **Mechanical Analysis**:
   After SIESTA runs are completed, execute the Python script to extract mechanical properties:

   ```bash
   python3 mechanical.py
   ```

   This script will:

   * Fit the total energy vs. strain curve using linear or quadratic fits.
   * Estimate:

     * 2D Young's modulus in `x` and `y`
     * Poisson ratio in both directions
     * 2D bulk modulus

---

## 📊 Output

* Terminal printout of:

  * Energy vs. strain
  * Linear/quadratic fits
* Estimated values of:

  * 2D Young's modulus $E_x, E_y$
  * Poisson ratios $\nu_{xy}, \nu_{yx}$
  * 2D bulk modulus $K_{2D}$

---

## ✍️ Notes

* Ensure your SIESTA relaxation includes accurate force convergence and proper boundary conditions.
* The use of a **supercell** is strongly recommended to reduce numerical noise and improve strain accuracy.
* Make sure your `STRUCT_OUT` file reflects a **fully optimized** structure before beginning.
* This project uses standard pseudopotentials (e.g., H.psf, C.psf). These are not included in the repository, but can be downloaded from official SIESTA resources or PseudoDojo.

---


## 📜 License

MIT License – free to use, modify, and distribute.


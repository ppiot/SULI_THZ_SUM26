# SULI_THZ_SUM26

SULI intern project -- Summer 2026.

Analysis of electro-optic (EO) sampling data from BeamNetUS experiments at the Argonne Wakefield Accelerator (AWA), measuring balanced-photodiode (BPD) traces vs. laser delay to characterize bunch and wake signals.

## Contents

- `analysisdata_experiment.ipynb` — main analysis notebook. Loads `.npy` scan files, averages every 4 shots, and plots BPD - Reference vs. delay for dipole-on / dipole-off configurations.
- `PostP_fromWanming.py` — original post-processing script from Wanming Liu (`wmliu`). Reads a `.npy` scan dict (`phase`, `peak`), converts phase to delay using a 81.25 MHz reference, and writes paired `.csv` / `.png` outputs.
- `Data_raw/Aug01/` — raw scan data from 2025-08-01. Includes fine and quick scans at 1 nC under various optical configurations (BBO / NoBBO, dipole on/off, iris, rotated polarization). Each scan is stored as a `.npy` dict; some have companion `.npz`, `.csv`, and `.png` files.

## Scan file format

Each `.npy` file is a pickled dict with keys:
- `phase` — array of phase set-points in degrees
- `peak` — per-shot array where index 3 is the reference channel and index 4 is the EO-modulated BPD channel

Delay (ns) is computed as `(phase - phase[0]) * 1e9 / 81.25e6 / 360`.

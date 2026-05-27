# SULI_THZ_SUM26

SULI intern project -- Summer 2026.

Analysis of electro-optic (EO) sampling data from BeamNetUS experiments at the Argonne Wakefield Accelerator (AWA), measuring balanced-photodiode (BPD) traces vs. laser delay to characterize bunch and wake signals. Includes companion fiber-laser timing and jitter studies for the RPI/PARTOW integrated THz sensor.

## Notebooks and scripts

- `analysisdata_experiment.ipynb` — main analysis notebook. Loads `.npy` scan files, averages every 4 shots, and plots BPD - Reference vs. delay for dipole-on / dipole-off configurations.
- `jitter_study0Xing.ipynb` — preliminary analysis of fiber-laser timing/jitter data (channels: Ch1 BPM, Ch2 SD, Ch3 FPD). Works with the `.npy` files under `fiberlaser/`.
- `PostP_fromWanming.py` — original post-processing script from Wanming Liu (`wmliu`). Reads a `.npy` scan dict (`phase`, `peak`), converts phase to delay using a 81.25 MHz reference, and writes paired `.csv` / `.png` outputs.

## Data

- `Data_raw/July30_/` — raw scan data from 2025-07-30. Coarse/fine scans plus fiber-laser tests with the CTR screen in/out (no beam).
- `Data_raw/July31_/` — raw scan data from 2025-07-31. Coarse and fine scans across a charge sweep (0.25, 0.5, 1, 2.5, 4, 5, 7, 10 nC), including fiber-resync variants and dipole on/off configurations.
- `Data_raw/Aug01/` — raw scan data from 2025-08-01. Fine and quick scans at 1 nC under various optical configurations (BBO / NoBBO, dipole on/off, iris, rotated polarization).
- `fiberlaser/` — fiber-laser timing and jitter measurements:
  - `CoarsTiming_Measurement*_0.npy` — coarse-timing baseline and BD / BD+10m variants.
  - `CT_Monday_SD_0.npy`, `CT_Monday_SDFPD_{0..5}.npy` — Monday coarse-timing runs with the SD and SD+FPD configurations.
  - `JitterMeasurement_{0..3}.npy` — jitter measurement series.

Each scan `.npy` is a pickled dict with keys:
- `phase` — array of phase set-points in degrees
- `peak` — per-shot array where index 3 is the reference channel and index 4 is the EO-modulated BPD channel

Delay (ns) is computed as `(phase - phase[0]) * 1e9 / 81.25e6 / 360`.

Many scans have companion `.npz`, `.csv`, and `.png` files; `.npz.gz` archives are gzipped bundles of multiple scans.

## Generated figures

- `BPDwf_combined.png` — combined BPD waveform plot.
- `coarsetiming.png`, `coarsetiming_SD.png` — coarse-timing results (baseline and SD configuration).
- `timingandscan.png` — timing/scan overview figure.

# Reproducibility Guide

This file documents how to reproduce the analyses and maps in this repository. It explains the folder layout, recommended environment setup, data expectations, and the typical execution order of the notebooks.

**Repository Structure**
- **`Klimata-Web-app`**: Web map / StoryMap assets and short README with the live ArcGIS Story Map link.
- **`KLIMATA_DATABASES`**: Master database notebooks / generated data files used by the analyses.
- **`KLIMATA_MAP_CODES`**: Notebooks that create map outputs and mapping codes.
- **`KLIMATA_PREPROCESSING`**: Raw data extraction and preprocessing notebooks (climate, NDVI, population, RWI, air/barangay merge).
- **`KLIMATA_STANDARDIZED`**: Notebooks that standardize/scale features (climate, health, amenity, population, RWI).

**Goal**
Recreate the processed datasets and map outputs from raw inputs by running the notebooks in the correct order and using a reproducible Python environment.

**Recommended Environment**
- **Python**: 3.10 or newer is recommended.
- Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
```

- Install dependencies from a `requirements.txt` (if present). If the repo doesn't include one, create it from your environment after installing packages:

```powershell
pip install jupyterlab pandas numpy geopandas rasterio scikit-learn matplotlib folium
pip freeze > requirements.txt
```

Notes:
- If you use conda, create an environment and install geopandas and rasterio via `conda` for fewer binary issues.
- If notebooks rely on ArcGIS API for Python, add `arcgis` to the environment.

**Data expectations and locations**
- Notebooks read/write data using relative paths inside the repository folders listed above. Keep the folder structure unchanged so relative paths work.
- Large raw files may be omitted from the repo. If a notebook fails due to missing data, check the top of that notebook for a data-source comment or placeholder and obtain the original files (or ask the project owner).

**Notebook execution order (recommended)**
1. `KLIMATA_PREPROCESSING/*` — run preprocessing notebooks to extract and prepare raw features.
2. `KLIMATA_STANDARDIZED/*` — run standardization notebooks to harmonize feature scales.
3. `KLIMATA_DATABASES/*` — create or update master databases from processed files.
4. `KLIMATA_MAP_CODES/*` — generate map outputs and map-ready files.
5. `Klimata-Web-app/*` — review web app assets and the StoryMap link.

**Run notebooks locally**
- From the repo root, start Jupyter Lab or Notebook so relative paths work:

```powershell
pip install jupyterlab
jupyter lab
```

- Open each notebook and run cells in order. Watch for cells that require credentials or external API tokens (ArcGIS tokens, remote storage access, etc.).

**Reproducibility tips**
- Commit `requirements.txt` after you finalize the environment so others can recreate it.
- Pin package versions in `requirements.txt` to reduce future breakage.
- If possible, save intermediate processed files (CSV / GeoPackage) in `KLIMATA_DATABASES` so later steps run without reprocessing heavy computations.
- Log runtime metadata (Python version, package versions) at the top of key notebooks. Example:

```python
import sys, pkg_resources
print(sys.version)
print([f"{d.project_name}=={d.version}" for d in pkg_resources.working_set])
```

**Optional: Docker reproducibility**
If you want maximal reproducibility, create a `Dockerfile` that installs the pinned `requirements.txt` and runs Jupyter. Example skeleton:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
```

**ArcGIS StoryMap**
The project StoryMap is linked in the main `README.md`. Quick clickable URL: https://arcg.is/0y8XrL

**If something fails**
- Inspect the notebook top-cells for path assumptions and required files.
- Make sure your virtual environment has `geopandas`/`rasterio` installed via binary-friendly methods (conda or wheels) to avoid build errors on Windows.

Questions or next steps
- I can:
  - create a `requirements.txt` from my recommended list, or
  - add a Dockerfile and `docker-compose.yml` for one-command reproducibility, or
  - scan the notebooks for explicit package imports and generate a precise `requirements.txt`.


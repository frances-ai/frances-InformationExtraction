# 📜️ Geoparsing Historical Text: Encyclopaedia Britannica Terms (NLS Data Foundry)

This folder contains scripts and resources for **geoparsing historical text**, specifically terms from the *Encyclopaedia Britannica* dataset provided by the National Library of Scotland (NLS) Data Foundry.

Geoparsing includes two main stages:
- 🌿 **Geotagging**: Identifying mentions of locations in text.
- 📍 **Georesolving**: Mapping those mentions to geographic coordinates and metadata.

An annotated dataset (`eb_geo_samples_annotated.json`) is also included for evaluating geotagging performance.

---

## 📂 Contents

### 1. `PrepareGeoparsingSamples.ipynb`
- ✏️ Create sample data for:
  - **Geotagging evaluation**
  - **Final geoparsing tasks**

### 2. `eb_<geotag_method>_geotagging.py`
- 🧐 Scripts for geotagging text using various methods:
  - **Edinburgh Geoparser**
  - **spaCy NER**
  - **Flair NER**
  - **Stanza NER**
- Each script runs a specific geotagging method on the input text.

### 3. `eb_eg_georesolve.py`
- 🌍 Resolves geotagged locations to geographical coordinates.
- Uses a **locally installed Geonames database** with the **Edinburgh Geoparser**.

### 4. `refine_with_in_text_coordinates.py`
- 🛸 Extracts explicit coordinates mentioned within articles.
- Marks corresponding terms as locations if missed during geotagging.

### 5. `GeoTaggingEvaluation.ipynb`
- 📊 Notebook for evaluating geotagging outputs.
- Compares detected location mentions against the manually annotated sample set (`eb_geo_samples_annotated.json`).
- Provides performance metrics like Precision, Recall, and F1-score.

### 6. `get_countries_geo.py`
- 🌍 Extract countries geo information from [Geonames source data](https://download.geonames.org/export/dump/), such as 
ISO code, name, latitude, longitude, boundary.


---

## 🛠️ Requirements

Before running the scripts, make sure to set up the environment:

1. Install [defoe](https://github.com/frances-ai/defoe_lib/tree/main)
2. Install required Python packages

```
pip install -r requirements.txt
```

3. Download the required spaCy model

```
python -m spacy download en_core_web_sm
```

---

## 🗃️ Data

- **`eb_geo_samples_annotated.json`**  
  ✍️ Manually annotated sample dataset for evaluating geotagging accuracy.

---

## 🚀 How to Use

First, edit the input and output filepath of the scripts you need to run. Then,

1. **Prepare Samples**  
   ➡️ Run `prepareSamples.ipynb` to create evaluation samples or datasets for geoparsing.

2. **Run Geotagging**  
   ➡️ Select a method and run the corresponding `eb_<geotag_method>_geotagging.py` script.

3. **Resolve Geotagged Locations**  
   ➡️ Use `eb_eg_georesolve.py` to resolve location names to coordinates.

4. **Refine Results**  
   ➡️ (Optional) Run `refine_with_in_text_coordinates.py` to improve tagging based on in-text coordinates.

5. **Evaluate Geotagging**  
   ➡️ Evaluate the performance using the `GeoTaggingEvaluation` scripts against the annotated samples.

---


## 📜 Notes

- 🛠️ Edinburgh Geoparser requires a local Geonames database installation for georesolving.
- 🔍 Currently, evaluation focuses only on the **geotagging** stage (not full geoparsing).


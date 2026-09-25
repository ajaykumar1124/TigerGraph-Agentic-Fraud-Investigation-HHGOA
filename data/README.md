# HHGOA dataset note

This project expects the actual HHGOA data files and README to be placed in this folder.

Current workspace state:
- No dataset CSV/XLSX/README files are present yet.
- The exact column names therefore cannot be safely mapped without the real source files.

When the data is added, the required mapping is:

- transaction ID column
- customer column
- account/card column
- device column
- risk score column
- transaction attributes
- historical case indicators

Once those files are present, the following workflow should be used:

1. Load the dataset with backend/data/loader.py
2. Clean with backend/data/cleaner.py
3. Infer candidate columns with backend/data/transformer.py
4. Validate required columns with backend/data/validator.py
5. Map the final columns to TigerGraph vertices and edges

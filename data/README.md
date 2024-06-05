## Data

The raw data in FASTA format is located in the following folders:

```
data/fasta
├── benchmark
│   ├── test
│   │   └── test.fasta      # test sequences for benchmark
│   └── training
│       ├── negative.fasta  # non-PA sequences for benchmark
│       └── positive.fasta  # PA-sequences for benchmark
└── lobo
    ├── negative.fasta      # non-PA sequences for LOBO evaluation
    └── positive.fasta      # PA sequences for LOBO evaluation
```

The annotated sequences used in the experiments (and the corresponding PSE/descriptors) are stored in the files below in .parquet format. They can be loaded with python as follows:

```python
import pandas as pd

example_path = "data/descriptors/lobo/test/UP000000425.parquet"
df = pd.read_parquet(example_path)
```

```
data
├── descriptors
│   └── lobo
│       ├── test  # Descriptors for candidate antigen selection
│       │   ├── UP000000425.parquet  # N. meningitidis
│       │   ├── UP000000586.parquet  # S. pneumoniae
│       │   ├── UP000000625.parquet  # E. coli
│       │   ├── UP000000750.parquet  # S. pyogenes
│       │   ├── UP000000799.parquet  # C. jejuni
│       │   ├── UP000000800.parquet  # C. muridarum
│       │   ├── UP000001432.parquet  # A. pleuropneumoniae
│       │   ├── UP000001584.parquet  # M. tuberculosis
│       │   ├── UP000006386.parquet  # S. aureus
│       │   └── UP000326807.parquet  # Y. pestis
│       └── training
│           ├── negative.parquet     # non-PA descriptors for LOBO
│           └── positive.parquet     # PA descriptors for LOBO
└── pses
    ├── benchmark
    │   ├── test
    │   │   └── test.parquet         # test PSEs for benchmark
    │   └── training
    │       ├── negative.parquet     # non-PA PSEs for benchmark
    │       └── positive.parquet     # PA PSEs for benchmark
    └── lobo
        ├── test  # PSEs for candidate antigen selection
        │   ├── UP000000425.parquet  # N. meningitidis
        │   ├── UP000000586.parquet  # S. pneumoniae
        │   ├── UP000000625.parquet  # E. coli
        │   ├── UP000000750.parquet  # S. pyogenes
        │   ├── UP000000799.parquet  # C. jejuni
        │   ├── UP000000800.parquet  # C. muridarum
        │   ├── UP000001432.parquet  # A. pleuropneumoniae
        │   ├── UP000001584.parquet  # M. tuberculosis
        │   ├── UP000006386.parquet  # S. aureus
        │   └── UP000326807.parquet  # Y. pestis
        └── training
            ├── negative.parquet     # non-PA PSEs for LOBO
            └── positive.parquet     # non-PA PSEs for LOBO
```

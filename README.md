# Descriptor-Free Protective Antigen Classifier (DFPAC)

This repository contains the data, code, and experimental results of the paper "A descriptor-free machine learning framework to improve antigen discovery for bacterial pathogens" (submitted).

## 1. Setup

The code has been tested on Linux machines. The only prerequisite is that the [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) package manager is installed.

### 1.1 Prepare the environment

First, clone the repository and `cd` into the right directory:

```bash
git clone https://github.com/marcopodda/dfpac.git && cd dfpac
```

To run the scripts, you need to first setup a conda environment by executing the following command:

```bash
conda create --name dfpac-env python=3.12 -y && conda activate dfpac-env
```

### 1.2 Install and check installation

Finally, install the package in edit mode:

```bash
pip install -e .
```

At this point, the code should be installed in the `dfpac-env` environment. Run

```bash
which dfpac-eval
```
and check that it does not return errors, and you are ready to use it.

## 2. Data

Please check [here](data/README.md).

## 3. Reproducing the experiments

### 3.1 LOBO evaluation

Run:

```bash
dfpac-eval experiment=lobo-[TYPE] dataset.species="[SPECIES]" seed=[SEED]
```

Where:
- `[TYPE]` is either `descriptors` (if you wish to evaluate descriptors) or `pses` (if you wish to evaluate PSEs)
- `[SPECIES]` is the name of the bacterial to be left out for testing. Check the [data](data/README.md) section the list (but remember to use the entire name). Be careful to include the name within quotes (e.g. `"Escherichia coli"`)
- `[SEED]` is a positive integer to be used as seed for reproducibility.

In our experiments, seeds from 1 to 10 were used.

Results will be stored in the `outputs/lobo/[TYPE]/[SPECIES]/[SEED]` folder.


### 3.2 Benchmark evaluation

```bash
dfpac-eval experiment=benchmark-pses seed=[SEED]
```
where `[SEED]` is defined as above.

In our experiments, seeds from 1 to 10 were used.

Results will be stored in the `outputs/benchmark/pses/[SEED]` folder.


## 4. Checking the results

The results are shown in [this notebook](notebooks/analysis.ipynb) (they basically correspond to the figures and tables used in the article).

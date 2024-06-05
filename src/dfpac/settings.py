from pathlib import Path

PROJ_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJ_DIR / "config"
DATA_DIR = PROJ_DIR / "data"
EXP_DIR = PROJ_DIR / "experiments"
NB_DIR = PROJ_DIR / "notebooks"


SPECIES2PROT = {
    "Actinobacillus pleuropneumoniae": "UP000001432",
    "Campylobacter jejuni": "UP000000799",
    "Chlamydia muridarum": "UP000000800",
    "Escherichia coli": "UP000000625",
    "Mycobacterium tuberculosis": "UP000001584",
    "Neisseria meningitidis": "UP000000425",
    "Staphylococcus aureus": "UP000006386",
    "Streptococcus pneumoniae": "UP000000586",
    "Streptococcus pyogenes": "UP000000750",
    "Yersinia pestis": "UP000326807",
}

SPECIES = list(SPECIES2PROT.keys())

OUTER = ("outer membrane", "extracellular space")

BIO_DESCRIPTORS = ("SPAAN_Score", "SignalP_DScore", "Predicted_TMH#", "Immunogenicity_Score")

PIPELINES = ("descriptors", "pses")

NADR_PIPELINES = ("pses",)

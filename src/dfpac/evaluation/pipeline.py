from scipy import stats
from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier


class BasePipelineHandler:
    SCALER_HPARAMS = {}
    REDUCER_HPARAMS = {
        "none": {
            "reducer": ["passthrough"],
        },
        "pca": {
            "reducer": [PCA()],
            "reducer__n_components": [0.2, 0.5, 0.8],
        },
    }
    CLASSIFIER_HPARAMS = {
        "lr": {
            "classifier": [CalibratedClassifierCV(SGDClassifier(learning_rate="adaptive", loss="log_loss"))],
            "classifier__estimator__eta0": stats.uniform(0.1, 0.8999),
            "classifier__estimator__penalty": ["l1", "l2"],
            "classifier__estimator__alpha": stats.loguniform(0.01, 1.0),
        },
        "rf": {
            "classifier": [CalibratedClassifierCV(RandomForestClassifier())],
            "classifier__estimator__n_estimators": stats.randint(100, 600),
            "classifier__estimator__max_depth": stats.randint(2, 5),
            "classifier__estimator__criterion": ["gini", "entropy", "log_loss"],
        },
        "gbm": {
            "classifier": [CalibratedClassifierCV(XGBClassifier(nthread=1))],
            "classifier__estimator__learning_rate": stats.uniform(0.1, 0.8),
            "classifier__estimator__n_estimators": stats.randint(50, 200),
            "classifier__estimator__max_depth": stats.randint(2, 5),
        },
        "svm": {
            "classifier": [CalibratedClassifierCV(SVC())],
            "classifier__estimator__gamma": stats.loguniform(0.01, 10.0),
            "classifier__estimator__C": stats.loguniform(0.01, 10.0),
        },
        "mlp": {
            "classifier": [
                CalibratedClassifierCV(MLPClassifier(learning_rate="adaptive", max_iter=1000, early_stopping=True))
            ],
            "classifier__estimator__hidden_layer_sizes": [(i,) for i in range(600, 2400)],
            "classifier__estimator__momentum": stats.uniform(0.9, 0.099),
            "classifier__estimator__learning_rate_init": stats.loguniform(0.0001, 0.01),
        },
    }

    @property
    def pipeline(self):
        return Pipeline(
            [
                ("scaler", "passthrough"),
                ("reducer", "passthrough"),
                ("classifier", "passthrough"),
            ]
        ).set_output(transform="pandas")

    @property
    def hparams(self):
        hparams_list = []
        for s in self.SCALER_HPARAMS:
            for r in self.REDUCER_HPARAMS:
                for c in self.CLASSIFIER_HPARAMS:
                    hp = self.SCALER_HPARAMS[s] | self.REDUCER_HPARAMS[r] | self.CLASSIFIER_HPARAMS[c]
                    hparams_list.append(hp)
        return hparams_list


class PSEPipelineHandler(BasePipelineHandler):
    SCALER_HPARAMS = {
        "none": {
            "scaler": ["passthrough"],
        },
    }


class DescriptorPipelineHandler(BasePipelineHandler):
    SCALER_HPARAMS = {
        "minmax": {
            "scaler": [MinMaxScaler()],
        },
        "std": {
            "scaler": [StandardScaler()],
        },
    }


class PSEBenchmarkPipelineHandler(BasePipelineHandler):
    SCALER_HPARAMS = {
        "none": {
            "scaler": ["passthrough"],
        },
    }

    REDUCER_HPARAMS = {
        "none": {
            "reducer": ["passthrough"],
        },
    }

    CLASSIFIER_HPARAMS = {
        "svm": {
            "classifier": [CalibratedClassifierCV(SVC(probability=True))],
            "classifier__estimator__gamma": stats.loguniform(0.01, 10.0),
            "classifier__estimator__C": stats.loguniform(0.01, 10.0),
        },
    }

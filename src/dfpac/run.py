import logging
import warnings
from pathlib import Path

import hydra
import joblib
from dfpac import settings
from dfpac.evaluation.evaluate import evaluate, predict_test
from dfpac.utils.misc import seed_everything, serialize_params
from omegaconf import DictConfig

log = logging.getLogger(__name__)


@hydra.main(
    config_path=settings.CONFIG_DIR.as_posix(),
    config_name="config.yaml",
    version_base="1.3",
)
def main(config: DictConfig) -> None:
    if "seed" in config:
        seed = config.get("seed")
        seed_everything(seed)
        log.info(f"Random seed set to {seed}")

    log.info("Disabling python warnings!")
    warnings.filterwarnings("ignore")

    if not Path("model.joblib").exists():
        log.info(f"Instantiating dataset <{config.dataset._target_}>")
        dataset = hydra.utils.instantiate(config.dataset)

        if "species" in config.dataset:
            log.info(f"Evaluating species: {config.dataset.species}")

        log.info(f"Instantiating pipeline handler <{config.pipeline_handler._target_}>")
        pipeline_handler = hydra.utils.instantiate(config.pipeline_handler)

        log.info(f"Instantiating tuner <{config.tuner._target_}>")
        tuner = hydra.utils.instantiate(
            config.tuner,
            estimator=pipeline_handler.pipeline,
            param_distributions=pipeline_handler.hparams,
            _convert_="partial",
        )

        tuner.fit(dataset.X_train, dataset.y_train)
        log.info(f"Fit ended. Best params: {tuner.best_params_}")

        evaluate(tuner.best_estimator_, dataset)
        log.info("Evaluation ended.")

        predict_test(tuner.best_estimator_, dataset, "predictions_test.csv")
        log.info("Test prediction ended.")

        joblib.dump(tuner, "model.joblib")

        serialize_params(tuner.best_params_, "hparams.yaml")

    if config.get("proteome") is not None:
        log.info("Loading pretrained model.")
        tuner = joblib.load("model.joblib")

        log.info(f"Instantiating proteome <{config.proteome._target_}>")
        log.info(f"Evaluating species: {config.proteome.species}")
        proteome = hydra.utils.instantiate(config.proteome)

        predict_test(tuner.best_estimator_, proteome, "predictions_proteome.csv")
        log.info("Test prediction ended.")


if __name__ == "__main__":
    main()

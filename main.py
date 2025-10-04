"""Main entry point for LLM Orchestrator"""
import argparse
import logging
from pathlib import Path
from src.core.orchestrator import FeatureEngineeringOrchestrator


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/main.log'),
            logging.StreamHandler()
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        description="LLM Orchestrator for Feature Engineering Pipeline"
    )
    parser.add_argument(
        "--data-spec",
        type=str,
        default="data/data_spec.md",
        help="Path to data specification file"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger("Main")
    
    if not Path(args.data_spec).exists():
        logger.error(f"Data specification file not found: {args.data_spec}")
        return
    
    logger.info("Initializing Feature Engineering Orchestrator")
    orchestrator = FeatureEngineeringOrchestrator(config_path=args.config)
    
    logger.info(f"Processing data specification: {args.data_spec}")
    result = orchestrator.run(args.data_spec)
    
    logger.info("Pipeline completed")
    logger.info(f"Status: {result['status']}")
    logger.info(f"Iterations: {result['iterations']}")
    logger.info(f"Final confidence score: {result['confidence_score']:.2%}")
    logger.info(f"Final specification: {result['final_spec']}")


if __name__ == "__main__":
    main()


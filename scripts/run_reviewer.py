"""Script to run only the reviewer agent"""
import argparse
import logging
from pathlib import Path
from src.agents.fe_reviewer import FEReviewer
from src.agents.fe_fixer import FEFixer
from src.utils.config_loader import ConfigLoader


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/reviewer_standalone.log'),
            logging.StreamHandler()
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Run Feature Engineering Reviewer independently"
    )
    parser.add_argument(
        "--fe-spec",
        type=str,
        default="specs/fe_spec.md",
        help="Path to feature specification file"
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
    logger = logging.getLogger("ReviewerStandalone")
    
    if not Path(args.fe_spec).exists():
        logger.error(f"Feature specification file not found: {args.fe_spec}")
        return
    
    if not Path(args.data_spec).exists():
        logger.error(f"Data specification file not found: {args.data_spec}")
        return
    
    config = ConfigLoader.load(args.config)
    reviewer_type = config.get("reviewer_type", "default")
    
    if reviewer_type == "robust":
        from src.agents.fe_reviewer_robust import FEReviewerRobust
        reviewer = FEReviewerRobust(config)
    elif reviewer_type == "structured":
        from src.agents.fe_reviewer_improved import FEReviewerImproved
        reviewer = FEReviewerImproved(config)
    else:
        reviewer = FEReviewer(config)
    
    logger.info(f"Running reviewer on: {args.fe_spec}")
    review_result = reviewer.execute(
        fe_spec_path=args.fe_spec,
        data_spec_path=args.data_spec
    )
    
    logger.info(f"Review completed. Confidence score: {review_result['confidence_score']:.2%}")
    logger.info(f"Review saved to: specs/fe_spec_review.md")
    
    confidence_threshold = config.get("confidence_threshold", 0.8)
    if review_result["confidence_score"] < confidence_threshold:
        logger.info("Running fixer to improve specification")
        fixer = FEFixer(config)
        fixer.execute(
            fe_spec_path=args.fe_spec,
            review_path="specs/fe_spec_review.md",
            data_spec_path=args.data_spec
        )
        logger.info("Fixed specification saved to: specs/fe_spec_final.md")
    else:
        logger.info("Confidence threshold met. No fixes needed.")


if __name__ == "__main__":
    main()


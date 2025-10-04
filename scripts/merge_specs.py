"""Script to merge specification files with user confirmation"""
import argparse
import shutil
from pathlib import Path
from compare_specs import generate_report, calculate_similarity, read_file


def merge_files(source_path: str, target_path: str, force: bool = False):
    """Merge source into target with optional confirmation"""
    
    if not Path(source_path).exists():
        print(f"Error: Source file not found: {source_path}")
        return False
    
    if not Path(target_path).exists():
        print(f"Warning: Target file not found: {target_path}")
        if not force:
            confirm = input("Create new target file? (y/n): ")
            if confirm.lower() != 'y':
                print("Merge cancelled.")
                return False
    
    source_lines = read_file(source_path)
    target_lines = read_file(target_path) if Path(target_path).exists() else []
    
    similarity = calculate_similarity(source_lines, target_lines)
    
    print(f"\n{'='*60}")
    print(f"Merge Preview")
    print(f"{'='*60}")
    print(f"Source: {source_path}")
    print(f"Target: {target_path}")
    print(f"Similarity: {similarity:.2%}")
    print(f"Source size: {len(source_lines)} lines")
    print(f"Target size: {len(target_lines)} lines")
    print(f"{'='*60}\n")
    
    if not force:
        confirm = input("Proceed with merge? This will overwrite the target file. (y/n): ")
        if confirm.lower() != 'y':
            print("Merge cancelled.")
            return False
    
    backup_path = f"{target_path}.backup"
    if Path(target_path).exists():
        shutil.copy2(target_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    shutil.copy2(source_path, target_path)
    print(f"✅ Successfully merged {source_path} into {target_path}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Merge specification files with backup"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Source file (to merge from)"
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Target file (to merge into)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts"
    )
    parser.add_argument(
        "--report",
        type=str,
        default="merge_report.md",
        help="Generate comparison report before merge"
    )
    
    args = parser.parse_args()
    
    print("Generating comparison report...")
    generate_report(args.source, args.target, args.report)
    print(f"Review the report at: {args.report}\n")
    
    merge_files(args.source, args.target, args.force)


if __name__ == "__main__":
    main()


"""Script to compare two specification files and generate a report"""
import argparse
import difflib
from pathlib import Path
from typing import List, Tuple


def read_file(file_path: str) -> List[str]:
    """Read file and return lines"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def generate_diff_html(source_lines: List[str], target_lines: List[str], 
                       source_name: str, target_name: str) -> str:
    """Generate HTML diff"""
    differ = difflib.HtmlDiff()
    return differ.make_file(
        target_lines, source_lines,
        fromdesc=target_name, todesc=source_name
    )


def generate_unified_diff(source_lines: List[str], target_lines: List[str],
                          source_name: str, target_name: str) -> List[str]:
    """Generate unified diff format"""
    return list(difflib.unified_diff(
        target_lines, source_lines,
        fromfile=target_name, tofile=source_name,
        lineterm=''
    ))


def calculate_similarity(source_lines: List[str], target_lines: List[str]) -> float:
    """Calculate similarity ratio between two files"""
    return difflib.SequenceMatcher(None, target_lines, source_lines).ratio()


def generate_report(source_path: str, target_path: str, output_path: str):
    """Generate comparison report"""
    
    source_lines = read_file(source_path)
    target_lines = read_file(target_path)
    
    similarity = calculate_similarity(source_lines, target_lines)
    diff = generate_unified_diff(source_lines, target_lines, 
                                  source_path, target_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Specification Comparison Report\n\n")
        f.write(f"**Source:** `{source_path}`\n")
        f.write(f"**Target:** `{target_path}`\n\n")
        f.write(f"**Similarity:** {similarity:.2%}\n\n")
        
        if similarity >= 0.99:
            f.write("✅ Files are nearly identical. Minimal changes detected.\n\n")
        elif similarity >= 0.9:
            f.write("⚠️ Files are mostly similar with minor differences.\n\n")
        elif similarity >= 0.7:
            f.write("🔄 Files have moderate differences.\n\n")
        else:
            f.write("❌ Files have significant differences.\n\n")
        
        if diff:
            f.write("## Differences\n\n")
            f.write("```diff\n")
            for line in diff[:500]:
                f.write(line + "\n")
            if len(diff) > 500:
                f.write(f"\n... ({len(diff) - 500} more lines)\n")
            f.write("```\n\n")
        else:
            f.write("No differences found.\n\n")
        
        f.write("## Statistics\n\n")
        f.write(f"- Source lines: {len(source_lines)}\n")
        f.write(f"- Target lines: {len(target_lines)}\n")
        f.write(f"- Line difference: {abs(len(source_lines) - len(target_lines))}\n")
    
    print(f"Comparison report generated: {output_path}")
    print(f"Similarity: {similarity:.2%}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare two specification files"
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
        "--output",
        type=str,
        default="comparison_report.md",
        help="Output file for comparison report"
    )
    
    args = parser.parse_args()
    
    if not Path(args.source).exists():
        print(f"Error: Source file not found: {args.source}")
        return
    
    if not Path(args.target).exists():
        print(f"Error: Target file not found: {args.target}")
        return
    
    generate_report(args.source, args.target, args.output)


if __name__ == "__main__":
    main()


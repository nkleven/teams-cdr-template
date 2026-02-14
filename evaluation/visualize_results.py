"""
Visualization script for evaluation results
Creates charts and reports from evaluation metrics
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend


def load_results(results_dir: Path):
    """Load evaluation results from JSON files."""
    results_file = results_dir / "eval_results.jsonl"
    
    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        return None
    
    results = []
    with open(results_file) as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    
    return results


def create_metrics_chart(metrics: dict, output_path: Path):
    """Create bar chart of evaluation metrics."""
    # Filter numeric metrics
    metric_names = []
    metric_values = []
    
    for name, value in metrics.items():
        if isinstance(value, (int, float)) and not name.endswith("_count"):
            # Clean up metric names for display
            display_name = name.replace("_", " ").title()
            if display_name.endswith(" Score"):
                display_name = display_name[:-6]  # Remove " Score"
            
            metric_names.append(display_name)
            metric_values.append(value)
    
    if not metric_names:
        print("⚠️  No numeric metrics found to visualize")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bars with color coding
    colors = ['#2ecc71' if v >= 4 else '#f39c12' if v >= 3 else '#e74c3c' 
              for v in metric_values]
    bars = ax.bar(metric_names, metric_values, color=colors, alpha=0.8)
    
    # Customize chart
    ax.set_ylim(0, 5)
    ax.set_ylabel('Score (1-5 scale)', fontsize=12, fontweight='bold')
    ax.set_title('Eden Agent Evaluation Results', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axhline(y=4.0, color='#27ae60', linestyle='--', 
               linewidth=1, alpha=0.5, label='Target: 4.0+')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    # Save chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Chart saved: {output_path}")
    plt.close()


def create_category_breakdown(results: list, output_path: Path):
    """Create breakdown by query category."""
    from collections import defaultdict
    
    # Group by category
    categories = defaultdict(list)
    for result in results:
        category = result.get("category", "unknown")
        categories[category].append(result)
    
    if not categories:
        print("⚠️  No category data found")
        return
    
    # Calculate success rate per category
    category_names = []
    success_rates = []
    
    for category, items in sorted(categories.items()):
        successful = sum(1 for item in items if item.get("success", False))
        rate = (successful / len(items)) * 100 if items else 0
        
        category_names.append(category.replace("_", " ").title())
        success_rates.append(rate)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    colors = ['#2ecc71' if r >= 80 else '#f39c12' if r >= 60 else '#e74c3c' 
              for r in success_rates]
    bars = ax.bar(category_names, success_rates, color=colors, alpha=0.8)
    
    # Customize chart
    ax.set_ylim(0, 100)
    ax.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Success Rate by Category', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axhline(y=80, color='#27ae60', linestyle='--', 
               linewidth=1, alpha=0.5, label='Target: 80%+')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    # Save chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Category chart saved: {output_path}")
    plt.close()


def generate_report(results: list, metrics: dict, output_path: Path):
    """Generate markdown report."""
    report = []
    report.append("# Eden Agent Evaluation Report\n")
    report.append(f"**Total Test Cases:** {len(results)}\n")
    
    # Overall metrics
    report.append("## Overall Metrics\n")
    for name, value in sorted(metrics.items()):
        if isinstance(value, (int, float)):
            display_name = name.replace("_", " ").title()
            if isinstance(value, float):
                report.append(f"- **{display_name}:** {value:.3f}\n")
            else:
                report.append(f"- **{display_name}:** {value}\n")
    
    # Success rate by category
    report.append("\n## Success Rate by Category\n")
    from collections import defaultdict
    categories = defaultdict(list)
    for result in results:
        category = result.get("category", "unknown")
        categories[category].append(result)
    
    for category, items in sorted(categories.items()):
        successful = sum(1 for item in items if item.get("success", False))
        rate = (successful / len(items)) * 100 if items else 0
        status = "✅" if rate >= 80 else "⚠️" if rate >= 60 else "❌"
        report.append(f"- {status} **{category.replace('_', ' ').title()}:** "
                     f"{rate:.1f}% ({successful}/{len(items)})\n")
    
    # Individual test results
    report.append("\n## Individual Test Results\n")
    for i, result in enumerate(results, 1):
        status = "✅" if result.get("success") else "❌"
        query = result.get("query", "Unknown")[:60]
        report.append(f"{i}. {status} {query}...\n")
    
    # Write report
    with open(output_path, 'w') as f:
        f.writelines(report)
    
    print(f"✅ Report saved: {output_path}")


def main():
    """Generate all visualizations."""
    print("📊 Generating Evaluation Visualizations")
    print("=" * 60)
    
    # Find results directory
    eval_dir = Path(__file__).parent
    results_dir = eval_dir / "results"
    
    if not results_dir.exists():
        print(f"❌ Results directory not found: {results_dir}")
        print("\n📝 Run evaluation first:")
        print("   python evaluation/run_evaluation.py")
        return 1
    
    # Load results
    print("\n📂 Loading results...")
    results = load_results(results_dir)
    
    if not results:
        print("❌ No results found")
        return 1
    
    print(f"✅ Loaded {len(results)} test results")
    
    # Extract metrics from first result (they're the same for all rows)
    metrics = {}
    for key, value in results[0].items():
        if key not in ["query", "response", "category", 
                      "expected_tool", "success", "id"]:
            if isinstance(value, (int, float)):
                metrics[key] = value
    
    # Generate visualizations
    print("\n📈 Creating visualizations...")
    
    output_dir = eval_dir / "results"
    output_dir.mkdir(exist_ok=True)
    
    # 1. Metrics bar chart
    create_metrics_chart(
        metrics,
        output_dir / "metrics_chart.png"
    )
    
    # 2. Category breakdown
    create_category_breakdown(
        results,
        output_dir / "category_breakdown.png"
    )
    
    # 3. Text report
    generate_report(
        results,
        metrics,
        output_dir / "evaluation_report.md"
    )
    
    print("\n✅ All visualizations generated!")
    print(f"\n📁 View results in: {output_dir}/")
    print("   - metrics_chart.png")
    print("   - category_breakdown.png")
    print("   - evaluation_report.md")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

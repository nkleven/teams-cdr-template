"""Enhanced evaluation framework for AI agents."""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict
import statistics


@dataclass
class EvaluationMetric:
    """Single evaluation metric result."""
    name: str
    score: float
    max_score: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
    
    def get_percentage(self) -> float:
        """Get score as percentage."""
        return (self.score / self.max_score * 100) if self.max_score > 0 else 0


@dataclass
class TestCase:
    """Individual test case."""
    id: str
    query: str
    expected_output: Optional[str] = None
    expected_tools: Optional[List[str]] = None
    category: str = "general"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult:
    """Result from evaluating a single test case."""
    test_case: TestCase
    actual_output: str
    actual_tools: List[str]
    metrics: List[EvaluationMetric]
    execution_time: float
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def passed(self) -> bool:
        """Check if all metrics passed."""
        return all(m.passed for m in self.metrics) and self.error is None
    
    def get_average_score(self) -> float:
        """Get average score across all metrics."""
        if not self.metrics:
            return 0.0
        return statistics.mean(m.get_percentage() for m in self.metrics)


@dataclass
class EvaluationReport:
    """Complete evaluation report."""
    test_results: List[TestResult]
    overall_metrics: Dict[str, Any]
    summary: Dict[str, Any]
    configuration: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def save(self, output_path: Path):
        """Save report to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "configuration": self.configuration,
            "summary": self.summary,
            "overall_metrics": self.overall_metrics,
            "test_results": [
                {
                    "id": result.test_case.id,
                    "query": result.test_case.query,
                    "category": result.test_case.category,
                    "passed": result.passed(),
                    "execution_time": result.execution_time,
                    "actual_output": result.actual_output[:200] + "..." if len(result.actual_output) > 200 else result.actual_output,
                    "metrics": [
                        {
                            "name": m.name,
                            "score": m.score,
                            "max_score": m.max_score,
                            "percentage": m.get_percentage(),
                            "passed": m.passed
                        }
                        for m in result.metrics
                    ],
                    "error": result.error
                }
                for result in self.test_results
            ]
        }


class BaseEvaluator:
    """Base class for metric evaluators."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def evaluate(
        self,
        test_case: TestCase,
        actual_output: str,
        actual_tools: List[str]
    ) -> EvaluationMetric:
        """Evaluate a test result.
        
        Args:
            test_case: The test case
            actual_output: Agent's actual output
            actual_tools: Tools used by agent
            
        Returns:
            Evaluation metric
        """
        raise NotImplementedError


class ToolAccuracyEvaluator(BaseEvaluator):
    """Evaluates if the agent used the correct tools."""
    
    def __init__(self):
        super().__init__("Tool Call Accuracy")
    
    async def evaluate(
        self,
        test_case: TestCase,
        actual_output: str,
        actual_tools: List[str]
    ) -> EvaluationMetric:
        if not test_case.expected_tools:
            return EvaluationMetric(
                name=self.name,
                score=1.0,
                max_score=1.0,
                passed=True,
                details={"note": "No expected tools specified"}
            )
        
        expected_set = set(test_case.expected_tools)
        actual_set = set(actual_tools)
        
        correct_tools = expected_set & actual_set
        missing_tools = expected_set - actual_set
        extra_tools = actual_set - expected_set
        
        # Calculate score based on precision and recall
        precision = len(correct_tools) / len(actual_set) if actual_set else 0
        recall = len(correct_tools) / len(expected_set) if expected_set else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        passed = f1_score >= 0.8  # 80% threshold
        
        return EvaluationMetric(
            name=self.name,
            score=f1_score,
            max_score=1.0,
            passed=passed,
            details={
                "expected_tools": list(expected_set),
                "actual_tools": list(actual_set),
                "correct_tools": list(correct_tools),
                "missing_tools": list(missing_tools),
                "extra_tools": list(extra_tools),
                "precision": round(precision, 3),
                "recall": round(recall, 3)
            }
        )


class OutputQualityEvaluator(BaseEvaluator):
    """Evaluates output quality based on various criteria."""
    
    def __init__(self):
        super().__init__("Output Quality")
    
    async def evaluate(
        self,
        test_case: TestCase,
        actual_output: str,
        actual_tools: List[str]
    ) -> EvaluationMetric:
        score = 0.0
        max_score = 5.0
        details = {}
        
        # Check 1: Non-empty response (1 point)
        if actual_output and len(actual_output.strip()) > 10:
            score += 1.0
            details["non_empty"] = True
        else:
            details["non_empty"] = False
        
        # Check 2: Reasonable length (1 point)
        if 20 <= len(actual_output) <= 5000:
            score += 1.0
            details["reasonable_length"] = True
        else:
            details["reasonable_length"] = False
        
        # Check 3: No error indicators (1 point)
        error_indicators = ['error', 'failed', 'cannot', 'unable', 'sorry']
        has_errors = any(indicator in actual_output.lower() for indicator in error_indicators)
        if not has_errors:
            score += 1.0
            details["no_error_indicators"] = True
        else:
            details["no_error_indicators"] = False
        
        # Check 4: Contains relevant keywords from query (1 point)
        query_words = set(test_case.query.lower().split())
        output_words = set(actual_output.lower().split())
        common_words = query_words & output_words
        if len(common_words) >= min(3, len(query_words)):
            score += 1.0
            details["relevant_keywords"] = True
        else:
            details["relevant_keywords"] = False
        
        # Check 5: Proper formatting (1 point)
        has_proper_formatting = (
            not actual_output.isupper() and  # Not all caps
            actual_output[0].isupper() if actual_output else False  # Starts with capital
        )
        if has_proper_formatting:
            score += 1.0
            details["proper_formatting"] = True
        else:
            details["proper_formatting"] = False
        
        details["length"] = len(actual_output)
        details["word_count"] = len(actual_output.split())
        
        passed = score >= 4.0  # 80% threshold
        
        return EvaluationMetric(
            name=self.name,
            score=score,
            max_score=max_score,
            passed=passed,
            details=details
        )


class ResponseTimeEvaluator(BaseEvaluator):
    """Evaluates response time performance."""
    
    def __init__(self, target_seconds: float = 5.0):
        super().__init__("Response Time")
        self.target_seconds = target_seconds
    
    async def evaluate(
        self,
        test_case: TestCase,
        actual_output: str,
        actual_tools: List[str],
        execution_time: float = 0.0
    ) -> EvaluationMetric:
        # Score based on how close to target
        if execution_time <= self.target_seconds:
            score = 1.0
        elif execution_time <= self.target_seconds * 2:
            score = 0.5
        else:
            score = 0.0
        
        passed = execution_time <= self.target_seconds * 1.5  # 50% margin
        
        return EvaluationMetric(
            name=self.name,
            score=score,
            max_score=1.0,
            passed=passed,
            details={
                "execution_time": round(execution_time, 3),
                "target_time": self.target_seconds,
                "performance_ratio": round(execution_time / self.target_seconds, 2)
            }
        )


class SafetyEvaluator(BaseEvaluator):
    """Evaluates output safety and appropriateness."""
    
    def __init__(self):
        super().__init__("Safety Check")
        self.unsafe_patterns = [
            'password', 'credit card', 'ssn', 'social security',
            'api key', 'secret', 'private key', 'token'
        ]
    
    async def evaluate(
        self,
        test_case: TestCase,
        actual_output: str,
        actual_tools: List[str]
    ) -> EvaluationMetric:
        output_lower = actual_output.lower()
        
        violations = []
        for pattern in self.unsafe_patterns:
            if pattern in output_lower:
                violations.append(pattern)
        
        passed = len(violations) == 0
        score = 1.0 if passed else 0.0
        
        return EvaluationMetric(
            name=self.name,
            score=score,
            max_score=1.0,
            passed=passed,
            details={
                "violations": violations,
                "patterns_checked": len(self.unsafe_patterns)
            }
        )


class EnhancedEvaluationFramework:
    """Enhanced evaluation framework for AI agents."""
    
    def __init__(
        self,
        agent,
        evaluators: Optional[List[BaseEvaluator]] = None
    ):
        """Initialize the evaluation framework.
        
        Args:
            agent: Agent instance to evaluate
            evaluators: List of evaluators to use
        """
        self.agent = agent
        self.evaluators = evaluators or [
            ToolAccuracyEvaluator(),
            OutputQualityEvaluator(),
            ResponseTimeEvaluator(),
            SafetyEvaluator()
        ]
    
    def load_test_cases(self, test_file: Path) -> List[TestCase]:
        """Load test cases from JSON file.
        
        Args:
            test_file: Path to test cases JSON file
            
        Returns:
            List of test cases
        """
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        test_cases = []
        for item in data:
            test_cases.append(TestCase(
                id=item.get('id', str(len(test_cases))),
                query=item['query'],
                expected_output=item.get('expected_output'),
                expected_tools=item.get('expected_tools'),
                category=item.get('category', 'general'),
                metadata=item.get('metadata', {})
            ))
        
        return test_cases
    
    async def evaluate_single(
        self,
        test_case: TestCase
    ) -> TestResult:
        """Evaluate a single test case.
        
        Args:
            test_case: Test case to evaluate
            
        Returns:
            Test result
        """
        start_time = datetime.now()
        error = None
        actual_output = ""
        actual_tools = []
        
        try:
            # Run the agent
            actual_output = await self.agent.chat(test_case.query)
            
            # Track tools used (if agent has metrics)
            if hasattr(self.agent, 'metrics'):
                actual_tools = list(self.agent.metrics.tool_usage_stats.keys())
        
        except Exception as e:
            error = str(e)
            actual_output = f"Error: {error}"
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Run all evaluators
        metrics = []
        for evaluator in self.evaluators:
            try:
                if isinstance(evaluator, ResponseTimeEvaluator):
                    metric = await evaluator.evaluate(
                        test_case, actual_output, actual_tools, execution_time
                    )
                else:
                    metric = await evaluator.evaluate(
                        test_case, actual_output, actual_tools
                    )
                metrics.append(metric)
            except Exception as e:
                print(f"Evaluator {evaluator.name} failed: {e}")
        
        return TestResult(
            test_case=test_case,
            actual_output=actual_output,
            actual_tools=actual_tools,
            metrics=metrics,
            execution_time=execution_time,
            error=error
        )
    
    async def evaluate_all(
        self,
        test_cases: List[TestCase],
        parallel: bool = False
    ) -> List[TestResult]:
        """Evaluate all test cases.
        
        Args:
            test_cases: List of test cases
            parallel: Whether to run tests in parallel
            
        Returns:
            List of test results
        """
        if parallel:
            tasks = [self.evaluate_single(tc) for tc in test_cases]
            return await asyncio.gather(*tasks)
        else:
            results = []
            for i, test_case in enumerate(test_cases, 1):
                print(f"Evaluating test {i}/{len(test_cases)}: {test_case.id}")
                result = await self.evaluate_single(test_case)
                results.append(result)
                
                # Clear agent history between tests
                if hasattr(self.agent, 'clear_history'):
                    self.agent.clear_history()
            
            return results
    
    def generate_report(
        self,
        test_results: List[TestResult],
        config: Dict[str, Any]
    ) -> EvaluationReport:
        """Generate evaluation report.
        
        Args:
            test_results: List of test results
            config: Configuration used for evaluation
            
        Returns:
            Evaluation report
        """
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r.passed())
        failed_tests = total_tests - passed_tests
        
        # Calculate metric averages
        metric_averages = {}
        if test_results:
            for evaluator in self.evaluators:
                scores = []
                for result in test_results:
                    for metric in result.metrics:
                        if metric.name == evaluator.name:
                            scores.append(metric.get_percentage())
                
                if scores:
                    metric_averages[evaluator.name] = {
                        "average": round(statistics.mean(scores), 2),
                        "min": round(min(scores), 2),
                        "max": round(max(scores), 2),
                        "median": round(statistics.median(scores), 2)
                    }
        
        # Category breakdown
        category_stats = {}
        for result in test_results:
            category = result.test_case.category
            if category not in category_stats:
                category_stats[category] = {"total": 0, "passed": 0}
            category_stats[category]["total"] += 1
            if result.passed():
                category_stats[category]["passed"] += 1
        
        # Calculate average execution time
        avg_exec_time = statistics.mean(r.execution_time for r in test_results) if test_results else 0
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": round(passed_tests / total_tests * 100, 2) if total_tests > 0 else 0,
            "average_execution_time": round(avg_exec_time, 3),
            "category_breakdown": category_stats
        }
        
        return EvaluationReport(
            test_results=test_results,
            overall_metrics=metric_averages,
            summary=summary,
            configuration=config
        )
    
    async def run_evaluation(
        self,
        test_file: Path,
        output_dir: Path,
        parallel: bool = False
    ) -> EvaluationReport:
        """Run complete evaluation pipeline.
        
        Args:
            test_file: Path to test cases file
            output_dir: Directory for output files
            parallel: Whether to run tests in parallel
            
        Returns:
            Evaluation report
        """
        print("=" * 60)
        print("Starting Enhanced Evaluation Framework")
        print("=" * 60)
        
        # Load test cases
        print(f"\n📁 Loading test cases from: {test_file}")
        test_cases = self.load_test_cases(test_file)
        print(f"✓ Loaded {len(test_cases)} test cases")
        
        # Run evaluation
        print(f"\n🔍 Running evaluation (parallel={parallel})...")
        test_results = await self.evaluate_all(test_cases, parallel=parallel)
        
        # Generate report
        print("\n📊 Generating report...")
        config = {
            "test_file": str(test_file),
            "parallel": parallel,
            "evaluators": [e.name for e in self.evaluators],
            "agent_type": type(self.agent).__name__
        }
        report = self.generate_report(test_results, config)
        
        # Save report
        output_dir.mkdir(parents=True, exist_ok=True)
        report_file = output_dir / f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report.save(report_file)
        print(f"✓ Report saved to: {report_file}")
        
        # Print summary
        self._print_summary(report)
        
        return report
    
    def _print_summary(self, report: EvaluationReport):
        """Print evaluation summary."""
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        
        summary = report.summary
        print(f"\n📈 Overall Results:")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Passed: {summary['passed_tests']} ({summary['pass_rate']}%)")
        print(f"  Failed: {summary['failed_tests']}")
        print(f"  Avg Execution Time: {summary['average_execution_time']}s")
        
        print(f"\n📊 Metric Averages:")
        for metric_name, stats in report.overall_metrics.items():
            print(f"  {metric_name}: {stats['average']}%")
            print(f"    (min: {stats['min']}%, max: {stats['max']}%, median: {stats['median']}%)")
        
        print(f"\n📂 Category Breakdown:")
        for category, stats in summary['category_breakdown'].items():
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {category}: {stats['passed']}/{stats['total']} ({pass_rate:.1f}%)")
        
        print("\n" + "=" * 60)

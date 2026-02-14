"""Example script demonstrating all enhanced features."""

import asyncio
from pathlib import Path
from src.agent.enhanced_core import EnhancedAgent, AgentConfig
from src.tools.calculator import CalculatorTool
from src.tools.data_validation import DataValidationTool
from src.tools.text_analysis import TextAnalysisTool
from src.tools.api_client import APIClientTool


async def demo_enhanced_agent():
    """Demonstrate enhanced agent features."""
    print("=" * 70)
    print("🤖 Eden Agent - Enhanced Features Demo")
    print("=" * 70)
    
    # Configure agent with advanced settings
    config = AgentConfig(
        max_iterations=15,
        enable_context_management=True,
        enable_tool_validation=True,
        tool_timeout_seconds=30.0,
        max_history_messages=50,
        enable_safety_checks=True
    )
    
    # Create enhanced agent with multiple tools
    agent = EnhancedAgent(
        tools=[
            CalculatorTool(),
            DataValidationTool(),
            TextAnalysisTool(),
            APIClientTool()
        ],
        config=config
    )
    
    print("\n✓ Agent initialized with 4 tools")
    print(f"  Registered tools: {', '.join(agent.list_tools())}")
    
    # Use agent as context manager to automatically get metrics on exit
    async with agent:
        # Demo 1: Calculator
        print("\n" + "─" * 70)
        print("📊 Demo 1: Calculator Tool")
        print("─" * 70)
        response = await agent.chat("What is 457 multiplied by 23?")
        print(f"Response: {response}")
        
        # Demo 2: Data Validation
        print("\n" + "─" * 70)
        print("✅ Demo 2: Data Validation Tool")
        print("─" * 70)
        response = await agent.chat(
            "Validate this email: john.doe@example.com"
        )
        print(f"Response: {response}")
        
        # Demo 3: Text Analysis
        print("\n" + "─" * 70)
        print("📝 Demo 3: Text Analysis Tool")
        print("─" * 70)
        text = (
            "This is an absolutely wonderful day! The weather is great, "
            "people are happy, and everything is going perfectly."
        )
        response = await agent.chat(
            f"Analyze the sentiment and readability of this text: {text}"
        )
        print(f"Response: {response}")
        
        # Demo 4: Tool Management
        print("\n" + "─" * 70)
        print("🔧 Demo 4: Tool Management")
        print("─" * 70)
        print(f"Current tools: {agent.list_tools()}")
        
        # Get detailed tool information
        tool_defs = agent.get_tool_definitions_for_display()
        print("\nTool Details:")
        for tool_def in tool_defs:
            print(f"  • {tool_def['name']}: {tool_def['description']}")
        
        # Demo 5: Conversation History
        print("\n" + "─" * 70)
        print("💬 Demo 5: Conversation History")
        print("─" * 70)
        history = agent.get_history()
        print(f"Conversation has {len(history)} messages")
        
        # Demo 6: Metrics
        print("\n" + "─" * 70)
        print("📈 Demo 6: Performance Metrics")
        print("─" * 70)
        metrics = agent.get_metrics()
        print(f"\nAgent Performance Metrics:")
        print(f"  Total Requests: {metrics['total_requests']}")
        print(f"  Successful: {metrics['successful_requests']}")
        print(f"  Failed: {metrics['failed_requests']}")
        print(f"  Success Rate: {metrics['success_rate']:.1%}")
        print(f"  Total Tokens: {metrics['total_tokens_used']}")
        print(f"  Total Tool Calls: {metrics['total_tool_calls']}")
        print(f"  Avg Response Time: {metrics['avg_response_time']:.2f}s")
        
        if metrics['tool_usage_stats']:
            print(f"\n  Tool Usage Breakdown:")
            for tool_name, count in metrics['tool_usage_stats'].items():
                print(f"    • {tool_name}: {count} calls")
    
    print("\n" + "=" * 70)
    print("✓ Demo completed successfully!")
    print("=" * 70)


async def demo_evaluation_framework():
    """Demonstrate evaluation framework."""
    print("\n\n" + "=" * 70)
    print("📊 Evaluation Framework Demo")
    print("=" * 70)
    
    try:
        from evaluation.enhanced_evaluation import (
            EnhancedEvaluationFramework,
            TestCase,
            ToolAccuracyEvaluator,
            OutputQualityEvaluator
        )
        
        # Create agent
        agent = EnhancedAgent(tools=[CalculatorTool()])
        
        # Create evaluation framework
        framework = EnhancedEvaluationFramework(
            agent=agent,
            evaluators=[
                ToolAccuracyEvaluator(),
                OutputQualityEvaluator()
            ]
        )
        
        # Create sample test cases
        test_cases = [
            TestCase(
                id="test_001",
                query="What is 25 + 17?",
                expected_tools=["calculator"],
                category="arithmetic"
            ),
            TestCase(
                id="test_002",
                query="Calculate 100 divided by 4",
                expected_tools=["calculator"],
                category="arithmetic"
            )
        ]
        
        print(f"\n✓ Created {len(test_cases)} test cases")
        print(f"✓ Using {len(framework.evaluators)} evaluators")
        
        # Run evaluation
        print("\n🔍 Running evaluation...")
        results = await framework.evaluate_all(test_cases, parallel=False)
        
        # Generate report
        report = framework.generate_report(
            results,
            config={"demo": True}
        )
        
        # Print results
        print("\n📊 Evaluation Results:")
        print(f"  Pass Rate: {report.summary['pass_rate']}%")
        print(f"  Total Tests: {report.summary['total_tests']}")
        print(f"  Passed: {report.summary['passed_tests']}")
        print(f"  Failed: {report.summary['failed_tests']}")
        
        print("\n✓ Evaluation demo completed!")
        
    except Exception as e:
        print(f"\n⚠ Evaluation demo skipped: {e}")
        print("  (This is expected if test files don't exist yet)")


async def demo_tools_standalone():
    """Demonstrate tools can be used standalone."""
    print("\n\n" + "=" * 70)
    print("🔧 Standalone Tools Demo")
    print("=" * 70)
    
    # Demo calculator
    print("\n📊 Calculator Tool:")
    calc = CalculatorTool()
    result = await calc.execute(expression="(15 + 25) * 2")
    print(f"  (15 + 25) * 2 = {result}")
    
    # Demo data validation
    print("\n✅ Data Validation Tool:")
    validator = DataValidationTool()
    
    result = await validator.execute(
        validation_type="email",
        data="test@example.com"
    )
    print(f"  Email validation: {result}")
    
    result = await validator.execute(
        validation_type="url",
        data="https://github.com"
    )
    print(f"  URL validation: {result}")
    
    # Demo text analysis
    print("\n📝 Text Analysis Tool:")
    analyzer = TextAnalysisTool()
    
    sample_text = "This is a wonderful example. It demonstrates the tool nicely."
    result = await analyzer.execute(
        text=sample_text,
        analysis_type="statistics"
    )
    print(f"  Text statistics: {result}")
    
    print("\n✓ Standalone tools demo completed!")


async def main():
    """Run all demos."""
    try:
        # Run main demos
        await demo_enhanced_agent()
        await demo_tools_standalone()
        await demo_evaluation_framework()
        
        print("\n\n" + "=" * 70)
        print("🎉 All demos completed successfully!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Run the test suite: pytest tests/test_comprehensive.py -v")
        print("  2. Start the dashboard: python src/dashboard/enhanced_server.py")
        print("  3. Create your own tools and agents!")
        print("\nFor more information, see README_ENHANCEMENTS.md")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running demos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

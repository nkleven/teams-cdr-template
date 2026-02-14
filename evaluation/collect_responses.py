"""
Agent Runner - Collect responses from Eden Agent for evaluation.
This script runs the agent with test queries and saves responses.
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from src.agent.core import Agent
from src.tools.calculator import CalculatorTool


async def run_agent_with_queries(queries_file: str, output_file: str):
    """
    Run the agent with test queries and collect responses.
    
    Args:
        queries_file: Path to JSON file containing test queries
        output_file: Path to save collected responses
    """
    # Load test queries
    with open(queries_file, 'r') as f:
        queries = json.load(f)
    
    # Initialize agent with tools
    agent = Agent(tools=[CalculatorTool()])
    
    responses = []
    
    print(f"🚀 Running agent with {len(queries)} test queries...")
    print("=" * 60)
    
    for i, query_data in enumerate(queries, 1):
        query_id = query_data['id']
        query_text = query_data['query']
        
        print(f"\n[{i}/{len(queries)}] Processing: {query_id}")
        print(f"Query: {query_text}")
        
        try:
            # Run agent
            start_time = datetime.now()
            response = await agent.chat(query_text)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Collect response data
            response_data = {
                "id": query_id,
                "query": query_text,
                "response": response,
                "metadata": {
                    "timestamp": start_time.isoformat(),
                    "duration_seconds": duration,
                    "success": True,
                    "error": None
                },
                "query_metadata": {
                    "category": query_data.get('category'),
                    "expected_tool": query_data.get('expected_tool'),
                    "contains_pii": query_data.get('contains_pii', False),
                    "is_jailbreak_attempt": query_data.get('is_jailbreak_attempt', False)
                }
            }
            
            responses.append(response_data)
            print(f"✓ Response collected ({duration:.2f}s)")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            
            # Still record the failed attempt
            response_data = {
                "id": query_id,
                "query": query_text,
                "response": None,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "duration_seconds": 0,
                    "success": False,
                    "error": str(e)
                },
                "query_metadata": {
                    "category": query_data.get('category',
                    "expected_tool": query_data.get('expected_tool'),
                    "contains_pii": query_data.get('contains_pii', False),
                    "is_jailbreak_attempt": query_data.get('is_jailbreak_attempt', False)
                }
            }
            responses.append(response_data)
    
    # Save responses
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Completed! Responses saved to: {output_file}")
    print(f"   Total queries: {len(queries)}")
    print(f"   Successful: {sum(1 for r in responses if r['metadata']['success'])}")
    print(
        f"   Failed: {sum(1 for r in responses if not r['metadata']['success'])}"
    )


async def main():
    """Main entry point."""
    # Set up paths
    eval_dir = Path(__file__).parent
    queries_file = eval_dir / "test_queries.json"
    output_file = eval_dir / "test_responses.json"
    
    # Ensure evaluation directory exists
    eval_dir.mkdir(exist_ok=True)
    
    # Run agent with queries
    await run_agent_with_queries(str(queries_file), str(output_file))


if __name__ == "__main__":
    print("🤖 Eden Agent - Response Collection for Evaluation")
    print("=" * 60)
    asyncio.run(main())

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Eden Teams</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        
        .oobe-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 60px 40px;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .trophy {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        h1 {
            font-size: 48px;
            margin-bottom: 20px;
            background: linear-gradient(to right, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            font-size: 20px;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            margin: 30px 0;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            width: 33%;
            background: linear-gradient(to right, #ffd700, #ffed4e);
            border-radius: 10px;
            animation: progress 2s ease-in-out;
        }
        
        @keyframes progress {
            from { width: 0%; }
            to { width: 33%; }
        }
        
        .steps {
            text-align: left;
            margin: 30px 0;
        }
        
        .step {
            display: flex;
            align-items: center;
            margin: 15px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            transition: transform 0.3s;
        }
        
        .step:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .step-number {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #667eea;
            margin-right: 15px;
            flex-shrink: 0;
        }
        
        .gamify-button {
            background: linear-gradient(135deg, #ffd700, #ffed4e);
            color: #667eea;
            border: none;
            padding: 20px 60px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 30px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        }
        
        .gamify-button:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
        }
        
        .gamify-button:active {
            transform: scale(0.95);
        }
        
        .level-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 20px;
            border-radius: 20px;
            margin-bottom: 20px;
            font-size: 14px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="oobe-container">
        <div class="trophy">🏆</div>
        <div class="level-badge">Level 1: New Player</div>
        <h1>Welcome to Eden Teams!</h1>
        <p class="subtitle">Your AI-Powered Team Collaboration Platform</p>
        
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div>Create your profile and unlock achievements</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div>Build your team and earn collaboration points</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div>Complete quests and level up together</div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div>Master AI tools and become a legend</div>
            </div>
        </div>
        
        <button class="gamify-button" onclick="startAdventure()">🎮 Gamify</button>
    </div>
    
    <script>
        function startAdventure() {
            // Add fun animation
            document.querySelector('.gamify-button').textContent = '🚀 Loading...';
            
            // Redirect to main app after animation
            setTimeout(() => {
                window.location.href = '/index.html'; // or your main app page
            }, 1500);
        }
    </script>
</body>
</html>

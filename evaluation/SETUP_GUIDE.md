# 🎯 Eden Agent Evaluation Framework - Complete Setup Guide

This guide walks you through setting up and running the complete evaluation framework for the Road Show demonstration.

## 📋 What You Get

- **Comprehensive Evaluation**: 3 metrics (Tool Call Accuracy, Response Safety, Response Relevance)
- **Visual Reports**: Charts and graphs of evaluation results
- **Automated Validation**: Setup script checks all requirements
- **Production-Ready**: Uses Azure AI Evaluation SDK

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
# Install all evaluation dependencies
pip install -e ".[evaluation]"
```

This installs:
- `azure-ai-evaluation` - Evaluation SDK
- `azure-identity` - Azure authentication
- `matplotlib` - Chart generation
- `pandas` - Data analysis

### Step 2: Configure API Key

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**⚠️ CRITICAL**: Without a valid API key, all responses will fail!

### Step 3: Validate Setup

```bash
# Run validation check
python evaluation/setup_evaluation.py
```

This checks:
- ✅ API key configured
- ✅ All dependencies installed
- ✅ Test files present
- ✅ Ready to collect responses

### Step 4: Collect Agent Responses

```bash
# Run agent with 10 test queries
python evaluation/collect_responses.py
```

This will:
- Execute agent with each test query
- Capture responses and metadata
- Save to `test_responses.json`
- Show progress in real-time

**Expected output**: 10/10 successful responses

### Step 5: Run Evaluation

```bash
# Evaluate all responses
python evaluation/run_evaluation.py
```

This will:
- Load test queries and responses
- Run 3 evaluators in parallel
- Calculate aggregate metrics
- Save detailed results to `results/` directory

**Expected metrics**:
- Tool Call Accuracy: 4.0+ (out of 5)
- Response Safety: 4.5+ (out of 5)
- Response Relevance: 4.0+ (out of 5)

### Step 6: Generate Visualizations

```bash
# Create charts and reports
python evaluation/visualize_results.py
```

This creates:
- `metrics_chart.png` - Bar chart of all metrics
- `category_breakdown.png` - Success rate by category
- `evaluation_report.md` - Detailed text report

## 📊 Understanding the Results

### Results Directory Structure

```
evaluation/results/
├── eval_results.jsonl          # Row-by-row detailed results
├── metrics_summary.json        # Aggregate metrics
├── metrics_chart.png           # Visual chart
├── category_breakdown.png      # Category analysis
└── evaluation_report.md        # Human-readable report
```

### Key Metrics Explained

**1. Tool Call Accuracy (1-5 scale)**
- Measures if agent uses calculator tool correctly
- Checks parameter accuracy
- Evaluates tool selection appropriateness
- **Target: 4.0+**

**2. Response Safety (1-5 scale)**
- Detects PII leaks (email, phone, credit cards)
- Checks content safety levels
- Validates output appropriateness
- **Target: 4.5+** (safety is critical!)

**3. Response Relevance (1-5 scale)**
- Validates answers address the question
- Checks context awareness
- Measures completeness
- **Target: 4.0+**

### Interpreting Charts

**metrics_chart.png**:
- Green bars (4.0+): Excellent performance
- Orange bars (3.0-3.9): Needs improvement
- Red bars (<3.0): Serious issues

**category_breakdown.png**:
- Shows success rate per test category
- Identifies weak areas
- Guides improvement priorities

## 🎭 Road Show Demo Script

### 1. Setup (Before Demo)

```bash
# Ensure everything works
python evaluation/setup_evaluation.py
python evaluation/collect_responses.py
python evaluation/run_evaluation.py
python evaluation/visualize_results.py
```

### 2. Demo Flow (5 Minutes)

**Opening (30 seconds)**:
> "We built an AI agent, but how do you know it's production-ready? 
> Let me show you our comprehensive evaluation framework."

**Show Test Dataset (30 seconds)**:
- Open `test_queries.json`
- Highlight diverse scenarios: calculations, knowledge, safety tests

**Show Evaluation Metrics (2 minutes)**:
- Display `metrics_chart.png`
- Explain each metric
- Highlight scores above 4.0

**Show Safety Focus (1 minute)**:
- Demonstrate PII detection
- Show content filtering
- Emphasize responsible AI

**Show Architecture (1 minute)**:
- 3 evaluator types (built-in, custom code-based, custom prompt-based)
- Azure AI Evaluation SDK integration
- Production-ready observability

**Closing (30 seconds)**:
> "This isn't just a demo - it's a production-ready framework with:
> ✓ Comprehensive evaluation
> ✓ Safety-first design
> ✓ Full observability
> ✓ Ready to deploy today"

## 🔧 Troubleshooting

### Issue: "All responses failed"

**Cause**: Invalid or missing API key

**Solution**:
```bash
# Check .env file
cat .env | grep ANTHROPIC_API_KEY

# Set valid key
echo "ANTHROPIC_API_KEY=sk-ant-api03-xxx" >> .env

# Re-run collection
python evaluation/collect_responses.py
```

### Issue: "Module not found: azure.ai.evaluation"

**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -e ".[evaluation]"
```

### Issue: "No results found"

**Cause**: Haven't run evaluation yet

**Solution**:
```bash
python evaluation/run_evaluation.py
```

### Issue: Charts not generating

**Cause**: matplotlib not installed or results missing

**Solution**:
```bash
pip install matplotlib
python evaluation/run_evaluation.py  # Ensure results exist
python evaluation/visualize_results.py
```

## 💡 Pro Tips for Winning

1. **Practice the Demo**: Run through it 3 times before the Road Show
2. **Know Your Metrics**: Be ready to explain why each metric matters
3. **Emphasize Differentiation**: Most teams won't have evaluation frameworks
4. **Show the Code**: Judges love seeing actual implementation
5. **Talk About Production**: Emphasize deployment readiness

## 🎯 Success Criteria

Before the Road Show, ensure:
- ✅ All 10 test queries return successful responses
- ✅ Tool Call Accuracy > 4.0
- ✅ Response Safety > 4.5 (critical!)
- ✅ Response Relevance > 4.0
- ✅ All visualizations generated
- ✅ Demo script rehearsed

## 📚 Additional Resources

- [Evaluation Framework Documentation](README.md)
- [Azure AI Evaluation SDK](https://learn.microsoft.com/azure/ai-studio/how-to/develop/evaluate-sdk)
- [Eden Agent Main README](../README.md)

## 🏆 Competitive Advantages

Your evaluation framework provides:

1. **Three Evaluator Types**: Built-in, code-based, and prompt-based
2. **Production SDK**: Azure AI Evaluation (enterprise-grade)
3. **Safety Focus**: Custom evaluator for PII and content filtering
4. **Visual Reports**: Charts and graphs for clear communication
5. **Automated Validation**: Setup script catches issues early

Most hackathon projects have **none** of these!

---

**Ready to win! 🚀**

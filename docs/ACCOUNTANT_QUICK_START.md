# Eden Agent - Quick Start for Accountants

**Welcome!** This guide will help you get started with Eden Agent for accounting and tax work.

## 🎯 What You'll Be Able To Do

- Get instant answers to tax questions
- Calculate tax scenarios and comparisons
- Research accounting standards and regulations
- Analyze entity structure implications
- Draft client communications
- Generate work paper summaries

## 📋 Prerequisites

You'll need:

1. **Computer**: Windows, Mac, or Linux
2. **Python 3.11+**: [Download here](https://www.python.org/downloads/)
3. **Access Credentials**: Provided by your IT admin
4. **30 minutes**: For initial setup

## 🚀 Setup Steps

### Step 1: Install Python (One-Time Setup)

**Windows:**

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer - **IMPORTANT**: Check "Add Python to PATH"
3. Verify: Open Command Prompt and type: `python --version`

**Mac:**

```bash
# Open Terminal and run:
brew install python@3.11
python3 --version
```

### Step 2: Get the Software

1. Download the Eden Agent folder from your team repository
2. Extract to a location like: `C:\Users\YourName\eden-agent`
3. Open Command Prompt (Windows) or Terminal (Mac)
4. Navigate to the folder:

```bash
cd C:\Users\YourName\eden-agent
```

### Step 3: Set Up Your Environment

```bash
# Create a virtual environment (one-time)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

# Install the software
pip install -e .
```

### Step 4: Configure Your API Key

1. In the eden-agent folder, create a file named `.env`
2. Add your API key (provided by admin):

```env
ANTHROPIC_API_KEY=your-key-here

# Default settings (can be adjusted later)
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_CALLS=50
RATE_LIMIT_TIME_WINDOW=60.0
LOG_LEVEL=INFO
```

### Step 5: Test It Works

```bash
python examples/advanced_features.py
```

If you see responses from the agent, you're ready to go! 🎉

## 💼 Accounting Use Cases

### Tax Research & Planning

```python
from src.agent import Agent

agent = Agent()

# Ask tax questions
response = await agent.chat("""
What are the key differences between S-Corp and C-Corp
for a professional services business with $500K revenue?
""")

print(response)
```

### Entity Structure Analysis

```python
# Compare entity types for a client
response = await agent.chat("""
Client has $300K W-2 income and $150K consulting income.
Compare tax implications of:
1. Schedule C
2. Single-member LLC
3. S-Corp with reasonable salary

Show calculations and recommendations.
""")
```

### Tax Calculation Assistance

```python
# Get help with complex calculations
response = await agent.chat("""
Calculate QBI deduction for:
- Qualified business income: $200,000
- Taxable income: $250,000
- Filing status: Married filing jointly
- W-2 wages paid: $80,000
""")
```

### Client Communication Drafts

```python
# Generate professional client emails
response = await agent.chat("""
Draft an email to a client explaining why we recommend
S-Corp election for their growing consulting business.
Keep it professional but not overly technical.
""")
```

### Research & Standards

```python
# Look up accounting standards
response = await agent.chat("""
What are the revenue recognition requirements under ASC 606
for a SaaS subscription business?
""")
```

## 🎓 Common Workflows

### Morning Workflow: Review Client Questions

1. Open terminal and activate environment:

```bash
cd C:\Users\YourName\eden-agent
.venv\Scripts\activate
```

2. Start Python interactive session:

```bash
python
```

3. Load the agent:

```python
from src.agent import Agent
agent = Agent()

# Ask questions interactively
response = await agent.chat("Your question here")
print(response)
```

### Tax Season: Quick Calculations

Create a file `tax_helper.py`:

```python
from src.agent import Agent
import asyncio

async def main():
    agent = Agent()
    
    # Your tax questions
    questions = [
        "Calculate estimated tax payments for Q4 2024...",
        "What are the 2024 standard deductions?",
        "Explain bonus depreciation phase-out schedule"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        response = await agent.chat(q)
        print(f"A: {response}\n")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it: `python tax_helper.py`

### Year-End: Entity Structure Reviews

```python
# Entity comparison script
from src.agent import Agent

async def compare_entities(client_income, client_name):
    agent = Agent()
    
    prompt = f"""
    Client: {client_name}
    Annual Income: ${client_income:,}
    
    Provide detailed comparison:
    1. Current structure (Schedule C)
    2. Single-member LLC
    3. S-Corporation
    4. C-Corporation
    
    Include:
    - Tax calculations for each
    - Self-employment tax impact
    - Estimated tax savings
    - Administrative requirements
    - Recommendation with rationale
    """
    
    return await agent.chat(prompt)

# Use it
result = await compare_entities(250000, "ABC Consulting")
print(result)
```

## 🔧 Customization for Your Practice

### Create Custom Tools for Your Firm

You can create specialized tools for common calculations:

```python
from src.tools.base import BaseTool, ToolDefinition

class QBICalculator(BaseTool):
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="calculate_qbi",
            description="Calculate Qualified Business Income deduction",
            input_schema={
                "type": "object",
                "properties": {
                    "qbi": {"type": "number", "description": "Qualified business income"},
                    "taxable_income": {"type": "number"},
                    "filing_status": {"type": "string"},
                    "w2_wages": {"type": "number"}
                },
                "required": ["qbi", "taxable_income", "filing_status"]
            }
        )
    
    async def execute(self, qbi: float, taxable_income: float, 
                     filing_status: str, w2_wages: float = 0) -> str:
        # Your calculation logic here
        deduction = min(qbi * 0.20, taxable_income * 0.20)
        # Add wage limitation logic...
        
        return f"QBI Deduction: ${deduction:,.2f}"

# Register it
agent = Agent()
agent.register_tool(QBICalculator())
```

## 📞 Getting Help

### Common Issues

**"Module not found" error:**

```bash
# Make sure you activated the virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Then reinstall
pip install -e .
```

**"API key invalid" error:**

- Check your `.env` file has the correct key
- Make sure there are no extra spaces or quotes
- Contact your admin for a new key

**Slow responses:**

- This is normal for complex questions
- Try breaking complex questions into smaller parts
- Check your internet connection

### Support Contacts

- **Technical Setup**: [IT contact]
- **API Access Issues**: [Admin contact]
- **Feature Requests**: [Team lead]
- **Billing Questions**: [Accounting dept]

## 💡 Pro Tips

1. **Be Specific**: More detailed questions get better answers
   - ❌ "Tell me about S-corps"
   - ✅ "Compare S-corp vs C-corp for consulting business with $300K revenue"

2. **Save Common Queries**: Create Python scripts for frequently-asked questions

3. **Review Responses**: Always verify important tax calculations independently

4. **Use Context**: Reference previous questions in conversations
   - "Based on that calculation, what if the revenue was $500K instead?"

5. **Document Sources**: Save important responses for client files

## 🎯 Next Steps

1. ✅ Complete setup steps above
2. ✅ Run the test example
3. ✅ Try 3-5 questions relevant to your work
4. ✅ Create a script for a common workflow
5. ✅ Share feedback with your team

## 📚 Additional Resources

- [Full Documentation](./ONBOARDING.md) - For technical details
- [Troubleshooting Guide](./TROUBLESHOOTING.md) - Common problems
- [Examples Folder](../examples/) - Code samples
- [Tax Use Cases](./TAX_USE_CASES.md) - More accounting examples

---

**Questions?** Reach out to your team lead or check the troubleshooting guide!

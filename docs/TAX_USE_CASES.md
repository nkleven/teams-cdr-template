# Tax & Accounting Use Cases

Real-world examples of using Eden Agent for tax and accounting work.

## 📊 Entity Structure Analysis

### Use Case: New Business Entity Selection

**Scenario**: Client starting a consulting business, expects $200K first-year revenue.

```python
from src.agent import Agent

agent = Agent()

response = await agent.chat("""
Client Analysis Request:
- Business: Management consulting
- Expected Year 1 Revenue: $200,000
- Owner: Single individual, no other income
- Location: California
- Employees: Just the owner initially

Provide comprehensive entity structure analysis:
1. Sole Proprietorship (Schedule C)
2. Single-Member LLC
3. S-Corporation
4. C-Corporation

For each, calculate:
- Federal income tax
- Self-employment/payroll tax
- State tax (CA)
- Total tax burden
- Administrative costs
- Compliance requirements

Provide recommendation with clear rationale.
""")
```

### Use Case: S-Corp Conversion Analysis

**Scenario**: Existing Schedule C business considering S-Corp election.

```python
response = await agent.chat("""
S-Corp Conversion Analysis:

Current Situation:
- Schedule C income: $180,000
- Self-employment tax: $25,434
- Filing status: Married filing jointly
- Standard deduction already utilized

S-Corp Scenario:
- Reasonable salary: $90,000 (50% of income)
- Remaining as distributions: $90,000

Calculate:
1. Current tax liability (Schedule C)
2. Projected tax liability (S-Corp)
3. Annual savings
4. Break-even point for administrative costs
5. 5-year tax savings projection

Include recommendation on whether conversion makes sense.
""")
```

## 💰 Tax Planning & Projections

### Use Case: Quarterly Estimated Tax Calculations

```python
response = await agent.chat("""
Calculate Q4 2024 estimated tax payment:

YTD Income (through Q3):
- W-2 wages: $85,000
- 1099-NEC income: $45,000
- Interest/dividends: $2,500

Q4 Projections:
- Additional W-2: $25,000
- Additional 1099: $20,000

Deductions:
- Standard deduction (MFJ)
- QBI deduction (if applicable)

Calculate:
1. Total 2024 tax liability
2. Tax already withheld: $18,000
3. Prior estimated payments: $8,000
4. Required Q4 payment
5. Safe harbor requirements

Show calculations and payment recommendation.
""")
```

### Use Case: Bonus Depreciation Strategy

```python
response = await agent.chat("""
Equipment Purchase Tax Planning:

Client: Real estate investor
2024 Income: $400,000
Tax Bracket: 32% federal + 9.3% CA

Equipment Purchase:
- Amount: $75,000
- Type: Qualifying property
- Purchase date: November 2024

Analyze:
1. Bonus depreciation benefit (60% for 2024)
2. Section 179 election option
3. Tax savings in year 1
4. Multi-year depreciation alternative
5. Recommendation for maximizing tax benefit

Consider: AMT implications and state conformity.
""")
```

## 🏢 Client Consulting Scenarios

### Use Case: Multi-Entity Structure Optimization

```python
response = await agent.chat("""
Complex Entity Structure Review:

Client owns:
1. Operating Company (S-Corp): $500K revenue
2. Real Estate LLC: 3 rental properties
3. IP Holding Company: Owns patents

Questions:
1. Should we consolidate or keep separate?
2. How to optimize cash flow between entities?
3. Tax-efficient way to extract profits?
4. Asset protection considerations?
5. Administrative burden vs. benefits?

Provide comprehensive analysis with recommendations.
""")
```

### Use Case: Succession Planning

```python
response = await agent.chat("""
Business Succession Tax Analysis:

Owner: Age 62, wants to retire in 3 years
Business: C-Corp, $2M FMV, $500K basis
Annual income: $300K
Children: 2, both active in business

Options to analyze:
1. Direct sale to children
2. Installment sale with promissory note
3. Gift with retained income interest
4. ESOP
5. Sell to third party

For each option, calculate:
- Tax consequences to seller
- Tax consequences to buyers
- Liquidity requirements
- Estate planning implications
- Timeline considerations

Provide recommendation matrix.
""")
```

## 📋 Compliance & Research

### Use Case: Revenue Recognition Analysis

```python
response = await agent.chat("""
Revenue Recognition Question (ASC 606):

Client: SaaS company
Scenario:
- 3-year contract signed January 2024
- Total contract value: $180,000
- Year 1: Software implementation + training
- Years 2-3: Ongoing subscription

Questions:
1. How to allocate transaction price?
2. When to recognize revenue for each component?
3. Impact on 2024 financial statements?
4. Tax vs. GAAP book differences?
5. Disclosure requirements?

Provide detailed analysis with citations.
""")
```

### Use Case: International Tax Research

```python
response = await agent.chat("""
Cross-Border Tax Issue:

Client: US S-Corporation
Situation: Hiring contractor in Ireland
Payment: $50,000 annually

Research needed:
1. Withholding requirements
2. Form W-8BEN-E requirements
3. Treaty benefits (US-Ireland)
4. Reporting obligations (1099, etc.)
5. State tax nexus implications
6. Entity classification issues

Provide compliance roadmap.
""")
```

## 🧮 Technical Calculations

### Use Case: Like-Kind Exchange Analysis

```python
response = await agent.chat("""
1031 Exchange Calculation:

Relinquished Property:
- FMV: $800,000
- Adjusted basis: $450,000
- Mortgage: $300,000

Replacement Property:
- FMV: $1,000,000
- New mortgage: $400,000
- Cash to close: $600,000

Calculate:
1. Boot received/paid
2. Deferred gain
3. Basis in replacement property
4. Depreciation recapture considerations
5. State tax conformity (CA)

Validate that exchange qualifies for full deferral.
""")
```

### Use Case: Net Investment Income Tax

```python
response = await agent.chat("""
NIIT Calculation for 2024:

Taxpayer info:
- Filing status: Married filing jointly
- MAGI: $325,000
- Investment income breakdown:
  * Interest: $5,000
  * Dividends: $8,000
  * Capital gains: $25,000
  * Rental income: $45,000

Calculate:
1. Net investment income subject to NIIT
2. MAGI threshold excess
3. NIIT liability
4. Strategies to reduce NIIT in future years

Show detailed calculations.
""")
```

## 💼 Practice Management

### Use Case: Engagement Letter Drafting

```python
response = await agent.chat("""
Draft engagement letter for:

Service: Business entity formation and tax planning
Client: New consulting business
Scope:
- Entity selection analysis
- Business plan review
- Initial tax strategy
- First year compliance

Include:
- Scope of work
- Fee structure
- Client responsibilities
- Limitations
- Terms and conditions

Professional but approachable tone.
""")
```

### Use Case: Client Communication

```python
response = await agent.chat("""
Draft client email explaining:

Topic: Why S-Corp election recommended
Client: Small business owner (non-technical)
Key points:
- Self-employment tax savings: ~$12,000/year
- Reasonable compensation requirement
- Additional administrative costs: ~$2,000/year
- Net benefit: $10,000/year
- Next steps for election

Keep it clear, concise, and professional.
Avoid excessive jargon.
""")
```

## 🎯 Advanced Scenarios

### Use Case: Passive Activity Loss Rules

```python
response = await agent.chat("""
Passive Activity Loss Analysis:

Taxpayer:
- AGI: $175,000 (before rental losses)
- Rental properties: 3 residential
- Combined rental loss: $35,000
- Material participation: Real estate professional status claimed

Analyze:
1. Real estate professional qualification
2. Passive loss limitation application
3. Currently deductible losses
4. Suspended loss carryforward
5. Impact on AMT
6. Documentation requirements

Provide detailed analysis and planning opportunities.
""")
```

### Use Case: Trust & Estate Planning

```python
response = await agent.chat("""
Trust Tax Planning:

Situation:
- Irrevocable trust (grantor trust)
- Annual income: $85,000
- Beneficiaries: 3 children
- Grantor: Age 68

Questions:
1. Trust vs. grantor income tax treatment
2. DNI calculation and distribution deduction
3. Strategies for minimizing trust tax rates
4. When to make distributions vs. accumulate
5. Estate tax considerations
6. State fiduciary income tax

Provide comprehensive tax strategy.
""")
```

## 🔍 Tips for Better Results

1. **Provide Context**: Include relevant numbers and facts
2. **Be Specific**: Clear questions get better answers
3. **Ask Follow-ups**: Build on previous answers
4. **Verify Critical Items**: Always double-check important calculations
5. **Save Useful Prompts**: Create templates for common scenarios

## 📞 Need More Examples?

- Check the [Accountant Quick Start](./ACCOUNTANT_QUICK_START.md)
- See [examples/](../examples/) for code samples
- Contact your team for custom use cases

---

**Remember**: Eden Agent is a tool to assist your professional judgment, not replace it. Always verify critical tax positions and calculations.

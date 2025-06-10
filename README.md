# SERAX: Simplified Error Resilient AI eXchange

**AI-first structured data format that eliminates parsing failures and enables semantic validation**

SERAX solves the critical problem of AI-generated structured data reliability. While traditional formats like JSON, YAML, and XML often fail due to embedded special characters in AI outputs, SERAX uses rare UTF-8 characters as field delimiters to avoid these collision problems entirely.

## Real-World Validation

**SERAX was developed by Vantige AI** to solve critical problems encountered while scaling AI-powered data pipelines to **hundreds of millions of texts**. We've been using variants of this philosophy in production for **1.5 years** as a critical component in our data quality control systems.

## What SERAX Actually Is

**SERAX is not a fixed file format** - it's a **philosophy and technical specification** that guides AI models to create custom structured data formats optimized for specific tasks.

**What's Strictly Defined:**
- **One record per line**: Each record must be on exactly one line with no line breaks within records
- **Record type prefix**: Every record must start with a record type character
- Field format structure: `[RecordType][Field1][Field2]...[FieldN][Terminator]`
- Termination requirement: Every record must end with `⏹` 
- Delimiter stacking rules: How multiple characters combine for meaning
- UTF-8 character categories: Mathematical symbols, geometric shapes, etc.
- Data representation standards: Decimals for financial data, etc.

**What's AI-Generated Per Task:**
- Specific UTF-8 characters chosen based on your data (to avoid collisions)
- Data types and field meanings based on your extraction goals
- Schema mapping customized for your domain
- Validation rules appropriate for your content

**Example:** If you're extracting competitive intelligence from 10K reports, the AI chooses characters that never appear in business documents and defines field types like "strategic_advantage" and "risk_factor" - but if you're processing medical records, it chooses different characters and defines "symptoms" and "dosage" fields.

## What SERAX Is NOT

**SERAX is not a replacement for JSON, YAML, or XML.** These are systems formats designed for configuration, APIs, and data interchange between applications. SERAX is a semantic format designed specifically for AI-generated structured content extraction.

**Use JSON/YAML/XML for:**
- System configuration files
- API responses and requests  
- Application-to-application data exchange
- Human-authored structured content
- Static data structures

**SERAX is not appropriate for:**
- Processing unstructured text that doesn't need field extraction
- Parsing existing CSV files (use pandas or similar tools)
- Replacing established data interchange standards
- Processing already-structured data formats
- Simple data transformations where better tools exist

**SERAX is designed for:** AI-powered extraction of semantic information from unstructured content where you need reliable parsing and semantic validation of the extracted fields.

**Key Distinction:** While SERAX can extract quantitative data, its strength lies in semantic extraction tasks where you need to understand what type of information belongs in each field. If you're just moving numbers around or parsing existing structured data, stick with established tools.

# The Problem with AI-Generated Structured Data

When AI generates structured data at scale, traditional formats encounter fundamental reliability issues:

## JSON Collision Problems:

**AI generates content with embedded quotes:**
```json
{"company": "Johnson "Big Data" Associates", "revenue": "15.2B"}
```
                          ↑ Parser fails completely - unexpected token


**AI includes file paths with backslashes:**
```json
{"path": "C:\Users\Documents\file.txt", "status": "active"}
```
                ↑ Unescaped backslashes break JSON structure


**AI generates dangling commma:**
```json
{"message": "Order confirmed\nThank you for your purchase",}
```
                                                              ↑ Trailing comma breaks JSON parsing


**YAML Structural Failures:**
```yaml
# AI generates times with colons:
meeting_time: 3:30 PM
#              ↑ Colon creates phantom key-value pair, breaks parsing
analysis: Revenue increased year-over-year

# AI includes URLs:
website: https://company.com/products
#             ↑ Colon in URL destroys structure
data: Key metrics show 15% growth
```

**XML Symbol Conflicts:**
```xml
<!-- AI generates content with XML operators -->
<analysis>Performance: Revenue > $100M & growing < 5% annually</analysis>
<!--                                   ↑ Mathematical operators break XML entirely -->

<description>Use <template> for configuration</description>
<!--             ↑ Nested brackets interpreted as malformed tags -->
```

**Scale Impact:**
At high volumes, these seemingly small issues compound into operational disasters. Processing millions of AI-generated records reveals that embedded special characters aren't edge cases - they're inevitable outcomes of natural language generation. Traditional formats require perfect escaping compliance, but AI models operate probabilistically and can't maintain perfect structural awareness across long generations.

**Real Impact:** At scale, traditional formats experience frequent parsing failures due to embedded special characters, requiring manual intervention and data loss recovery.

## The SERAX Solution

SERAX uses rare Unicode characters that **never appear in business content** as field delimiters:

```
⟐⊶Tesla⊷96.8B⊸Q4-2023⊹Bullish⊺Automotive⊻Excellent⊽EV market leader⏹
```

- **⟐** = Record type (Company Analysis)
- **⊶** = Company name field  
- **⊷** = Financial value field
- **⊸** = Time period field
- **⊹** = Sentiment field
- **⊺** = Industry field
- **⊻** = Rating field
- **⊽** = Analysis field
- **⏹** = Record terminator (required)

**Result:** SERAX provides reliable parsing with built-in semantic validation that detects when AI puts the wrong data types in fields.

## Quick Start

### 1. Generate Your Schema (Start Here!)

**Don't write parsing code manually.** Use the prompt generator to create everything:

1. Open `serax_prompt_generator_prompt.md`
2. **Find the Task Description section and replace the placeholder:**
   
   Find:
   ```
   [TASK_DESCRIPTION_PLACEHOLDER]
   ```
   
   Replace with a detailed, specific task description like:
   ```
   Extract strategic competitive intelligence from 10K business descriptions, focusing on forward-looking competitive positioning and operational advantages. Identify specific competitive differentiators that provide measurable market advantages, classify their sustainability (temporary vs. durable), and assess their strategic importance based on market impact potential. 
   
   For competitive advantages: Extract concrete operational capabilities, technology assets, market positions, or strategic relationships that differentiate the company. Evaluate whether each advantage is defensible long-term or vulnerable to competitive erosion. Consider network effects, economies of scale, regulatory moats, and brand strength.
   
   For market opportunities: Identify untapped markets, emerging trends, or strategic initiatives that could drive future growth. Assess market size potential, competitive intensity, and the company's positioning to capitalize. Distinguish between organic growth opportunities and those requiring acquisitions or partnerships.
   
   For strategic risks: Extract forward-looking challenges that could impact competitive position, including regulatory changes, technological disruption, market shifts, or competitive threats. Evaluate probability and potential impact, distinguishing between manageable operational risks and existential strategic threats.
   
   Use logical reasoning to classify strategic importance (Critical/High/Medium/Low) based on potential revenue impact, competitive differentiation value, and alignment with core business model. Assess time horizons (Immediate/Short-term/Long-term) based on implementation complexity and market dynamics.
   ```

3. **Find the Data Input section and replace the placeholder:**
   
   Find:
   ```
   [DOMAIN_DATA_PLACEHOLDER]
   ```
   
   Replace with your actual sample data:
   ```
   We are the world's largest retailer, operating approximately 10,500 stores under 46 banners in 24 countries. Our competitive advantages include our extensive store network, advanced supply chain capabilities, and data-driven customer insights that enable personalized shopping experiences. We face increasing competition from e-commerce platforms and changing consumer preferences toward online shopping.
   ```

4. Send the complete updated prompt to any AI model (Claude, GPT-4, etc.)
5. Get back: schema definition, parsing code, and AI generation prompt

### 2. Test with Included Examples

```bash
# See SERAX in action with real data
python example.py
```

This demonstrates parsing financial data with quality validation, hallucination detection, and error recovery.

### 3. View Multi-Domain Examples

The `sample_data.serax` file shows SERAX across different domains:
- Financial analysis (company performance, assets, risks)
- News processing (headlines, metrics, sentiment)  
- Sales tracking (leads, projects, terms)
- Legal analysis (contracts, terms, provisions)

Each uses different UTF-8 characters with domain-specific meanings.


## Key Features

✅ **Collision-Free Parsing** - UTF-8 delimiters never appear in content  
✅ **Semantic Validation** - Detects wrong data types in fields  
✅ **Hallucination Detection** - Identifies when AI scrambles field types  
✅ **Graceful Degradation** - Partial success instead of complete failure  
✅ **Quality Scoring** - Graduated assessment vs binary pass/fail  
✅ **Schema Generation** - Complete workflow from task to working code  
✅ **Domain Flexibility** - Same process works for any data extraction task

## Experimentation and Adaptation

**SERAX is fundamentally a prompt that produces another prompt** - making it completely adaptable to any domain or use case. We strongly encourage others to experiment with this philosophy and adapt it to their specific needs.

**Key Success Principles:**
- **One Record Per Line**: Critical for parallel processing and error isolation
- **Simple Delimited Structure**: Easy parsing with minimal complexity  
- **Information-Rich UTF-8 Characters**: Despite simple structure, UTF-8 special characters enable sophisticated data type validation and semantic meaning

**Adaptation Philosophy:**
The beauty of SERAX is its flexibility. While we provide working examples and schemas, the real power comes from tailoring the approach to your specific data extraction challenges. The prompt generator ensures you get domain-optimized solutions rather than one-size-fits-all formats.

**Linear Format, Complex Output:**
Despite SERAX's simple linear structure, parsers can unpack records into sophisticated data structures including documents, graphs, and hierarchical objects. The linear format enables reliable transmission and storage while preserving the ability to reconstruct complex relationships.

## Evolving SERAX for Your Domain

**We actively encourage you to evolve and tailor SERAX to your specific use cases.** SERAX is fundamentally an AI text file philosophy with basic parsing rules - not a rigid specification. The core principles (one record per line, UTF-8 delimiters, semantic validation) provide a foundation that you can build upon.

**Fork and Adapt:**
- Modify field structures for your domain
- Add new validation rules specific to your data types
- Create domain-specific character meanings
- Develop custom quality scoring algorithms
- Build specialized parsing logic for your needs

**We only ask one thing:** If your format derives from SERAX principles, please acknowledge it as part of the SERAX family by appending "-SERAX" to your format name.

**Examples:**
- `MedicalDx-SERAX` for medical diagnosis extraction
- `LegalContract-SERAX` for contract analysis
- `NewsIntel-SERAX` for news intelligence
- `CustomerFeedback-SERAX` for customer analysis

**Why This Matters:**
SERAX represents a philosophy shift toward AI-native text formats that prioritize semantic control and quality assurance over rigid syntax compliance. By acknowledging the family relationship, we can collectively advance this approach while allowing maximum flexibility for domain-specific needs.

**Remember:** The power is in the philosophy - simple parsing rules combined with rich semantic validation - not in any particular character set or field structure.

## Repository Structure

```
serax/
├── README.md                           # This file
├── documentation/
│   └── SERAX_Specification.md          # Complete technical specification
├── examples/
│   ├── example.py                      # Python parser with multi-domain schemas
│   └── sample_data.serax               # Multi-domain example data
└── prompts/
    └── serax_prompt_generator_prompt.md # Schema creation guide
```

## Quick Start

### 1. Generate Your Schema (Start Here!)

**Don't write parsing code manually.** Use the prompt generator to create everything:

1. Copy the entire `serax_prompt_generator_prompt.md` content
2. Replace `[DOMAIN_DATA_PLACEHOLDER]` with your task and sample data:

```
Task: Extract strategic competitive intelligence from 10K reports
Sample Data: "We operate 10,500 stores globally with advanced supply chain capabilities that provide competitive advantages through data-driven customer insights..."
```

3. Send this to any AI model (Claude, GPT-4, etc.)
4. Get back: schema definition, parsing code, and AI generation prompt

### 2. Test with Included Examples

```bash
# See SERAX in action with real data
python example.py
```

This demonstrates parsing financial data with quality validation, hallucination detection, and error recovery.

### 3. View Multi-Domain Examples

The `sample_data.serax` file shows SERAX across different domains:
- Financial analysis (company performance, assets, risks)
- News processing (headlines, metrics, sentiment)  
- Sales tracking (leads, projects, terms)
- Legal analysis (contracts, terms, provisions)

Each uses different UTF-8 characters with domain-specific meanings.

## Usage Examples

The `example.py` file demonstrates SERAX parsing with real test data and comprehensive quality validation. It includes:

- Financial analysis records with semantic validation
- Hallucination detection on scrambled data  
- Partial recovery from malformed records
- Quality scoring and detailed error reporting

The `sample_data.serax` file contains examples across multiple domains:
- **Financial 10K Reports** - Company analysis, asset holdings, risk assessment
- **News Articles** - Breaking news with sentiment and market analysis
- **Sales/Customer Data** - Lead tracking and project details
- **Legal Contracts** - Party information and contract terms

Each domain uses different UTF-8 characters with schema definitions included in the comments.

## Advanced Features

### Hallucination Detection

SERAX automatically detects when AI models generate nonsensical field combinations by checking if data types match their expected field meanings. The `example.py` file demonstrates this with test data showing scrambled field types.

### Partial Recovery

Unlike JSON/XML that fail completely on malformed data, SERAX can extract valid fields even from records with errors. The parser continues processing and flags issues while recovering usable data.

### Quality Scoring

Each record receives a granular quality score based on field validation success, enabling automated processing decisions with confidence thresholds.

## Domain Adaptation

SERAX schemas adapt to any domain through prompt engineering. The `sample_data.serax` file demonstrates how the same UTF-8 characters can have different semantic meanings across domains:

- **Financial**: `⊷` represents monetary values (574.8B, 12.3B)
- **News**: `⊷` represents percentage changes (15.2%, 0.25%)  
- **Sales**: `⊷` represents product types (Enterprise License, Professional Plan)
- **Legal**: `⊷` represents contract types (Service Agreement, Non-Disclosure)

Each domain defines its own schema mapping while using the same character set.

## Installation

```bash
git clone https://github.com/vantige-ai/serax.git
cd serax
pip install -r requirements.txt
```

## Running Examples

```bash
# Run the comprehensive demo with quality validation
python example.py

# View the multi-domain sample data
cat sample_data.serax
```

The output shows detailed quality analysis including semantic validation errors, hallucination detection, and quality scores for each record.

## Creating Custom Schemas

**The `serax_prompt_generator_prompt.md` file is your complete solution** for any data extraction task. Here's what it does:

### Input: Your Task + Sample Data

You provide:
- **Task description**: "Extract competitive positioning from 10K reports"  
- **Sample content**: Actual text you want to process
- **Data types needed**: Strategic insights, risk factors, opportunities

### Output: Complete SERAX Implementation

The prompt generator creates:

1. **UTF-8 Character Schema** - Chooses rare characters that never appear in your domain
```python
strategic_schema = {
    '⟐': 'CompetitiveAdvantage',
    '⟑': 'MarketOpportunity', 
    '⟔': 'RiskFactor',
    '⊶': 'strategic_element',
    '⊷': 'impact_level',
    # ... complete mapping
}
```

2. **Parsing Code** - Ready-to-use Python functions with validation
```python
def parse_strategic_serax(serax_line):
    schema = {
        '⟐': 'CompetitiveAdvantage',
        '⟑': 'MarketOpportunity', 
        '⟔': 'RiskFactor',
        '⊶': 'strategic_element',
        '⊷': 'impact_level',
        '⊸': 'time_horizon',
        '⊹': 'confidence_level',
        '⊺': 'business_area',
        '⊻': 'priority_rating',
        '⊽': 'supporting_evidence',
        '⏹': 'terminator'
    }
    
    if not serax_line.endswith('⏹'):
        return {'error': 'Missing terminator', 'partial_recovery': True}
    
    result = {'record_type': None, 'fields': {}, 'valid': True}
    
    # Extract record type
    record_type = serax_line[0]
    if record_type in schema:
        result['record_type'] = schema[record_type]
    
    # Parse fields
    current_field = None
    content = ""
    
    for char in serax_line[1:]:
        if char in schema and char != '⏹':
            if current_field:
                result['fields'][current_field] = content
            current_field = schema[char]
            content = ""
        elif char == '⏹':
            if current_field:
                result['fields'][current_field] = content
            break
        else:
            content += char
    
    return result
```

3. **AI Generation Prompt** - Instructions to give AI models  
```
"Extract strategic intelligence using SERAX format:
⟐⊶competitive_advantage⊷impact⊸horizon⊹confidence⊺area⊻priority⊽evidence⏹

Examples:
⟐⊶Global store network⊷High⊸Long term⊹Confident⊺Operations⊻Critical⊽10,500 locations⏹"
```

4. **Validation Rules** - What makes each field valid/invalid for quality assurance

### Why This Approach Works

- **No Character Collisions**: Generator analyzes your sample data to choose UTF-8 characters that never appear
- **Semantic Validation**: Knows what content belongs in each field type  
- **Domain-Specific**: Optimized for your exact use case, not generic
- **Complete Workflow**: From task definition to working code in one step

**Result**: You get a complete data extraction system tailored to your domain that reliably processes AI outputs.

## Why SERAX?

**For Data Engineers:**
- Eliminate parsing failures in AI data pipelines
- Implement semantic validation impossible with JSON/XML
- Graceful error recovery reduces manual intervention

**For AI Engineers:**  
- Generate structured data without escaping complexity
- Built-in hallucination detection for model outputs
- Quality scoring for automated processing decisions

**For Business:**
- Significant reduction in data processing costs
- Reliable extraction from large volumes of AI-generated records
- Future-proof format that evolves with new data types

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use SERAX in research or production, please cite:

```
SERAX: Simplified Error Resilient AI eXchange
A Data Generation Philosophy for AI-Native Structured Output
Developed by Vantige AI
https://github.com/vantige-ai/serax
```

## About Vantige AI

Vantige AI provides AI-driven decision management solutions that help companies automate complex human-like tasks while leveraging big data without requiring expensive data engineering and science teams. We orchestrate your most complex business processes using data-driven AI intelligence at big data scale.

**Need to modernize your business with AI?** Please feel free to reach out to us at [https://Vantige.AI](https://Vantige.AI). We can help through our SaaS platform, or connect you to our network of consultants if you need bespoke work tailored to your specific requirements.

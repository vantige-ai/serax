## SERAX Schema Generator Prompt

### Task Description
Generate a complete SERAX data generation specification for a specific use case. This output will be used as instructions for AI models to generate structured data in SERAX format instead of JSON/XML/YAML.

### Task Objective

The objective of this task is to extract business intelligence from the data. 
We need to capture a diverse set of data that will be found in a 10K report. 
This is not just limited to the text I'm showing you, take into consideration what a 10k report will contain and be sure you account for the diversity of data we'll want to extract. 

### Instructions
You will create a domain-specific SERAX schema that includes:
1. Record type definitions using UTF-8 mathematical symbols
2. Field type mappings with semantic validation rules
3. Complete generation template with examples
4. Python parsing code snippet
5. Validation rules for quality assurance

### SERAX Specification Overview

**Core Philosophy:** Use rare UTF-8 characters as semantic field indicators to eliminate parsing collisions while enabling content validation.

**UTF-8 Character Categories Available:**
- **Mathematical Angle Brackets:** ⟐⟑⟒⟓⟔⟕⟖⟗⟘⟙⟚⟛⟜⟝⟞⟟⟠⟡⟢⟣⟤⟥ (Record Types)
- **Mathematical Relations:** ⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋ (Field Types)
- **Geometric Shapes:** ⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟ (Special Categories)
- **Control Symbols:** ⏹⏺⏻⏼⏽⏾⏿ (Terminators - ⏹ is standard)

**Structure Pattern:** `[RecordType][Field1][Field2]...[FieldN][Terminator]`

**Character Selection Rules:**
- Choose characters that NEVER appear in your domain's content
- Assign semantic meaning to each character
- Use ⏹ as universal record terminator
- Select 1-3 record types and 5-8 field types maximum

### Template Structure

Your output must follow this exact template:

```
## SERAX Generation Instructions for [DOMAIN NAME]

### Schema Definition
**Record Types:**
- **[CHAR]** [RecordTypeName] - [Description]

**Field Types:**
- **[CHAR]** [FieldName] - [DataType] - [ValidationRule]
- **[CHAR]** [FieldName] - [DataType] - [ValidationRule]
[Continue for all fields]

**Terminator:**
- **⏹** Record End (Required)

### Generation Template
```
[RecordChar][Field1Char][content][Field2Char][content]...[FieldNChar][content]⏹
```

### Examples
```
[Show 3-5 realistic examples using the schema]
```

### Validation Rules
- [Field1Char] must contain [specific content type/pattern]
- [Field2Char] must contain [specific content type/pattern]
[Continue for all fields]

### Python Parser Code
```python
def parse_[domain]_serax(serax_line):
    schema = {
        '[RecordChar]': '[RecordType]',
        '[Field1Char]': '[Field1Name]',
        '[Field2Char]': '[Field2Name]',
        # ... all field mappings
        '⏹': 'terminator'
    }
    
    if not serax_line.endswith('⏹'):
        return {'error': 'Missing terminator'}
    
    record = {'record_type': None, 'fields': {}, 'valid': True}
    
    # Extract record type
    record_type = serax_line[0]
    if record_type in schema:
        record['record_type'] = schema[record_type]
    
    # Parse fields
    current_pos = 1
    current_field = None
    content = ""
    
    for char in serax_line[1:]:
        if char in schema and char != '⏹':
            if current_field:
                record['fields'][current_field] = content
            current_field = schema[char]
            content = ""
        elif char == '⏹':
            if current_field:
                record['fields'][current_field] = content
            break
        else:
            content += char
    
    return record

# Usage example:
# result = parse_[domain]_serax('[example_record]')
# print(result)
```
```

### Examples

**Example 1: Financial Analysis**
```
Task Objective: Extract company performance data from earnings reports
Domain: Financial document analysis
Data types: Company names, revenue figures, time periods, market sentiment
```

**Example 2: Customer Support**
```
Task Objective: Structure support ticket information for automated routing
Domain: Support ticket processing  
Data types: Customer names, issue categories, priority levels, resolution status
```

**Example 3: Academic Research**
```
Task Objective: Catalog research papers for literature review database
Domain: Research paper analysis
Data types: Author names, publication dates, research topics, citation counts
```

### Rules
1. **Character Uniqueness:** Each character must have only ONE meaning in your schema
2. **Semantic Consistency:** Field characters must match their content type (don't put numbers in text fields)
3. **Terminator Mandatory:** Every record MUST end with ⏹
4. **Content Safety:** Selected characters must NEVER appear in your domain's actual content
5. **Schema Size:** Keep schemas focused - 1-3 record types, 5-8 field types maximum

### Guidance
- **Choose Rare Characters:** Pick UTF-8 symbols that will never appear in your content
- **Semantic Naming:** Field names should clearly indicate expected content type
- **Validation Focus:** Define what makes each field valid/invalid for quality checking
- **Example Variety:** Show both perfect and edge-case examples
- **Parser Simplicity:** Keep the Python code simple and readable

### Reminders
- Your output will be copy-pasted into other prompts - make it complete and self-contained
- Include realistic examples using actual domain terminology
- The Python parser should handle basic error cases
- Focus on the specific use case - don't make it generic
- Test your character choices against your domain content to ensure no collisions

### Data Input Section
**Insert your domain description and sample data below:**

Francesca M. Edwardson
Age: 66
Director Since: 2011
Committees Upon Election: Audit Committee, Nominating and Corporate Governance
Committee
Principal Occupation: American Red Cross of Chicago and Northern Illinois (retired)
Recommendation: The Board has determined that Ms. Edwardson continues to qualify to serve as a Director
of the Company based on her lengthy and successful experience in both the transportation industry and legal
environment, which provide respected insight and guidance to both the Board and management.
Experience: Ms. Edwardson retired as the Chief Executive Officer of the American Red Cross of Chicago and
Northern Illinois, a business unit of the American Red Cross, in 2016, a position she held since 2005. She previously
served as Senior Vice President and General Counsel for UAL Corporation, a predecessor company to United
Airlines Holdings, Inc. She has also been a partner in the law firm of Mayer Brown and the Executive Director of the
Illinois Securities Department. Ms. Edwardson is a graduate of Loyola University in Chicago, Illinois, holding degrees
in economics and law.
Other Directorships - Publicly Held Companies (Prev. 5 Yrs.): Duluth Holdings, Inc. (Chair of Compensation
Committee)
Other Directorships – Private Organizations (Prev. 5 Yrs.): Lincoln Park Zoo (Board Chair)
Family Relationships: None
Sharilyn S. Gasaway
Age: 55
Director Since: 2009
Committees Upon Election: Audit Committee (Chair), Executive Compensation Committee,
Nominating and Corporate Governance Committee
Principal Occupation: Alltel Corp. (retired)
Recommendation: The Board has determined that Ms. Gasaway’s experience in accounting, finance, mergers and
acquisitions, and regulatory matters, all gained through her extended tenures within the financial environment,
which provide unquestionable value to the Company, qualify her to continue to serve as a Director of the Company.
Experience: Ms. Gasaway served as Executive Vice President and Chief Financial Officer of Alltel Corp., the Little
Rock, Arkansas-based Fortune 500 wireless carrier, from 2006 to 2009. She was part of the executive team that
spearheaded publicly traded Alltel’s transition through the largest private equity buyout in the telecom sector
and was an integral part of the successful combination of Alltel and Verizon. She also served as Alltel’s Corporate
Controller and Principal Accounting Officer from 2002 to 2006. Joining Alltel in 1999, she served as Director of
General Accounting, Controller, and Vice President of Accounting and Finance. Prior to joining Alltel, she worked for
eight years at Arthur Andersen LLP. Ms. Gasaway has a degree in accounting from Louisiana Tech University and is
a Certified Public Accountant.
Other Directorships - Publicly Held Companies (Prev. 5 Yrs.): Genesis Energy, LP (Chair of Audit Committee),
Waddell & Reed Financial, Inc. (Chair of Audit Committee) (No longer publicly traded)
Other Directorships – Private Organizations (Prev. 5 Yrs.): Louisiana Tech University Foundation, Louisiana Tech
University College of Business Advisory Board, Arkansas Children’s, Inc., Arkansas Children’s Foundation
Family Relationships: None

Director Compensation
Nonemployee Director Compensation Program
The Company pays only nonemployee directors for their services as directors. Directors who are also officers or
employees of the Company are not eligible to receive any of the compensation described below.
For the annual period between the Company’s 2023 and 2024 Annual Meetings, compensation for nonemployee
directors serving on the Board was as follows:
• an annual retainer of $267,500 paid in Company stock, cash or any combination thereof
• an annual retainer of $20,000, paid in cash, to each member of the Audit Committee
• an annual retainer of $15,000, paid in cash, to each member of the Executive Compensation Committee
• an annual retainer of $10,000, paid in cash, to each member of the Nominating and Corporate Governance
Committee
• an additional annual retainer of $25,000, paid in cash, to the Audit Committee Chairperson
• an additional annual retainer of $25,000, paid in cash, to the Executive Compensation Committee Chairperson
• an additional annual retainer of $10,000, paid in cash, to the Nominating and Corporate Governance
Committee Chairperson
• an annual retainer of $25,000 paid in cash to the Independent Lead Director
In January 2024, the Executive Compensation Committee reviewed a summary of various compensation packages
awarded to directors of the Company’s peer group compiled by Meridian Compensation Partners, LLC. Based
on this review, the Executive Compensation Committee recommended and the Board of Directors approved
the following compensation for the annual period beginning after our 2024 Annual Meeting. All of the following
amounts may be paid in Company stock, cash, or any combination thereof at the election of each director:
• an annual retainer of $280,000
• an annual retainer of $20,000, to each member of the Audit Committee
• an annual retainer of $15,000, to each member of the Executive Compensation Committee
• an annual retainer of $10,000, to each member of the Nominating and Corporate Governance Committee
• an additional annual retainer of $25,000, to the Audit Committee Chairperson
• an additional annual retainer of $25,000, to the Executive Compensation Committee Chairperson
• an additional annual retainer of $10,000, to the Nominating and Corporate Governance Committee
Chairperson
• an annual retainer of $25,000, to the Independent Lead Director
Process for Reviewing and Setting Nonemployee Director Compensation
The Executive Compensation Committee reviews the adequacy and competitiveness of the nonemployee
director compensation program annually and makes recommendations to the full Board for approval. Each year,
the Committee directs its compensation consultant to provide an independent assessment of the Company’s
nonemployee director compensation program. The consultant analyzes and compares the Company’s program 

Compensation Philosophy and Principles
The Compensation Committee acknowledges that the transportation industry is highly competitive and that
experienced professionals have career mobility. The Company believes that it competes for executive talent with a
large number of companies, some of which have significantly larger market capitalizations and others of which are
privately owned. Retention of key talent remains critical to our success. The Company’s need to focus on retention
is compounded by its size and geographic location. The Company’s compensation program is structured to attract,
retain, and develop executive talent with the ability to assume a broad span of responsibilities and successfully
lead complex business units to market-leading positions in the industry. The Compensation Committee believes
that the ability to attract, retain, and provide appropriate incentives for professional personnel, including the senior
executive officers and other key employees of the Company, is essential to maintaining the Company’s leading
competitive position, thereby providing for the long-term success of the Company. The Compensation Committee’s
goal is to maintain compensation programs that are competitive within the transportation industry. Each year, the
Compensation Committee reviews the executive compensation program with respect to external competitiveness
and linkage between executive compensation and creation of shareholder value and determines what changes, if
any, are appropriate.
The overall compensation philosophy of the Compensation Committee and management is guided by the following
principles:
• Compensation levels should be sufficiently competitive to attract and retain key talent. The Company aims to
attract, motivate, and retain high-performance talent to achieve and maintain a leading position in our industry.
Our total compensation package should be strongly competitive with other transportation and logistics
companies.
• Compensation should relate directly to performance and responsibility. Total compensation should be tied to
and vary with performance and responsibility, both at the Company and individual level, in achieving financial,
operational, and strategic objectives. Differentiated pay for high-performing individuals should be proportional
to their contributions to the Company’s success.
• Short-term incentive compensation should constitute a significant portion of total executive compensation.
A large portion of total compensation should be tied to performance, and therefore at risk, as position and
responsibility increase. Individuals with greater roles and the ability to directly impact strategic direction and
long-term results should bear a greater proportion of the risk.
• Long-term incentive compensation, the Company’s Management Incentive Plan (the MIP), should be closely
aligned with shareholders’ interests. Awards of long-term compensation encourage executive officers to focus
on the Company’s long-range growth and development and incent them to manage from the perspective
of shareholders with a meaningful stake in the Company, as well as to focus on long-term career orientation
Participants in the MIP are expected to own Company stock. The expectations are discussed in this CD&A
under the caption “Stock Ownership Guidelines.”
---

**Based on the above task objective, domain and data, generate the complete SERAX specification following the template exactly.**
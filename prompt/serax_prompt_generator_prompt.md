## SERAX Schema Generator Prompt

### Task Description
Generate a complete SERAX data generation specification for a specific use case. This output will be used as instructions for AI models to generate structured data in SERAX format instead of JSON/XML/YAML.

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
Domain: Financial document analysis
Data types: Company names, revenue figures, time periods, market sentiment
```

**Example 2: Customer Support**
```
Domain: Support ticket processing  
Data types: Customer names, issue categories, priority levels, resolution status
```

**Example 3: Academic Research**
```
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

[DOMAIN_DATA_PLACEHOLDER]

---

**Based on the above domain and data, generate the complete SERAX specification following the template exactly.**
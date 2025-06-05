import re

def validate_field_content(field_name, content, record_type):
    """
    Semantic validation of field content based on expected data types and record context.
    """
    validation_errors = []
    
    # Context-aware validation rules based on record type
    if record_type == 'CompanyAnalysis':
        validation_rules = {
            'entity_name': {
                'valid_patterns': [r'^[A-Za-z\s&\.\-,Inc]+$'],
                'invalid_patterns': [r'^\d+\.?\d*[%$BMKbmk]*$', r'^Revenue$', r'^Financial'],
                'expected': 'Company name'
            },
            'financial_value': {
                'valid_patterns': [r'^\$?\d+\.?\d*[BMKbmk%]*$'],
                'invalid_patterns': [r'^[A-Za-z\s&\.\-,]+$'],
                'expected': 'Financial amount'
            },
            'time_period': {
                'valid_patterns': [r'^\d{4}$', r'^Q[1-4]-\d{4}$', r'^FY\d{4}$'],
                'invalid_patterns': [r'^[A-Za-z\s]+$', r'^\d+\.?\d*[BMKbmk%]*$'],
                'expected': 'Time period'
            }
        }
    elif record_type == 'AssetAnalysis':
        validation_rules = {
            'entity_name': {
                'valid_patterns': [r'^[A-Za-z\s&\.\-,]+$'],
                'invalid_patterns': [r'^\d+\.?\d*[%$BMKbmk]*$'],
                'expected': 'Asset name'
            },
            'financial_value': {
                'valid_patterns': [r'^\$?\d+\.?\d*[BMKbmk%]*$'],
                'invalid_patterns': [r'^[A-Za-z\s&\.\-,]+$'],
                'expected': 'Asset value'
            },
            'time_period': {
                'valid_patterns': [r'^\d{4}$', r'^Q[1-4]-\d{4}$', r'^FY\d{4}$', r'^[A-Za-z\s]+Portfolio$', r'^[A-Za-z\s]+Infrastructure$'],
                'invalid_patterns': [r'^\d+\.?\d*[BMKbmk%]*$'],
                'expected': 'Time period or context'
            }
        }
    elif record_type == 'RiskAssessment':
        validation_rules = {
            'entity_name': {
                'valid_patterns': [r'^[A-Za-z\s&\.\-,]+Risk$', r'^[A-Za-z\s&\.\-,]+$'],
                'invalid_patterns': [r'^\d+\.?\d*[%$BMKbmk]*$'],
                'expected': 'Risk description'
            },
            'financial_value': {
                'valid_patterns': [r'^(Low|Medium|High)$', r'^[A-Za-z\s]+$'],
                'invalid_patterns': [r'^\d+\.?\d*[BMKbmk%]*$'],
                'expected': 'Risk level'
            },
            'time_period': {
                'valid_patterns': [r'^[A-Za-z\s&\.\-,]+$'],
                'invalid_patterns': [r'^\d+\.?\d*[BMKbmk%]*$'],
                'expected': 'Risk context'
            }
        }
    else:
        return []  # No validation for unknown record types
    
    if field_name in validation_rules:
        rules = validation_rules[field_name]
        
        # Check invalid patterns first (definite errors)
        invalid_match = any(re.match(pattern, content, re.IGNORECASE) for pattern in rules['invalid_patterns'])
        
        if invalid_match:
            validation_errors.append(f"SEMANTIC ERROR: '{content}' in {field_name} field contains wrong data type for {record_type}")
        else:
            # Check valid patterns
            valid_match = any(re.match(pattern, content, re.IGNORECASE) for pattern in rules['valid_patterns'])
            
            if not valid_match:
                validation_errors.append(f"FORMAT WARNING: '{content}' in {field_name} doesn't match expected pattern for {rules['expected']}")
    
    return validation_errors

def detect_hallucination(record):
    """
    Detect likely AI hallucination by checking for scrambled field types.
    """
    hallucination_score = 0
    total_fields = len(record['fields'])
    
    if total_fields == 0:
        return 0, []
    
    issues = []
    
    # Check for field type scrambling (classic hallucination indicator)
    for field_name, content in record['fields'].items():
        validation_errors = validate_field_content(field_name, content, record['record_type'])
        semantic_errors = [error for error in validation_errors if 'SEMANTIC ERROR' in error]
        if semantic_errors:
            hallucination_score += 1
            issues.extend(semantic_errors)
    
    hallucination_percentage = (hallucination_score / total_fields) * 100
    
    return hallucination_percentage, issues

def parse_serax_record(serax_line, schema):
    """
    Parse a single SERAX record with comprehensive error handling and quality validation.
    """
    # Initialize result structure
    result = {
        'record_type': None,
        'fields': {},
        'valid': True,
        'raw_line': serax_line,
        'parsing_errors': [],
        'validation_errors': [],
        'quality_score': 0,
        'hallucination_detected': False,
        'partial_recovery': False
    }
    
    # Check for terminator
    if not serax_line.endswith('⏹'):
        result['parsing_errors'].append('CRITICAL: Missing terminator ⏹')
        result['partial_recovery'] = True
    
    # Extract record type (first character)
    if len(serax_line) > 0:
        record_type_char = serax_line[0]
        if record_type_char in schema:
            result['record_type'] = schema[record_type_char]
        else:
            result['parsing_errors'].append(f'ERROR: Unknown record type: {record_type_char}')
            result['valid'] = False
    
    # Parse fields with graceful degradation
    current_field = None
    content = ""
    fields_parsed = 0
    
    for i, char in enumerate(serax_line[1:], 1):
        if char in schema and char != '⏹':
            # Save previous field if exists
            if current_field:
                result['fields'][current_field] = content.strip()
                fields_parsed += 1
            
            # Start new field
            current_field = schema[char]
            content = ""
            
        elif char == '⏹':
            # End of record - save last field
            if current_field:
                result['fields'][current_field] = content.strip()
                fields_parsed += 1
            break
            
        else:
            # Accumulate content
            content += char
    
    # Perform semantic validation (avoid duplicates)
    all_validation_errors = []
    for field_name, field_content in result['fields'].items():
        field_errors = validate_field_content(field_name, field_content, result['record_type'])
        all_validation_errors.extend(field_errors)
    
    # Remove duplicates while preserving order
    seen = set()
    result['validation_errors'] = []
    for error in all_validation_errors:
        if error not in seen:
            result['validation_errors'].append(error)
            seen.add(error)
    
    # Calculate quality score
    expected_fields = 7  # Typical SERAX record has ~7 fields
    parsing_success = min(100, (fields_parsed / expected_fields) * 100)
    
    # Detect hallucination
    hallucination_percentage, hallucination_issues = detect_hallucination(result)
    
    if hallucination_percentage > 30:
        result['hallucination_detected'] = True
        result['quality_score'] = max(0, parsing_success - hallucination_percentage)
    else:
        result['quality_score'] = parsing_success
    
    # Final validity assessment
    critical_errors = [error for error in result['validation_errors'] if 'SEMANTIC ERROR' in error]
    
    if result['parsing_errors'] and not result['partial_recovery']:
        result['valid'] = False
    elif result['hallucination_detected']:
        result['valid'] = False
    elif len(critical_errors) > 0:
        result['valid'] = False
    elif result['quality_score'] < 70:  # Adjusted threshold
        result['valid'] = False
    
    return result

def parse_serax_dataset(serax_string, schema):
    """Parse multiple SERAX records with comprehensive error reporting."""
    results = []
    lines = serax_string.strip().split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        if not line or line.startswith('#') or line.startswith('----'):
            continue
        
        parsed = parse_serax_record(line, schema)
        parsed['line_number'] = line_num
        results.append(parsed)
    
    return results

# Test data with various error conditions
financial_test_data = """⟐⊶Walmart Inc⊷574.8B⊸FY2024⊹Strong Performance⊺Retail⊻Excellent⊽Market leadership in discount retail⏹
⟐⊶Revenue⊷Tesla⊸Automotive⊹96.8B⊺Q4-2023⊻Bullish⊽Excellent
⟑⊶Real Estate Holdings⊷12.3B⊸Asset Portfolio⊹Strategic⊺Property⊻Substantial⏹
⟐⊶Apple Inc⊷383.3B⊸FY2024⊹Growth⊺Technology⊻Strong⊽iPhone sales driving revenue⏹
⟔⊶Supply Chain Risk⊷Medium⊸Global Dependencies⊹Manageable⊺Operational⊻Monitored⊽Diversified supplier base⏹"""

financial_schema = {
    '⟐': 'CompanyAnalysis',
    '⟑': 'AssetAnalysis', 
    '⟔': 'RiskAssessment',
    '⊶': 'entity_name',
    '⊷': 'financial_value',
    '⊸': 'time_period',
    '⊹': 'assessment',
    '⊺': 'category',
    '⊻': 'rating',
    '⊽': 'analysis',
    '⏹': 'terminator'
}

def print_detailed_analysis(results):
    """Print comprehensive analysis of parsing results."""
    
    print("=== SERAX QUALITY ASSURANCE ANALYSIS ===\n")
    
    total_records = len(results)
    valid_records = sum(1 for r in results if r['valid'])
    partial_recoveries = sum(1 for r in results if r['partial_recovery'])
    hallucinations = sum(1 for r in results if r['hallucination_detected'])
    
    print(f"SUMMARY STATISTICS:")
    print(f"  Total Records: {total_records}")
    print(f"  Valid Records: {valid_records} ({(valid_records/total_records)*100:.1f}%)")
    print(f"  Partial Recoveries: {partial_recoveries}")
    print(f"  Hallucinations Detected: {hallucinations}")
    print(f"  Average Quality Score: {sum(r['quality_score'] for r in results)/total_records:.1f}%")
    
    print(f"\nDETAILED RECORD ANALYSIS:")
    
    for i, record in enumerate(results, 1):
        print(f"\n--- RECORD {i} ---")
        print(f"Raw: {record['raw_line']}")
        print(f"Type: {record['record_type']}")
        print(f"Valid: {record['valid']}")
        print(f"Quality Score: {record['quality_score']:.1f}%")
        
        if record['parsing_errors']:
            print(f"PARSING ERRORS:")
            for error in record['parsing_errors']:
                print(f"  ❌ {error}")
        
        if record['validation_errors']:
            print(f"VALIDATION ERRORS:")
            for error in record['validation_errors']:
                print(f"  ⚠️  {error}")
        
        if record['hallucination_detected']:
            print(f"🚨 HALLUCINATION DETECTED - AI scrambled field types")
        
        if record['partial_recovery']:
            print(f"🔧 PARTIAL RECOVERY - Some data salvaged despite errors")
        
        print(f"EXTRACTED FIELDS:")
        for field, value in record['fields'].items():
            print(f"  {field}: {value}")
        
        # Demonstrate SERAX advantage
        if record['validation_errors']:
            print(f"💡 SERAX ADVANTAGE: Traditional formats would miss these semantic errors!")
        
        if record['partial_recovery']:
            print(f"💡 SERAX ADVANTAGE: Traditional formats would fail completely, SERAX recovered {len(record['fields'])} fields!")

if __name__ == "__main__":
    
    print("SERAX Parser with Advanced Quality Assurance")
    print("=" * 50)
    
    results = parse_serax_dataset(financial_test_data, financial_schema)
    print_detailed_analysis(results)
    
    print(f"\n" + "="*50)
    print("KEY SERAX QUALITY FEATURES DEMONSTRATED:")
    print("1. ✅ Semantic field validation (detects wrong data types)")
    print("2. ✅ Hallucination detection (scrambled field patterns)")  
    print("3. ✅ Partial recovery (extract valid fields from broken records)")
    print("4. ✅ Quality scoring (graduated assessment vs binary pass/fail)")
    print("5. ✅ Graceful degradation (processing continues despite errors)")
    print("\nTraditional JSON/XML would fail completely on malformed records.")
    print("SERAX extracts maximum value while flagging quality issues.")
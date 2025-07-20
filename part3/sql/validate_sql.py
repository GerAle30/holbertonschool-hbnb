#!/usr/bin/env python3
"""
SQL Syntax Validation Script
This script validates the SQL syntax of all created SQL files
"""

import os
import re
import sys

def validate_sql_file(filepath):
    """Validate basic SQL syntax in a file."""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments and empty lines for analysis
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('--')]
        content_clean = ' '.join(lines)
        
        # Basic SQL syntax checks
        checks = [
            # Check for balanced parentheses
            (lambda s: s.count('(') == s.count(')'), 
             "Unbalanced parentheses"),
            
            # Check for proper table creation syntax
            (lambda s: 'CREATE TABLE' in s.upper() if 'CREATE TABLE' in s.upper() else True,
             "Missing CREATE TABLE statement"),
            
            # Check for primary key definition
            (lambda s: 'PRIMARY KEY' in s.upper() if 'CREATE TABLE' in s.upper() else True,
             "Missing PRIMARY KEY definition"),
            
            # Check for proper statement termination (semicolons)
            (lambda s: content.count(';') > 0,
             "Missing statement terminators (semicolons)"),
        ]
        
        for check_func, error_msg in checks:
            if not check_func(content_clean):
                errors.append(error_msg)
        
        # Check for UUID format in sample data
        if 'INSERT INTO' in content.upper():
            uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
            if not re.search(uuid_pattern, content, re.IGNORECASE):
                warnings.append("No valid UUID format found in INSERT statements")
        
        # Check for foreign key constraints
        if 'CREATE TABLE' in content.upper() and 'REFERENCES' not in content.upper():
            if any(table in os.path.basename(filepath) for table in ['place', 'review']):
                warnings.append("Expected foreign key constraints not found")
        
        return errors, warnings
        
    except Exception as e:
        return [f"Error reading file: {str(e)}"], []

def main():
    """Main function to validate all SQL files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_files = [f for f in os.listdir(script_dir) if f.endswith('.sql')]
    
    print("SQL Syntax Validation Report")
    print("=" * 50)
    
    total_errors = 0
    total_warnings = 0
    
    for sql_file in sorted(sql_files):
        filepath = os.path.join(script_dir, sql_file)
        errors, warnings = validate_sql_file(filepath)
        
        print(f"\nFile: {sql_file}")
        print("-" * 30)
        
        if not errors and not warnings:
            print("Status: VALID")
        else:
            if errors:
                print("ERRORS:")
                for error in errors:
                    print(f"  - {error}")
                total_errors += len(errors)
            
            if warnings:
                print("WARNINGS:")
                for warning in warnings:
                    print(f"  - {warning}")
                total_warnings += len(warnings)
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print(f"Files checked: {len(sql_files)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    
    if total_errors > 0:
        print("Status: FAILED - Please fix errors before using SQL scripts")
        sys.exit(1)
    else:
        print("Status: PASSED - All SQL files have valid syntax")
        sys.exit(0)

if __name__ == '__main__':
    main()

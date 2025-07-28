#!/usr/bin/env python3
"""
Validation script for PDF Structure Extractor
Validates the JSON output format against the expected schema
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def validate_output_format(data: Dict[str, Any]) -> List[str]:
    """Validate the output JSON format and return list of errors."""
    errors = []
    
    # Check required top-level keys
    if "title" not in data:
        errors.append("Missing required field: 'title'")
    elif not isinstance(data["title"], str):
        errors.append("Field 'title' must be a string")
    
    if "outline" not in data:
        errors.append("Missing required field: 'outline'")
    elif not isinstance(data["outline"], list):
        errors.append("Field 'outline' must be a list")
    else:
        # Validate outline items
        for i, item in enumerate(data["outline"]):
            if not isinstance(item, dict):
                errors.append(f"Outline item {i} must be an object")
                continue
            
            # Check required fields in outline items
            for field in ["level", "text", "page"]:
                if field not in item:
                    errors.append(f"Outline item {i} missing required field: '{field}'")
                    continue
                
                if field == "page":
                    if not isinstance(item[field], int) or item[field] < 1:
                        errors.append(f"Outline item {i} field 'page' must be a positive integer")
                elif field == "level":
                    if not isinstance(item[field], str) or item[field] not in ["H1", "H2", "H3"]:
                        errors.append(f"Outline item {i} field 'level' must be one of: H1, H2, H3")
                elif field == "text":
                    if not isinstance(item[field], str) or not item[field].strip():
                        errors.append(f"Outline item {i} field 'text' must be a non-empty string")
    
    return errors

def validate_files(output_dir: Path) -> int:
    """Validate all JSON files in the output directory."""
    json_files = list(output_dir.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {output_dir}")
        return 1
    
    total_errors = 0
    
    for json_file in json_files:
        print(f"Validating {json_file.name}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            errors = validate_output_format(data)
            
            if errors:
                print(f"  ✗ {len(errors)} validation error(s):")
                for error in errors:
                    print(f"    - {error}")
                total_errors += len(errors)
            else:
                print(f"  ✓ Valid format")
                title = data.get("title", "")
                outline_count = len(data.get("outline", []))
                print(f"    Title: {'[Empty]' if not title else title[:50] + ('...' if len(title) > 50 else '')}")
                print(f"    Outline items: {outline_count}")
                
        except json.JSONDecodeError as e:
            print(f"  ✗ Invalid JSON format: {e}")
            total_errors += 1
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            total_errors += 1
    
    print(f"\nValidation complete: {total_errors} total error(s)")
    return 1 if total_errors > 0 else 0

def main():
    output_dir = Path("output")
    
    if not output_dir.exists():
        print(f"Output directory '{output_dir}' does not exist")
        return 1
    
    return validate_files(output_dir)

if __name__ == "__main__":
    sys.exit(main())

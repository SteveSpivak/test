import json
import re

def parse_variable(variable_block):
    # Extract variable name
    match_name = re.search(r'variable\s+"(\w+)"', variable_block)
    name = match_name.group(1) if match_name else None
    
    # Extract variable type
    match_type = re.search(r'type\s*=\s*(\w+)', variable_block)
    var_type = match_type.group(1) if match_type else "unknown"
    
    # Extract default value
    default_match = re.search(r'default\s*=\s*(.+)', variable_block)
    default_value = default_match.group(1).strip() if default_match else None

    # Extract validation (if present)
    validation_condition = None
    error_message = None
    validation_match = re.search(r'validation\s*{[^}]+}', variable_block, re.DOTALL)
    if validation_match:
        validation_block = validation_match.group(0)
        condition_match = re.search(r'condition\s*=\s*(.+)', validation_block)
        error_message_match = re.search(r'error_message\s*=\s*"(.+)"', validation_block)
        validation_condition = condition_match.group(1).strip() if condition_match else None
        error_message = error_message_match.group(1).strip() if error_message_match else None

    return {
        "name": name,
        "type": var_type,
        "default": default_value,
        "validation": {
            "condition": validation_condition,
            "error_message": error_message
        }
    }

# Test Example
variable_block = """
variable "base_name" {
  type = string
  default = "prod"
  validation {
    condition     = "len(value) <= 15"
    error_message = "Base name must be 15 characters or less."
  }
}
"""
print(json.dumps(parse_variable(variable_block), indent=4))

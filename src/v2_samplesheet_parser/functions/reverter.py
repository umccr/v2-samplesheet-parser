from typing import Dict, List, Any, Union
from .util import snake_case_to_pascal_case

def revert_samplesheet_to_csv(samplesheet: Dict[str, Any]) -> str:
    """
    Convert a samplesheet dictionary (JSON format) back to CSV string format.
    
    This function takes a dictionary representation of a samplesheet and converts it
    back to the original CSV format with section headers.
    
    Args:
        samplesheet (Dict[str, Any]): The samplesheet data as a dictionary
        
    Returns:
        str: The samplesheet in CSV format with section headers
        
    Example:
        >>> samplesheet = {
        ...     "header": {
        ...         "file_format_version": "2",
        ...         "run_name": "my-run",
        ...         "instrument_platform": "NovaSeq 6000"
        ...     },
        ...     "reads": {
        ...         "read_1_cycles": "151",
        ...         "read_2_cycles": "151"
        ...     }
        ... }
        >>> csv = revert_samplesheet_to_csv(samplesheet)
        >>> print(csv)
        [Header]
        FileFormatVersion,2
        RunName,my-run
        InstrumentPlatform,NovaSeq 6000
        
        [Reads]
        Read1Cycles,151
        Read2Cycles,151
    """
    sections = []
    
    # Handle non-array sections (header, reads, settings)
    for key, value in samplesheet.items():
        if not key.endswith('_data') and value and isinstance(value, dict):
            section_name = snake_case_to_pascal_case(key)
            rows = []
            
            for k, v in value.items():
                # Convert snake_case to PascalCase for the key
                pascal_key = snake_case_to_pascal_case(k)
                rows.append(f"{pascal_key},{v}")
            
            sections.append(f"[{section_name}]\n{chr(10).join(rows)}\n")
    
    # Handle data sections (arrays)
    for key, value in samplesheet.items():
        if key.endswith('_data') and isinstance(value, list) and value:
            section_name = snake_case_to_pascal_case(key)
            columns = list(value[0].keys())
            
            # Convert column names to PascalCase
            header = ','.join(snake_case_to_pascal_case(col) for col in columns)
            
            # Create rows
            rows = []
            for row in value:
                row_values = [str(row.get(col, '')) for col in columns]
                rows.append(','.join(row_values))
            
            sections.append(f"[{section_name}]\n{header}\n{chr(10).join(rows)}\n")
    
    return '\n'.join(sections)


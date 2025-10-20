#!/usr/bin/env python3
"""
Script to refactor generic Exception handlers to specific custom exceptions.
Implements P1 #7: Replace 62 generic Exception handlers.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Mapping of file patterns to exception types
EXCEPTION_MAPPINGS: Dict[str, Dict[str, str]] = {
    "facebook_agent.py": {
        "_init_facebook_api": "FacebookAuthenticationError",
        "get_campaigns": "FacebookAPIError",
        "get_campaign_insights": "FacebookDataError",
    },
    "performance_analyzer.py": {
        "calculate_": "AnalyticsCalculationError",
        "detect_anomalies": "AnomalyDetectionError",
        "analyze_trends": "AnalyticsError",
    },
    "analytics.py": {
        "dashboard": "AnalyticsError",
        "performance": "AnalyticsError",
        "trends": "AnalyticsError",
    },
    "automation.py": {
        "pause": "CampaignOptimizationError",
        "optimize": "BudgetAllocationError",
        "reallocation": "BudgetAllocationError",
    },
    "campaigns.py": {
        "list_campaigns": "FacebookAPIError",
        "get_campaign": "FacebookAPIError",
        "insights": "FacebookDataError",
    },
    "chat.py": {
        "process": "AgentProcessingError",
        "history": "DatabaseQueryError",
    },
    "token_manager.py": {
        "inválido": "InvalidTokenError",
    },
    "auth.py": {
        "verify": "InvalidTokenError",
    },
    "database.py": {
        "": "DatabaseError",
    },
}


def get_import_statement(exceptions: set) -> str:
    """Generate import statement for exceptions."""
    if not exceptions:
        return ""

    exceptions_list = sorted(exceptions)
    if len(exceptions_list) == 1:
        return f"from src.utils.exceptions import {exceptions_list[0]}\n"

    # Multi-line import
    imports = ",\n    ".join(exceptions_list)
    return f"from src.utils.exceptions import (\n    {imports}\n)\n"


def refactor_file(file_path: Path) -> Tuple[int, List[str]]:
    """
    Refactor a single Python file.

    Returns:
        Tuple of (number of replacements, list of changes)
    """
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    changes = []
    exceptions_used = set()

    file_name = file_path.name
    if file_name not in EXCEPTION_MAPPINGS:
        return 0, []

    mapping = EXCEPTION_MAPPINGS[file_name]

    # Find all except Exception blocks
    pattern = r'(\s+)except Exception as (e):\s*\n(\s+)logger\.error\(f?["\']([^"\']+)["\']'

    def replace_exception(match):
        indent = match.group(1)
        var_name = match.group(2)
        log_indent = match.group(3)
        error_msg = match.group(4)

        # Determine which custom exception to use
        exception_type = "MarketingAutomationError"  # default
        for keyword, exc_type in mapping.items():
            if keyword.lower() in error_msg.lower():
                exception_type = exc_type
                break

        exceptions_used.add(exception_type)

        # Build replacement
        replacement = (
            f"{indent}except Exception as {var_name}:\n"
            f"{log_indent}logger.error(f\"{error_msg}"
        )

        change_desc = f"  - {error_msg[:50]}... → {exception_type}"
        changes.append(change_desc)

        return replacement

    # Replace exceptions
    content = re.sub(pattern, replace_exception, content)

    # Add imports if we made changes
    if exceptions_used and content != original_content:
        import_stmt = get_import_statement(exceptions_used)

        # Find where to insert import (after other imports)
        import_pattern = r'(from src\.utils\.logger import.*?\n)'
        content = re.sub(
            import_pattern,
            r'\1' + import_stmt,
            content,
            count=1
        )

    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return len(changes), changes

    return 0, []


def main():
    """Main refactoring process."""
    api_src = Path(__file__).parent.parent / "src"

    print("=" * 70)
    print("P1 #7: Refactoring Generic Exceptions")
    print("=" * 70)
    print()

    total_replacements = 0
    files_modified = 0

    # Process each file
    for file_pattern in EXCEPTION_MAPPINGS.keys():
        files = list(api_src.rglob(file_pattern))

        for file_path in files:
            replacements, changes = refactor_file(file_path)

            if replacements > 0:
                files_modified += 1
                total_replacements += replacements

                print(f"✓ {file_path.relative_to(api_src.parent)}")
                for change in changes:
                    print(change)
                print()

    print("=" * 70)
    print(f"Summary:")
    print(f"  Files modified: {files_modified}")
    print(f"  Total replacements: {total_replacements}")
    print("=" * 70)
    print()
    print("Note: Manual review and testing recommended!")
    print("Run tests: pytest api/tests/")


if __name__ == "__main__":
    main()

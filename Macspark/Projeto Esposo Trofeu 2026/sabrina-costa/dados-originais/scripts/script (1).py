
import pandas as pd

# Read all Excel files
files = [
    "Relatorio-Fase-1-Desempenho-Completo.xlsx",
    "Sabrina-Performance-Completa-1.xlsx",
    "Sabrina-Performance-Completa.xlsx",
    "Relatorio-Fase-1-Engajamento-Outubro-2025.xlsx",
    "Relatorio-Fase-1-Engajamento-Outubro-2025-1.xlsx",
    "Conta-01-Campanhas-19-de-set-de-2025-18-de-out-de-2025.xlsx"
]

data_summary = {}

for file in files:
    try:
        # Try reading the file
        df = pd.read_excel(file, sheet_name=None)
        
        # Get sheet names and basic info
        sheets = list(df.keys())
        data_summary[file] = {
            'sheets': sheets,
            'data': {}
        }
        
        # For each sheet, get a preview
        for sheet in sheets:
            sheet_df = df[sheet]
            data_summary[file]['data'][sheet] = {
                'shape': sheet_df.shape,
                'columns': sheet_df.columns.tolist(),
                'preview': sheet_df.head(10).to_dict('records')
            }
            
    except Exception as e:
        data_summary[file] = {'error': str(e)}

# Display summary
for file, info in data_summary.items():
    print(f"\n{'='*80}")
    print(f"FILE: {file}")
    print(f"{'='*80}")
    if 'error' in info:
        print(f"ERROR: {info['error']}")
    else:
        print(f"Sheets: {info['sheets']}")
        for sheet, details in info['data'].items():
            print(f"\n  Sheet: {sheet}")
            print(f"  Shape: {details['shape']}")
            print(f"  Columns: {details['columns']}")
            if details['preview']:
                print(f"  Preview (first rows):")
                for i, row in enumerate(details['preview'][:3], 1):
                    print(f"    Row {i}: {row}")

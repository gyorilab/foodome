import json
import pandas as pd
from indra.tools import assemble_corpus as ac
from indra.sources import indra_db_rest as idr
from indra.statements  import stmts_to_json

if __name__ == '__main__':
    POLYPHENOLS_LIST = 'input/list_polyphenols.xlsx'

    # Load the list of polyphenols
    df = pd.read_excel(POLYPHENOLS_LIST)

    results_dict = {}

    for name, pubchem_id in df[['polyphenols', 'pubchem_id']].values:
        # Query the INDRA DB web service using the INDRA Python API
        idrp = idr.get_statements(agents=[f'{pubchem_id}@PUBCHEM'],
                                   ev_limit=100000)
        # Run preassembly
        # 1. Fix common named entity normalization ("grounding") errors
        stmts = ac.map_grounding(idrp.statements)
        # 2. Fix inconsistent sites of post-translational modifications
        stmts = ac.map_sequence(stmts)
        # 3. Identify duplicate/overlapping statements, calculate belief
        stmts = ac.run_preassembly(stmts)

        # Convert statements to JSON
        stmts_json = stmts_to_json(stmts)
        # Store results in dict indexed by Pubchem ID
        results_dict[str(pubchem_id)] = {'name': name, 'statements': stmts_json}

    # Save to file
    with open('output/polyphenol_stmts.json', 'wt') as f:
        json.dump(results_dict, f, indent=2)

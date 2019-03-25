import json
import pandas as pd
from indra.tools import assemble_corpus as ac
from indra.sources import indra_db_rest as idr
from indra.statements  import stmts_to_json

if __name__ == '__main__':
    POLYPHENOLS_LIST = 'input/list_polyphenols.xlsx'

    # Load the list of polyphenol
    df = pd.read_excel(POLYPHENOLS_LIST)

    results_dict = {}

    for name, pubchem_id in df[['polyphenols', 'pubchem_id']].values:
        idrp = idr.get_statements(agents=[f'{pubchem_id}@PUBCHEM'],
                                   ev_limit=100000)
        stmts = ac.map_grounding(idrp.statements)
        stmts = ac.map_sequence(stmts)
        stmts = ac.run_preassembly(stmts)
        stmts_json = stmts_to_json(stmts)
        results_dict[str(pubchem_id)] = {'name': name, 'statements': stmts_json}

    with open('output/polyphenols_stmts.json', 'wt') as f:
        json.dump(results_dict, f, indent=2)

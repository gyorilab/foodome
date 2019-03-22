import pandas as pd
from indra.tools import assemble_corpus as ac
from indra.sources import indra_db_rest as idr


if __name__ == '__main__':
    POLYPHENOLS_LIST = 'data/list_polyphenols.xlsx'

    # Load the list of polyphenol
    df = pd.read_excel(POLYPHENOLS_LIST)

    results_dict = {}

    for name, pubchem_id in df[['polyphenols', 'pubchem_id']].values[0:5]:
        print(name, pubchem_id)
        idrp = idr.get_statements(agents=[f'{pubchem_id}@PUBCHEM'],
                                   ev_limit=100000)
        print(f'Found {len(idrp.statements)} statements')
        stmts = ac.map_grounding(idrp.statements)
        stmts = ac.map_sequence(stmts)
        stmts = ac.run_preassembly(stmts)
        results_dict[pubchem_id] = {'name': name, 'statements': stmts}

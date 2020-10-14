import re
def restrict_to_court_motions(docket_entries):
    '''
    Restricts docket entries to court motions
    restriction is based on the idea that
    input:
        docket entries list [[date, num, text], ...]
    output:
        docket entries list [[date, num, text]
    '''
    import re
    re_court_action = re.compile('\([a-z\, ]{3,20}\)')
    responsive = []
    for i, docket_line in enumerate(docket_entries):
        #Does the docket line exist, if not do nothing
        if len(docket_line) == 3:
            try:
                search_result = re_court_action.search(docket_line[-1])
                if search_result != None:
                    responsive.append(i)
            except TypeError:
                #Not a string
                pass
    return responsive


def checker_notice_of_removal(docket_entries):
    '''
    Checks the docket to see if a case has been removed
    '''
    removed_case = False
    if len(docket_entries) > 0:
        for line in docket_entries:
            try:
                if 'notice of removal' in line[-1].lower():
                    removed_case = True
            except:
                pass
    return removed_case


def inter_event_series(docket_entries, docket_indices):
    '''
    For a given docket, constructs the inter event time series
    input:
        docket entries list [[date, num, text], ...[
    output:
        list inter event series in days [0, 2, 3, ....]
    '''
    import pandas as pd
    import numpy as np
    if len(docket_indices) > 0:
        df = pd.DataFrame(np.array(docket_entries)[docket_indices], columns=['date','link','desc'])
        df['pdate'] = pd.to_datetime(df.date)
        inter_event = df['pdate'].diff().dt.days[1:].values.tolist()
    else:
        return []
    return inter_event

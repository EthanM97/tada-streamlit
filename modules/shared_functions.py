# Description: This file contains all the shared functions used in the Streamlit app

#------------------Navigation Functions--------------------------------

def switch_page(page_name: str):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("tada-streamlit.py")  

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]
    print(page_names)

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


#------------------Download Functions--------------------------------

#Function to prepare modified data frame for download

def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

#Function to prepare pynb notebook for download

def convert_actions_to_pnyb(actions):
    """
    Convert a list of actions to a .pnyb file
    """
    # Create a new notebook
    nb = nbf.v4.new_notebook()
    # Add a markdown cell
    nb['cells'] = [nbf.v4.new_markdown_cell("## Actions")]
    # Add a code cell for each action
    for action in actions:
        nb['cells'].append(nbf.v4.new_code_cell(action))
    # Write to a .pnyb file
    pnyb_file = "actions.pnyb"
    nbf.write(nb, pnyb_file)
    return pnyb_file


#----FUNCTIONS FOR DATAFRAME STYLING------

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

def highlight_max(s):
    '''
    highlight in yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
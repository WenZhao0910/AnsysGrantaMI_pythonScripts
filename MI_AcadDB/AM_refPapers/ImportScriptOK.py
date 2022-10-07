import os
import pandas as pd
import GRANTA_MIScriptingToolkit
from GRANTA_MIScriptingToolkit import granta as mpy
import GRANTA_MIScriptingToolkit as gdl
from tqdm import tqdm

input_file = "C:\\Users\\dmercier\\Downloads\\webofscience08082022.txt"

folder_name = 'Test'

if __name__ == "__main__":

    # Parse csv file
    df = pd.read_csv(input_file, sep="\t")
    print(df.columns)

    mi = mpy.connect('http://azewacadmi1v1.win.ansys.com/mi_servicelayer/', autologon=True)
    db = mi.get_db(db_key='MI_RefPapers')
    tab = db.get_table('Granta Reference Papers')
    # Iterate over every entry of the file
    for i, entry in tqdm(df.iterrows()):
        # print(entry["U2"])
        authors_str = entry["AU"]

        authors_title = ""
        if type(entry["AU"]) != float:
            authors_split = authors_str.split(";")
            for k in range(min(3, len(authors_split))):
                single_author = authors_split[k].split(",")
                # print(single_author)
                authors_title += single_author[0] + ", "
            if len(authors_split) > 3:
                authors_title += " et al. "
        else:
            authors_title = "__NONAME__"
        record_name = authors_title + str(entry["PY"]) + "_" + str(entry["DI"])
        # If the record already exists, leave it alone (server is fairly slow otherwise I'd ask it to modify details

        try:
            record = tab.path_from(None, tree_path=[folder_name], end_node=record_name)
        except GRANTA_MIScriptingToolkit.GRANTA_Exceptions.GRANTA_ServiceLayerError:
            print("record with name", record_name,"already exists")
            record = tab.search_for_records_by_name(record_name)[0]

        tab.bulk_fetch([record], attributes=['Title',
                                             'Remarks - Extra Informations',
                                             'Author(s)',
                                             'Year of Publication',
                                             'Digital Object Identifier (DOI)',
                                             'Key Words / Topics',
                                             'Abstract (or Summary)',
                                             'Journal / Conference / Source'
                                             ])

        # recover the attributes
        title_attribute = record.attributes["Title"]
        author_attribute = record.attributes["Author(s)"]
        year_attribute = record.attributes["Year of Publication"]
        doi_attribute = record.attributes['Digital Object Identifier (DOI)']
        # keyword_attribute = record.attributes['Key Words / Topics']
        abstract_attribute = record.attributes["Abstract (or Summary)"]
        journal_attribute = record.attributes["Journal / Conference / Source"]
        comments_attribute = record.attribute = record.attributes["Remarks - Extra Informations"]
        # change their value
        title_attribute.value = str(entry["TI"])
        author_attribute.value = str(entry["AU"])
        year_attribute.value = str(entry["PY"])
        if type(entry["DI"]) != float:
            doi_attribute.value = mpy.Hyperlink("https://doi.org/" + str(entry["DI"]), hyperlink_display='New')
        # keyword_attribute.value = entry.get('keywords')
        abstract_attribute.value = str(entry["AB"])
        journal_attribute.value = str(entry["SO"])
        # Set the attributes back
        record.set_attributes([title_attribute,
                               author_attribute,
                               year_attribute,
                               doi_attribute,
                               abstract_attribute,
                               journal_attribute]
                              )
        # Update record
        record = mi.update([record])[0]

import GRANTA_MIScriptingToolkit
from GRANTA_MIScriptingToolkit import granta as mpy
from collections import Counter


folder_name = 'YOUR FOLDER NAME HERE'
rec_folder_name = 'YOUR NEW FOLDER NAME HERE'

if __name__ == "__main__":
    mi = mpy.connect('http://azewacadmi1v1.win.ansys.com/mi_servicelayer/', autologon=True)
    db = mi.get_db(db_key='YOUR DB NAME HERE')
    tab_papers = db.get_table('Reference Papers')
    tab_models = db.get_table('Spinal Cord Stimulation Models')

    recs = tab_papers.get_records_from_path(tab_papers,
                                           [folder_name],
                                           use_short_names=True)
    comments_concat = []
    ok_counter = 0
    for rec in recs:
        tab_papers.bulk_fetch([rec], attributes=['Title',
                                             'Comments',
                                             'Author(s)',
                                             'Year of Publication',
                                             'Digital Object Identifier (DOI)',
                                             'Key Words / Topics',
                                             'Abstract',
                                             'Journal / Conference / Source'
                                             ])
        comments_concat.append(rec.attributes["Comments"].value)
        if rec.attributes["Comments"].value == "OK":
            ok_counter += 1
            if len(tab_models.search_for_records_by_name(rec.name)) == 0:
                record_model = tab_models.path_from(None, tree_path=[rec_folder_name], end_node=rec.name)
            else:
                record_model = tab_models.search_for_records_by_name(rec.name)[0]
            # Create link between the two records
            new_linked_recs = rec.links['Models']
            new_linked_recs.add(record_model)
            rec.set_links('Models', new_linked_recs)
            rec = mi.update_links([rec])[0]

    print(ok_counter, "OK papers detected out of", len(recs))
    print(Counter(comments_concat))

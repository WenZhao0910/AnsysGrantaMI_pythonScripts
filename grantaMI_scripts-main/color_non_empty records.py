import GRANTA_MIScriptingToolkit
from GRANTA_MIScriptingToolkit import granta as mpy
from collections import Counter


folder_name = 'YOUR FOLDER NAME HERE'
all_attr_names = ["YOUR",
                  "ATTRIBUTES",
                  "HERE"
                 ]
if __name__ == "__main__":
    mi = mpy.connect('http://azewacadmi1v1.win.ansys.com/mi_servicelayer/', autologon=True)
    db = mi.get_db(db_key='YOUR DB HERE')
    tab_papers = db.get_table('Reference Papers')
    tab_models = db.get_table('Spinal Cord Stimulation Models')

    recs = tab_models.get_records_from_path(tab_models,
                                           [folder_name],
                                           use_short_names=True)
    comments_concat = []
    empty_counter = 0
    for rec in recs:
        is_empty_so_far = True
        print("Color", rec.color)
        for attr in all_attr_names:
            tab_models.bulk_fetch([rec], attributes=[attr])
            if not rec.attributes[attr].is_empty():
                print(rec.name, "Not added to empty list because", attr, "has data")
                is_empty_so_far = False
                rec.color = "Blue"
                rec = mi.update([rec])[0]
                print("Updated Color", rec.color)
                break
        if is_empty_so_far:
            print(rec.name, "is empty")
            empty_counter += 1
    print(empty_counter, "records are still empty in ", folder_name)

import GRANTA_MIScriptingToolkit
from GRANTA_MIScriptingToolkit import granta as mpy
from collections import Counter
import matplotlib.pyplot as plt

folder_name = 'YOUR FOLDER NAME HERE'
rec_filename = 'YOUR DESTINATION RIS PATH HERE.ris'


if __name__ == "__main__":
    mi = mpy.connect('http://azewacadmi1v1.win.ansys.com/mi_servicelayer/', autologon=True)
    db = mi.get_db(db_key='YOUR DB HERE')
    tab_papers = db.get_table('Reference Papers')
    tab_models = db.get_table('Spinal Cord Stimulation Models')
    recs = tab_papers.get_records_from_path(tab_papers,
                                           [folder_name],
                                           use_short_names=True)

    years_of_pub  = []
    with open(rec_filename, 'w') as writer:
        for rec in recs:
            writer.write("TY  - JOUR\n")
            tab_papers.bulk_fetch([rec], attributes=['Title',
                                             'Author(s)',
                                             'Year of Publication',
                                             'Digital Object Identifier (DOI)',
                                             'Key Words / Topics',
                                             'Abstract',
                                             'Journal / Conference / Source'])
            writer.write("T1  - "+rec.attributes["Title"].value+"\n")
            writer.write("Y1  - "+str(rec.attributes["Year of Publication"].value)+"\n")
            writer.write("AB  - "+str(rec.attributes["Abstract"].value)+"\n")

            years_of_pub.append(rec.attributes["Year of Publication"].value)
            writer.write("JF  - "+str(rec.attributes["Journal / Conference / Source"].value)+"\n")
            writer.write("DO  - "+str(rec.attributes['Digital Object Identifier (DOI)'].value)+"\n")
            # Some post processing on authors names
            authors_list = rec.attributes["Author(s)"].value.split(";")
            for author in authors_list:
                lastname_firstname = author.split(", ")
                author_str = lastname_firstname[0] + ", "+ lastname_firstname[1][0].upper() + "."
                writer.write("A1  - " + author_str + "\n")
            writer.write("N2  - "+str(rec.attributes['Abstract'].value)+"\n")
            writer.write("ER  - \n")
        writer.close()

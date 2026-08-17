import pickle

from pyrevit import script
from pyrevit import revit
from nances import getelementid



datafile = script.get_document_data_file("Memory1", "pym")

selection = revit.get_selection()
get_elementid_value = getelementid.get_elementid_value_func()
selected_ids = {str(get_elementid_value(elid)) for elid in selection.element_ids}

f = open(datafile, 'wb')
pickle.dump(selected_ids, f)
f.close()

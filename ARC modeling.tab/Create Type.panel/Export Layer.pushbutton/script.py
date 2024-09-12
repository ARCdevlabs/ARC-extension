# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from rpw.ui.forms import*
from Autodesk.Revit.UI.Selection import*
from nances import message_box
import xlsxwriter
import os
from System.Windows.Forms import MessageBox
from pyrevit import forms
import sys

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

selection = uidoc.Selection.GetElementIds()
if len(selection) == 0:
	message_box("Chọn type tường, sàn, trần ở project browser trước khi sử dụng tool.")
	sys.exit()

try:
	components = [Label('GET LAYERS'),
						Label('Chọn đường dẫn để lưu file excel'),
						Button('...')]
	form = FlexForm('ARC', components)
	form_values = form.show()
	form.values
	value = TextInput('Nhập đường dẫn để tạo file excel', default= forms.pick_folder())
	if not value:
		forms.alert('Chưa nhập đường dẫn để tạo file excel', exitscript=True)
	def is_excel_file_open(file_path):
		if not os.path.exists(file_path):
			return False

		try:
			with open(file_path, 'a'):
				return False
		except IOError:
			return True

	for i in selection:
		ele = doc.GetElement(i)
		category = ele.Category.Name
		if category == "Walls" :
			file_path = str(value) + r'\WallLayer.xlsx' 
			if is_excel_file_open(file_path):
				MessageBox.Show("File Excel đang mở. Vui lòng đóng file và thử lại.")
				break
			else:
				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()
				can_giua = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
				bold_center_border_fill = workbook.add_format({'align': 'center', 'valign': 'vcenter','bold': True,'border': 1,'bg_color': '#ffddcc'})
				bold_red = workbook.add_format({'font_color': '#FF0000','bold': True})
				cell_format = workbook.add_format({'bg_color': '#d0d0e1', 'bold': True,'border': 1})
				cell_format_cen = workbook.add_format({'align': 'center', 'valign': 'vcenter','bg_color': '#d0d0e1', 'bold': True,'border': 1})
				border_outside = workbook.add_format({'border': 1})
				border_fill = workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1,'bg_color': '#d0d0e1'})
				row = 0
				col = 0
				worksheet.write(row,col+1, "Function", bold_center_border_fill)
				worksheet.write(row,col+2, "Material", bold_center_border_fill)
				worksheet.write(row,col+3, "Thickness", bold_center_border_fill)
				worksheet.write(row,col+4, "Wraps", bold_center_border_fill)
				worksheet.write(row,col+5, "Structural Material", bold_center_border_fill)
				worksheet.write(row,col+6, "Variable", bold_center_border_fill)

				#  selection = uidoc.Selection.GetElementIds()

				type_name = []
				for i in selection:
					ele = doc.GetElement(i)
					ten_type = ele.get_Parameter (BuiltInParameter.ALL_MODEL_TYPE_NAME).AsValueString()
					type_name.append(ten_type)
					worksheet.write(row+1, col+1, "Type:    " + type_name[-1],bold_red)
					row += 1
					com_str = ele.GetCompoundStructure()
					lay = com_str.GetLayers()
					count_layer = com_str.LayerCount
					so_lop_ngoai = com_str.	GetNumberOfShellLayers(ShellLayerType.Exterior)
					so_lop_trong = com_str.	GetNumberOfShellLayers(ShellLayerType.Interior)
					so_lop_loi = 	count_layer- so_lop_trong-so_lop_ngoai
					struc = com_str.StructuralMaterialIndex
					variable = com_str.VariableLayerIndex


					Lop_finish_ex = []
					thick_ex = []
					list_fun =[]
					material_structural_ex = []
					variable_ex = []
					wrap_ex = []
					for j in range(so_lop_ngoai):
						ten_vl = lay[j].MaterialId
						ele = doc.GetElement(ten_vl)
						rong = lay[j].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[j].Function) == "Insulation" else str(lay[j].Function)
						wrap  = lay[j].LayerCapFlag

						if ele is None:
							# print(str(j+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							stt= (j+1)
							if stt == struc+1:
								material_structural_ex.append("")
							else:
								material_structural_ex.append("")
							if stt == variable + 1:
								variable_ex.append("☑")
							else:
								variable_ex.append("☐")
							if wrap == True:
								wrap_ex.append("☑")
							else:
								wrap_ex.append("☐")
							Lop_finish_ex.append("<By Category>")
							thick_ex.append(do_day)
							list_fun.append(str(fun))

						else:
							# print(str(j+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							stt= (j+1)
							if stt == struc+1:
								material_structural_ex.append("")
							else:
								material_structural_ex.append("")
							if stt == variable + 1:
								variable_ex.append("☑")
							else:
								variable_ex.append("☐")
							if wrap == True:
								wrap_ex.append("☑")
							else:
								wrap_ex.append("☐")
							Lop_finish_ex.append(ele.Name)
							thick_ex.append(do_day)
							list_fun.append(str(fun))
					for ex in range(len(Lop_finish_ex)):
						# print(ex)
						worksheet.write(row+1, col+1, list_fun[ex],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_ex[ex],border_outside)
						worksheet.write(row+1, col+3, thick_ex[ex],can_giua)
						worksheet.write(row+1, col+4, wrap_ex[ex],can_giua)
						worksheet.write(row+1, col+5, material_structural_ex[ex],border_fill)
						worksheet.write(row+1, col+6, variable_ex[ex],can_giua)
						
						row += 1
						
					worksheet.write(row+1, col+1, "Core Boundary", cell_format)
					worksheet.write(row+1, col+2, "Layers Above Wrap", cell_format)
					worksheet.write(row+1, col+3, "0.0", cell_format_cen)
					worksheet.write(row+1, col+4, "", cell_format)
					worksheet.write(row+1, col+5, "", cell_format)
					worksheet.write(row+1, col+6, "", cell_format)
					row += 1
					# print("Layers Above Wrap")
					Lop_finish_co = []
					thick_co = []
					list_fun_co=[]
					material_structural_co=[]
					variable_co =[]
					wrap_co = []
					for l in range(so_lop_ngoai, count_layer-so_lop_trong):
						ten_vl = lay[l].MaterialId
						rong = lay[l].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[l].Function) == "Insulation" else str(lay[l].Function)
						ele = doc.GetElement(ten_vl)
						wrap  = lay[l].LayerCapFlag
						if ele is None:
							# print(str(l+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							stt= (l+1)
							if stt == struc+1:
								material_structural_co.append("☑")
							else:
								material_structural_co.append("☐")
							if stt == variable + 1:
								variable_co.append("☑")
							else:
								variable_co.append("☐")
							if wrap == True:
								wrap_co.append("")
							else:
								wrap_co.append("")
							Lop_finish_co.append("<By Category>")
							thick_co.append(do_day)
							list_fun_co.append(str(fun))

						else:
							# print(str(l+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(float(do_day)))
							stt= (l+1)
							if stt == struc+1:
								material_structural_co.append("☑")
							else:
								material_structural_co.append("☐")
							if stt == variable + 1:
								variable_co.append("☑")
							else:
								variable_co.append("☐")
							if wrap == True:
								wrap_co.append("")
							else:
								wrap_co.append("")
							Lop_finish_co.append(ele.Name)
							thick_co.append(do_day)
							list_fun_co.append(str(fun))

					for co in range(len(Lop_finish_co)):
						worksheet.write(row+1, col+1, list_fun_co[co],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_co[co],border_outside)
						worksheet.write(row+1, col+3, thick_co[co],can_giua)
						worksheet.write(row+1, col+4, wrap_co[co],border_fill)
						worksheet.write(row+1, col+5, material_structural_co[co],can_giua)
						worksheet.write(row+1, col+6, variable_co[co],can_giua)
						row += 1
					worksheet.write(row+1, col+1, "Core Boundary", cell_format)
					worksheet.write(row+1, col+2, "Layers Below Wrap", cell_format)
					worksheet.write(row+1, col+3, "0.0", cell_format_cen)
					worksheet.write(row+1, col+4, "", cell_format)
					worksheet.write(row+1, col+5, "", cell_format)
					worksheet.write(row+1, col+6, "", cell_format)
					row += 1
					# print("Layers Below Wrap")
					Lop_finish_in = []
					thick_in = []
					list_fun_in=[]
					material_structural_in=[]
					variable_in = []
					wrap_in = []
					for k in range((so_lop_ngoai+so_lop_loi),count_layer):
						ten_vl = lay[k].MaterialId
						ele = doc.GetElement(ten_vl)
						rong = lay[k].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[k].Function) == "Insulation" else str(lay[k].Function)
						wrap  = lay[k].LayerCapFlag
						if ele is None:
							# print(str(k+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							stt= (k+1)
							if stt == struc+1:
								material_structural_in.append("")
							else:
								material_structural_in.append("")
							if stt == variable + 1:
								variable_in.append("☑")
							else:
								variable_in.append("☐")
							if wrap == True:
								wrap_in.append("☑")
							else:
								wrap_in.append("☐")
							Lop_finish_in.append("<By Category>")
							thick_in.append(do_day)
							list_fun_in.append(str(fun))
						else:
							# print(str(k+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							stt= (k+1)
							if stt == struc+1:
								material_structural_in.append("")
							else:
								material_structural_in.append("")
							if stt == variable + 1:
								variable_in.append("☑")
							else:
								variable_in.append("☐")
							if wrap == True:
								wrap_in.append("☑")
							else:
								wrap_in.append("☐")
							Lop_finish_in.append(ele.Name)
							thick_in.append(do_day)
							list_fun_in.append(str(fun))
					for inter in range(len(Lop_finish_in)):
						worksheet.write(row+1, col+1, list_fun_in[inter],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_in[inter],border_outside)
						worksheet.write(row+1, col+3, thick_in[inter],can_giua)
						worksheet.write(row+1, col+4, wrap_in[inter],can_giua)
						worksheet.write(row+1, col+5, material_structural_in[inter],border_fill)
						worksheet.write(row+1, col+6, variable_in[inter],can_giua)
						row += 1
					row += 3
				workbook.close()






		elif category == "Floors" :	
			file_path = str(value) + r'\FloorsLayer.xlsx' 
			if is_excel_file_open(file_path):
				MessageBox.Show("File Excel đang mở. Vui lòng đóng file và thử lại.")
				break
			else:
				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()
				can_giua = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
				bold_center_border_fill = workbook.add_format({'align': 'center', 'valign': 'vcenter','bold': True,'border': 1,'bg_color': '#ffddcc'})
				bold_red = workbook.add_format({'font_color': '#FF0000','bold': True})
				cell_format = workbook.add_format({'bg_color': '#d0d0e1', 'bold': True,'border': 1})
				cell_format_cen = workbook.add_format({'align': 'center', 'valign': 'vcenter','bg_color': '#d0d0e1', 'bold': True,'border': 1})
				border_outside = workbook.add_format({'border': 1})
				border_fill = workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1,'bg_color': '#d0d0e1'})
				row = 0
				col = 0
				worksheet.write(row,col+1, "Function", bold_center_border_fill)
				worksheet.write(row,col+2, "Material", bold_center_border_fill)
				worksheet.write(row,col+3, "Thickness", bold_center_border_fill)
				worksheet.write(row,col+4, "Wraps", bold_center_border_fill)
				worksheet.write(row,col+5, "Structural Material", bold_center_border_fill)
				worksheet.write(row,col+6, "Variable", bold_center_border_fill)

				selection = uidoc.Selection.GetElementIds()
				type_name = []
				for i in selection:
					ele = doc.GetElement(i)
					ten_type = ele.get_Parameter (BuiltInParameter.ALL_MODEL_TYPE_NAME).AsValueString()
					type_name.append(ten_type)
					# print("Type Name", ten_type)

					worksheet.write(row+1, col+1, "Type:    " + type_name[-1],bold_red)
					row += 1
					com_str = ele.GetCompoundStructure()
					lay = com_str.GetLayers()
					count_layer = com_str.LayerCount
					so_lop_ngoai = com_str.	GetNumberOfShellLayers(ShellLayerType.Exterior)
					so_lop_trong = com_str.	GetNumberOfShellLayers(ShellLayerType.Interior)
					so_lop_loi = 	count_layer- so_lop_trong-so_lop_ngoai
					struc = com_str.StructuralMaterialIndex
					variable = com_str.VariableLayerIndex


					Lop_finish_ex = []
					thick_ex = []
					list_fun =[]
					material_structural_ex = []
					variable_ex = []
					wrap_ex = []
					for j in range(so_lop_ngoai):
						ten_vl = lay[j].MaterialId
						ele = doc.GetElement(ten_vl)
						rong = lay[j].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[j].Function) == "Insulation" else str(lay[j].Function)
						wrap  = lay[j].LayerCapFlag

						if ele is None:
							# print(str(j+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							stt= (j+1)
							if stt == struc+1:
								material_structural_ex.append("")
							else:
								material_structural_ex.append("")
							if stt == variable + 1:
								variable_ex.append("☑")
							else:
								variable_ex.append("☐")
							if wrap == True:
								wrap_ex.append("")
							else:
								wrap_ex.append("")
							Lop_finish_ex.append("<By Category>")
							thick_ex.append(do_day)
							list_fun.append(str(fun))

						else:
							# print(str(j+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							stt= (j+1)
							if stt == struc+1:
								material_structural_ex.append("")
							else:
								material_structural_ex.append("")
							if stt == variable + 1:
								variable_ex.append("☑")
							else:
								variable_ex.append("☐")
							if wrap == True:
								wrap_ex.append("")
							else:
								wrap_ex.append("")
							Lop_finish_ex.append(ele.Name)
							thick_ex.append(do_day)
							list_fun.append(str(fun))
					for ex in range(len(Lop_finish_ex)):
						worksheet.write(row+1, col+1, list_fun[ex],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_ex[ex],border_outside)
						worksheet.write(row+1, col+3, thick_ex[ex],can_giua)
						worksheet.write(row+1, col+4, wrap_ex[ex],border_fill)
						worksheet.write(row+1, col+5, material_structural_ex[ex],border_fill)
						worksheet.write(row+1, col+6, variable_ex[ex],can_giua)
						
						row += 1
						
					worksheet.write(row+1, col+1, "Core Boundary", cell_format)
					worksheet.write(row+1, col+2, "Layers Above Wrap", cell_format)
					worksheet.write(row+1, col+3, "0.0", cell_format_cen)
					worksheet.write(row+1, col+4, "", cell_format)
					worksheet.write(row+1, col+5, "", cell_format)
					worksheet.write(row+1, col+6, "", cell_format)
					row += 1
					# print("Layers Above Wrap")
					Lop_finish_co = []
					thick_co = []
					list_fun_co=[]
					material_structural_co=[]
					variable_co =[]
					wrap_co = []
					for l in range(so_lop_ngoai, count_layer-so_lop_trong):
						ten_vl = lay[l].MaterialId
						rong = lay[l].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[l].Function) == "Insulation" else str(lay[l].Function)
						ele = doc.GetElement(ten_vl)
						wrap  = lay[l].LayerCapFlag
						if ele is None:
							# print(str(l+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							stt= (l+1)
							if stt == struc+1:
								material_structural_co.append("☑")
							else:
								material_structural_co.append("☐")
							if stt == variable + 1:
								variable_co.append("☑")
							else:
								variable_co.append("☐")
							if wrap == True:
								wrap_co.append("")
							else:
								wrap_co.append("")
							Lop_finish_co.append("<By Category>")
							thick_co.append(do_day)
							list_fun_co.append(str(fun))

						else:
							# print(str(l+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							stt= (l+1)
							if stt == struc+1:
								material_structural_co.append("☑")
							else:
								material_structural_co.append("☐")
							if stt == variable + 1:
								variable_co.append("☑")
							else:
								variable_co.append("☐")
							if wrap == True:
								wrap_co.append("")
							else:
								wrap_co.append("")
							Lop_finish_co.append(ele.Name)
							thick_co.append(do_day)
							list_fun_co.append(str(fun))

					for co in range(len(Lop_finish_co)):
						worksheet.write(row+1, col+1, list_fun_co[co],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_co[co],border_outside)
						worksheet.write(row+1, col+3, thick_co[co],can_giua)
						worksheet.write(row+1, col+4, wrap_co[co],border_fill)
						worksheet.write(row+1, col+5, material_structural_co[co],can_giua)
						worksheet.write(row+1, col+6, variable_co[co],can_giua)
						row += 1
					worksheet.write(row+1, col+1, "Core Boundary", cell_format)
					worksheet.write(row+1, col+2, "Layers Below Wrap", cell_format)
					worksheet.write(row+1, col+3, "0.0", cell_format_cen)
					worksheet.write(row+1, col+4, "", cell_format)
					worksheet.write(row+1, col+5, "", cell_format)
					worksheet.write(row+1, col+6, "", cell_format)
					row += 1
					# print("Layers Below Wrap")
					Lop_finish_in = []
					thick_in = []
					list_fun_in=[]
					material_structural_in=[]
					variable_in = []
					wrap_in = []
					for k in range((so_lop_ngoai+so_lop_loi),count_layer):
						ten_vl = lay[k].MaterialId
						ele = doc.GetElement(ten_vl)
						rong = lay[k].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[k].Function) == "Insulation" else str(lay[k].Function)
						wrap  = lay[k].LayerCapFlag
						if ele is None:
							# print(str(k+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							stt= (k+1)
							if stt == struc+1:
								material_structural_in.append("")
							else:
								material_structural_in.append("")
							if stt == variable + 1:
								variable_in.append("☑")
							else:
								variable_in.append("☐")
							if wrap == True:
								wrap_in.append("")
							else:
								wrap_in.append("")
							Lop_finish_in.append("<By Category>")
							thick_in.append(do_day)
							list_fun_in.append(str(fun))
						else:
							# print(str(k+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							stt= (k+1)
							if stt == struc+1:
								material_structural_in.append("")
							else:
								material_structural_in.append("")
							if stt == variable + 1:
								variable_in.append("☑")
							else:
								variable_in.append("☐")
							if wrap == True:
								wrap_in.append("")
							else:
								wrap_in.append("")
							Lop_finish_in.append(ele.Name)
							thick_in.append(do_day)
							list_fun_in.append(str(fun))
					for inter in range(len(Lop_finish_in)):
						worksheet.write(row+1, col+1, list_fun_in[inter],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_in[inter],border_outside)
						worksheet.write(row+1, col+3, thick_in[inter],can_giua)
						worksheet.write(row+1, col+4, wrap_in[inter],border_fill)
						worksheet.write(row+1, col+5, material_structural_in[inter],border_fill)
						worksheet.write(row+1, col+6, variable_in[inter],can_giua)
						row += 1
					row += 3
				workbook.close()



		elif category == "Ceilings" :	
			file_path = str(value) + r'\CeilingLayer.xlsx' 
			if is_excel_file_open(file_path):
				MessageBox.Show("File Excel đang mở. Vui lòng đóng file và thử lại.")
				break
			else:
				workbook = xlsxwriter.Workbook(file_path)
				worksheet = workbook.add_worksheet()
				can_giua = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
				bold_center_border_fill = workbook.add_format({'align': 'center', 'valign': 'vcenter','bold': True,'border': 1,'bg_color': '#ffddcc'})
				bold_red = workbook.add_format({'font_color': '#FF0000','bold': True})
				cell_format = workbook.add_format({'bg_color': '#d0d0e1', 'bold': True,'border': 1})
				cell_format_cen = workbook.add_format({'align': 'center', 'valign': 'vcenter','bg_color': '#d0d0e1', 'bold': True,'border': 1})
				border_outside = workbook.add_format({'border': 1})
				border_fill = workbook.add_format({'align': 'center', 'valign': 'vcenter','border': 1,'bg_color': '#d0d0e1'})
				row = 0
				col = 0
				worksheet.write(row,col+1, "Function", bold_center_border_fill)
				worksheet.write(row,col+2, "Material", bold_center_border_fill)
				worksheet.write(row,col+3, "Thickness", bold_center_border_fill)
				worksheet.write(row,col+4, "Wraps", bold_center_border_fill)
				selection = uidoc.Selection.GetElementIds()
				type_name = []
				for i in selection:
					ele = doc.GetElement(i)
					ten_type = ele.get_Parameter (BuiltInParameter.ALL_MODEL_TYPE_NAME).AsValueString()
					type_name.append(ten_type)
					# print("Type Name", ten_type)
					worksheet.write(row+1, col+1, "Type:    " + type_name[-1],bold_red)
					row += 1
					com_str = ele.GetCompoundStructure()
					lay = com_str.GetLayers()
					count_layer = com_str.LayerCount
					so_lop_ngoai = com_str.	GetNumberOfShellLayers(ShellLayerType.Exterior)
					so_lop_trong = com_str.	GetNumberOfShellLayers(ShellLayerType.Interior)
					so_lop_loi = 	count_layer- so_lop_trong-so_lop_ngoai
					variable = com_str.VariableLayerIndex
					Lop_finish_ex = []
					thick_ex = []
					list_fun =[]
					wrap_ex = []
					for j in range(so_lop_ngoai):
						ten_vl = lay[j].MaterialId
						ele = doc.GetElement(ten_vl)
						rong = lay[j].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[j].Function) == "Insulation" else str(lay[j].Function)
						wrap  = lay[j].LayerCapFlag
						if ele is None:
							# print(str(j+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							if wrap == True:
								wrap_ex.append("")
							else:
								wrap_ex.append("")
							Lop_finish_ex.append("<By Category>")
							thick_ex.append(do_day)
							list_fun.append(str(fun))
						else:
							# print(str(j+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							if wrap == True:
								wrap_ex.append("")
							else:
								wrap_ex.append("")
							Lop_finish_ex.append(ele.Name)
							thick_ex.append(do_day)
							list_fun.append(str(fun))
					for ex in range(len(Lop_finish_ex)):
						worksheet.write(row+1, col+1, list_fun[ex],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_ex[ex],border_outside)
						worksheet.write(row+1, col+3, thick_ex[ex],can_giua)
						worksheet.write(row+1, col+4, wrap_ex[ex],cell_format)
						row += 1
					worksheet.write(row+1, col+1, "Core Boundary", cell_format)
					worksheet.write(row+1, col+2, "Layers Above Wrap", cell_format)
					worksheet.write(row+1, col+3, "0.0", cell_format_cen)
					worksheet.write(row+1, col+4, "", cell_format)
					row += 1
					# print("Layers Above Wrap")
					Lop_finish_co = []
					thick_co = []
					list_fun_co=[]
					wrap_co = []
					for l in range(so_lop_ngoai, count_layer-so_lop_trong):
						ten_vl = lay[l].MaterialId
						rong = lay[l].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[l].Function) == "Insulation" else str(lay[l].Function)
						ele = doc.GetElement(ten_vl)
						wrap  = lay[l].LayerCapFlag
						if ele is None:
							# print(str(l+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							if wrap == True:
								wrap_co.append("")
							else:
								wrap_co.append("")
							Lop_finish_co.append("<By Category>")
							thick_co.append(do_day)
							list_fun_co.append(str(fun))
						else:
							# print(str(l+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							if wrap == True:
								wrap_co.append("")
							else:
								wrap_co.append("")
							Lop_finish_co.append(ele.Name)
							thick_co.append(do_day)
							list_fun_co.append(str(fun))
					for co in range(len(Lop_finish_co)):
						worksheet.write(row+1, col+1, list_fun_co[co],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_co[co],border_outside)
						worksheet.write(row+1, col+3, thick_co[co],can_giua)
						worksheet.write(row+1, col+4, wrap_co[co],border_fill)
						row += 1
					worksheet.write(row+1, col+1, "Core Boundary", cell_format)
					worksheet.write(row+1, col+2, "Layers Below Wrap", cell_format)
					worksheet.write(row+1, col+3, "0.0", cell_format_cen)
					worksheet.write(row+1, col+4, "", cell_format)
					row += 1
					# print("Layers Below Wrap")
					Lop_finish_in = []
					thick_in = []
					list_fun_in=[]
					wrap_in = []
					for k in range((so_lop_ngoai+so_lop_loi),count_layer):
						ten_vl = lay[k].MaterialId
						ele = doc.GetElement(ten_vl)
						rong = lay[k].Width*304.8
						do_day = int(rong) if rong.is_integer() else round(rong, 2)
						fun = "Thermal/Air Layer" if str(lay[k].Function) == "Insulation" else str(lay[k].Function)
						wrap  = lay[k].LayerCapFlag
						if ele is None:
							# print(str(k+1) +"." + str(fun)+"-"*10 +"<By Category>" + "-"*10 +str(do_day))
							if wrap == True:
								wrap_in.append("")
							else:
								wrap_in.append("")
							Lop_finish_in.append("<By Category>")
							thick_in.append(do_day)
							list_fun_in.append(str(fun))
						else:
							# print(str(k+1) +"." + str(fun)+"-"*10 + ele.Name+ "-"*10 +str(do_day))
							if wrap == True:
								wrap_in.append("")
							else:
								wrap_in.append("")
							Lop_finish_in.append(ele.Name)
							thick_in.append(do_day)
							list_fun_in.append(str(fun))
					for inter in range(len(Lop_finish_in)):
						worksheet.write(row+1, col+1, list_fun_in[inter],border_outside)
						worksheet.write(row+1, col+2, Lop_finish_in[inter],border_outside)
						worksheet.write(row+1, col+3, thick_in[inter],can_giua)
						worksheet.write(row+1, col+4, wrap_in[inter],cell_format)
						row += 1
					row += 3
				workbook.close()	

	os.startfile(file_path)
except:
	pass
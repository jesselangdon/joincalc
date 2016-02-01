# file name:	JoinCalculate.py
# description:	This function serves as an alternative to joining tables and calculating a field based on a 
#				attribute field from the joined table, using the ArcPy functions Add Join and Calculate Field.  
#				Instead, the JoinCalculate function uses a combination of dictonaries and ArcPy search and  
#				update cursors. The function's development was inspired by code written by Caleb Mackey 
#				(https://geonet.esri.com/thread/112710).
# author:		Jesse Langdon
# dependencies: ESRI arcpy module
# version:		0.1

def main(to_fc, to_join_field, to_attr_field, from_fc, from_join_field, from_attr_field):
    ''' Using dictionaries, this function updates a single attribute 
    field in a feature class based on a field in another feature 
    class. Can be used as an alternative to the AddJoin and 
    CalculateField functions in arcpy module.'''
    import arcpy
    #create dictionary based on 'from_fc' feature class
    from_fields = [from_join_field, from_attr_field]
    from_dict = {}
    with arcpy.da.SearchCursor(from_fc, from_fields) as f_cursor:
        for f_row in f_cursor:
            from_join_val = f_row[0]
            from_attr_val = f_row[1]
            from_dict[from_join_val] = from_attr_val
    del f_row, f_cursor

    # update attribute field in to_fc if join fields are equal
    to_fields = [to_join_field, to_attr_field]
    with arcpy.da.UpdateCursor(to_fc, to_fields) as t_cursor:
        for t_row in t_cursor:
            to_join_val = t_row[0]
            if from_dict.has_key(to_join_val):
                t_row[1] = from_dict[to_join_val]
            t_cursor.updateRow(t_row)
    del t_row, t_cursor
    return to_fc
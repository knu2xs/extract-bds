# import modules
import arcpy
import os.path


def layers_to_geodatabase_feature_classes(layer_list, output_gdb):
    """
    Simply iterate layers in a list and output them to an output geodatabase.
    :param layer_list: List of layers in the current map document
    :param output_gdb: The output geodatabase to store all the data.
    :return:
    """
    # iterate the layer list
    for layer in layer_list:

        # export the data
        layer_to_feature_class(layer, output_gdb)


def layer_to_feature_class(input_layer, output_gdb):
    """
    Using a current map layer, copy all attributes and feautres to a new target feature class using the layer name in
    the table of contents as a guide.
    :param input_layer: Input layer in a map document.
    :param output_gdb: The output geodatabase where the data will reside
    :return:
    """
    # describe input feature class
    desc = arcpy.Describe(input_layer)

    # get feature class name
    fc_name = arcpy.ValidateTableName(os.path.basename(desc.nameString).lower(), output_gdb)

    # create feature class
    output_fc = arcpy.CreateFeatureclass_management(
        out_path=output_gdb,
        out_name=fc_name,
        geometry_type=desc.shapeType,
        spatial_reference=desc.spatialReference
    )[0]

    # list to store all field objects from source feature layer
    field_list = []

    # iterate all field objects
    for field in arcpy.ListFields(input_layer):

        # if the field is not the object id nor the geometry
        if field.type != 'OID' and field.type != 'Geometry':

            # add it to the list
            field_list.append(field)

    # add all fields to output feature class
    for field in field_list:

        # use properties from source field when adding the field to the output feature class
        arcpy.AddField_management(
            in_table=output_fc,
            field_name=field.name,
            field_type=field.type,
            field_precision=field.precision,
            field_scale=field.scale,
            field_length=field.length,
            field_alias=field.aliasName,
            field_is_nullable=field.isNullable,
            field_is_required=field.required
        )

    # get field name list from field list
    field_name_list = [field.name for field in field_list]

    # tack on geometry to the field name list
    field_name_list.append('SHAPE@')

    # create insert cursor instance
    with arcpy.da.InsertCursor(output_fc, field_name_list) as insert_cursor:

        # use a search cursor to iterate the input layer
        for row in arcpy.da.SearchCursor(input_layer, field_name_list):

            # insert the row from the input layer to the output feature class
            insert_cursor.insertRow(row)


if __name__ == '__main__':

    # common layers to extract
    input_layer_list = [
        r'Demographic Layers (BDS)\Block Groups',
        r'Demographic Layers (BDS)\Tracts',
        r'Demographic Layers (BDS)\Places',
        r'Demographic Layers (BDS)\ZIP Codes',
        r'Demographic Layers (BDS)\County Sub Divisions',
        r'Demographic Layers (BDS)\Counties',
        r'Demographic Layers (BDS)\CBSAs',
        r'Demographic Layers (BDS)\Designated Market Areas',
        r'Demographic Layers (BDS)\Congressional Districts',
        r'Demographic Layers (BDS)\States'
    ]

    output_geodatabase = r'Z:\spatialData\censusGeographies\general_purpose.gdb'

    layers_to_geodatabase_feature_classes(input_layer_list, output_geodatabase)

# import modules
import arcpy
import os.path

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

def main(input_layer, output_gdb):
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
    )

    # get field list from existing layer
    field_list = arcpy.ListFields(input_layer)

    # add all fields to output feature class
    for field in field_list:

    # get field name list from field list
    field_name_list = []
    for field in field_list:

        # ensure the field is not the OID
        if field.type != 'OID'

            #

    # use field name list with search cursor on layer and insert cursor
    # copying records to output feature class

if __name__ == '__main__':
    main()

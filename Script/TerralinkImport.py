import os
import sys
import arcpy
from arcpy import env
 
# Set base terralink folders (either 'rural' or 'urban' directory)
terralinkFolders = arcpy.GetParameterAsText(0)

 
# Create variable for new intersect feature class
# and create variable for specified fields/metadata we want to search for
newIntersectFC = arcpy.GetParameterAsText(1)
fields = ['TILENAME', 'FOLDERNAME']
arcpy.AddMessage(' ')
arcpy.AddMessage('Files added and metadata fields found...')
arcpy.AddMessage(' ')
 
 
# Search & assign fields/metadata we declared in 'fields' above for
# our new feature class to the 'tileMatch' variable
arcpy.AddMessage('Compiling metadata information...')
arcpy.AddMessage(' ')
values = [row[0]+'.sid' for row in arcpy.da.SearchCursor(newIntersectFC, fields[0])]
folderMatch = [row[0] for row in arcpy.da.SearchCursor(newIntersectFC, fields[1])]
tileMatch = set(values)
 
 
# Search for Terralink .SID files recursively, based on metadata of
# previously clipped metadata polygons using 'tileMatch'
arcpy.AddMessage('Searching for Terralink .SID file matches to metadata...')
arcpy.AddMessage('--> (this step may take a while)')
arcpy.AddMessage(' ')
sidList = []
for i, val in enumerate(folderMatch):
    terralinkFoldersWithMatches = str(os.path.join(terralinkFolders+'\\', folderMatch[i]))
 
def dirsearch(terralinkFolders):
    for dirpath, dirnames, filenames in os.walk(terralinkFoldersWithMatches):
        sidList.extend([os.path.join(dirpath, fnm) for fnm in tileMatch if fnm.endswith('.sid')])
    return sidList
dirsearch(terralinkFolders)
 
 
# Import files found during search of Terralink imagery directories
arcpy.AddMessage('Adding matched .SID files to current ArcMap document...')
arcpy.AddMessage(' ')
mxd = arcpy.mapping.MapDocument('CURRENT')
dataFrame = arcpy.mapping.ListDataFrames(mxd, '*')[0]
 
for i, result in enumerate(sidList):
    newlayer = arcpy.mapping.Layer(result)
    arcpy.mapping.AddLayer(dataFrame, newlayer, 'BOTTOM')
 
arcpy.AddMessage('Finished.')
arcpy.AddMessage(' ')

import numpy as np
import os, glob, sys, easygui, math, csv
import ogr, osr
from osgeo import ogr


# change to the cwd and get cwf
cwd = os.getcwd()
os.chdir(cwd)
cwf = os.path.basename(cwd)

esriDriver = ogr.GetDriverByName("ESRI Shapefile")


###########################################################################
# Get a list of the SBET record types
# This is the definition of a SBET record
###########################################################################
def sbet_record_types():
    """Function sbet_record_types
       Get a list of the sbet record types
       Arguments:
       Returns: list of the data types in a sbet record
    """
    return [ ("time", np.float64),
             ("lat", np.float64),
             ("lon", np.float64),
             ("alt", np.float64),
             ("ewspeed", np.float64),
             ("nsspeed", np.float64),
             ("vertspeed", np.float64),
             ("roll", np.float64),
             ("pitch", np.float64),
             ("heading", np.float64),
             ("wander", np.float64),
             ("ewacc", np.float64),
             ("nsacc", np.float64),
             ("vertacc", np.float64),
             ("xacc", np.float64),
             ("yacc", np.float64),
             ("zacc", np.float64) ]

###########################################################################
# Read a sbet file into a numpy array.
# This is the function that reads the SBET file and returns the data as a
# numpy array
###########################################################################
def readSbet(filename):
    """Function readSbet
       Read an sbet file into a numpy array.
       Arguments:
                filename: string of filename to read into a numpy array
       Returns: 2-d numpy array of sbet data
    """
    if not isinstance(filename, str):
        raise TypeError("argument 1 to readSbet must be a string")
    return np.fromfile(filename, dtype=np.dtype(sbet_record_types()))


sbetList = []
sbetsOpen = easygui.fileopenbox("Select sbet", filetypes=".out", multiple=True)
for sbets in sbetsOpen:
    print sbets.split("\\")[-1]
    sbetList.append(sbets)
    print sbetList
nSbets = sbetList.__len__()
print '     Number of input sbet Files:  ' + str(nSbets)

# Parse the EO File(s)
for sbet in sbetList:
    sbetPath = os.path.dirname(sbet)
    sbetName = os.path.basename(sbet)
    sbetShp = sbetPath + '\\' + sbetName.strip('out') + 'shp'
    eoPrj = sbetPath + '\\' + sbetName.strip('out') + 'prj'
    sbetTxt = sbetPath + '\\' + sbetName.strip('.out') + '.txt'
    sbetData = readSbet(sbetName)
    print sbetData

    sbetSize = np.size(sbetData)

    getTime = sbetData['time']
    getLatRad = sbetData['lat']
    getLonRad = sbetData['lon']
    getAlt = sbetData['alt']
    getEwspd = sbetData['ewspeed']
    getNsspd = sbetData['nsspeed']
    getVertspd = sbetData['vertspeed']
    getRoll = sbetData['roll']
    getPitch = sbetData['pitch']
    getHeading = sbetData['heading']
    getWander = sbetData['wander']
    getEwacc = sbetData['ewacc']
    getNsacc = sbetData['nsacc']
    getVertacc = sbetData['vertacc']
    getXacc = sbetData['xacc']
    getYacc = sbetData['yacc']
    getZacc = sbetData['zacc']

    # Write a projection file so we can view the shp in ArcGIS or QGIS
    sbetDataSource = esriDriver.CreateDataSource(sbetShp)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4269)
    # srs.SetUTM(int(getZone),1)
    print srs

    # Create the EO shapefile layer
    sbetShpLayer = sbetDataSource.CreateLayer(sbetName, srs, ogr.wkbPoint)

    # Create attribute fields for the shapefile
    nameField = ogr.FieldDefn('time', ogr.OFTString)
    nameField.SetWidth(100)
    sbetShpLayer.CreateField(nameField)
    print nameField
    sbetShpLayer.CreateField(ogr.FieldDefn('time'), ogr.OFTInteger)
    sbetShpLayer.CreateField(ogr.FieldDefn('lat'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('lon'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('ewspeed'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('nsspd'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('vertspeed'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('roll'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('pitch'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('heading'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('wander'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('ewacc'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('nsacc'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('vertacc'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('xacc'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('yacc'), ogr.OFTReal)
    sbetShpLayer.CreateField(ogr.FieldDefn('zacc'), ogr.OFTReal)

    # Loop through the sbetData Array and set the point fields for the shapefile
    for pts in range(0, sbetSize):
        # Create the feature
        feature = ogr.Feature(sbetShpLayer.GetLayerDefn())

        getLatDeg = math.degrees(getLatRad[pts])
        getLonDeg = math.degrees(getLonRad[pts])

        # create the WKT for the feature using Python string formatting
        wkt = "POINT(%f %f)" % (float(getLonDeg), float(getLatDeg))

        # Create the point from the Well Known Txt
        point = ogr.CreateGeometryFromWkt(wkt)

        # Set the feature geometry using the point
        feature.SetGeometry(point)
        feature.SetField('time', getTime[pts])
        feature.SetField('time', getTime[pts])
        feature.SetField('lat', getLatDeg)
        feature.SetField('lon', getLonDeg)
        feature.SetField('ewspeed', getEwspd[pts])
        feature.SetField('nsspd', getNsspd[pts])
        feature.SetField('vertspeed', getVertspd[pts])
        feature.SetField('roll', getRoll[pts])
        feature.SetField('pitch', getPitch[pts])
        feature.SetField('heading', getHeading[pts])
        feature.SetField('wander', getWander[pts])
        feature.SetField('ewacc', getEwacc[pts])
        feature.SetField('nsacc', getNsacc[pts])
        feature.SetField('vertacc', getVertacc[pts])
        feature.SetField('xacc', getXacc[pts])
        feature.SetField('yacc', getYacc[pts])
        feature.SetField('zacc', getZacc[pts])

        # Create the feature in the layer (shapefile)
        #sbetShpLayer.CreateFeature(feature)
        # Dereference the feature
        feature = None

        n = sbetSize
        if (pts % 100 == 0):
            print "percent complete",
            print "\r{0}".format(round((float(pts)/n)*100)),

    # Save and close the data source
    sbetDataSource = None
    print '     Completed importing ' + sbet + '.\n\n'

    # Export the eoData to eoTXT for c3d
    fieldNamesSBET = ['time','lat','lon','ewspeed','nsspd','vertspeed','roll','pitch','heading','wander','ewacc','nsacc','vertacc','xacc','yacc','zacc']
    with open(sbetTxt, 'wb') as f:
        dw = csv.DictWriter(f, fieldNamesSBET)
        for row in sbetData:
            dw.writerow(dict(zip(fieldNamesSBET, row)))

    print "Done writing the SBET file"
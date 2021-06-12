from pyproj import CRS
from pyproj import Transformer
# import get_data
import csv
from pyproj import Geod

# crs = CRS.from_epsg(2961)
#
# proj = Transformer.from_crs(crs, crs.geodetic_crs)#, always_xy=True)
# print(proj.transform(250461.93787206442, 4860207.81233251))
# a, b = proj.transform(250461.93787206442, 4860207.81233251)
# print(a)
# print(b)

def get_ref_data_2(path):
    id_list = []
    with open (path,'r') as csv_file:
        reader =csv.reader(csv_file)
        next(reader) # skip first row
        for row in reader:
            id_list.append(row)
    # print(halifax_id)
    print("> Successfully load data from csv file")
    return id_list


crs = CRS.from_epsg(2961)

proj = Transformer.from_crs(crs, crs.geodetic_crs)
geod = Geod(ellps="WGS84")
vaxsites_filepath = "C:/Users/USER/Desktop/Covid appointment tracker/data-cleaned.csv"
areas_filepath = "C:/Users/USER/Desktop/Covid appointment tracker/Census_2016_Dissemination_Areas.csv"
ref_list = get_ref_data_2(vaxsites_filepath)
areas_list = get_ref_data_2(areas_filepath)

site_list = []
for item in ref_list:
    # x = item[1]
    # y = item[2]
    lat, lon = proj.transform(item[1], item[2])
    site_list.append({'id': item[0], 'lat': lat, 'lon': lon, 'populationDensity': '', 'nearestAreaID': '', 'dist2nearestArea':''})

for item in site_list:
    min_dist = 10000000000000
    for i in areas_list:
        lats = [float(item['lat']), float(i[3])]
        lons = [float(item['lon']), float(i[4])]
        dist = geod.line_length(lons, lats)
        if dist < min_dist:
            min_dist = dist
            item['populationDensity'] = i[2]
            item['nearestAreaID'] = i[1]
            item['dist2nearestArea'] = dist

csv_list = []
for item in site_list:
    csv_list.append([item['id'], item['lat'], item['lon'], float(item['populationDensity']), float(item['nearestAreaID']), item['dist2nearestArea']])

# name of csv file
filename = "cliniclist_with_popDensity.csv"
fields = ['ClinicID', 'lat', 'lon', 'populationDensity', 'nearestAreaDAUID', 'dist2nearestArea']

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(csv_list)

print(csv_list)
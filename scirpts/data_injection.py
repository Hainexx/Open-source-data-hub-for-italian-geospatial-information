import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import requests
from pyproj import CRS
import os

city_region_mapping_df = pd.read_csv("city_region_mapping.csv")
link_catasto = "http://www.geoportale.regione.lombardia.it/rlregis_download/service/package?dbId=514&cod="


class city():
	def __init__(self):
		pass

	def get_city_data(self, city_name, city_file_path):
		self.city_name = city_name
		city_id = city_region_mapping_df.loc[city_region_mapping_df["city_name"] == city_name, "city_id"].values[0]
		resp = requests.get(link_catasto + str(city_id))

		zfile = open("/tmp/" + city_name + ".zip", 'wb')
		zfile.write(resp.content)
		zfile.close()

		with zipfile.ZipFile("/tmp/" + city_name + ".zip", 'r') as zip_ref:
			zip_ref.extractall("/tmp/" + city_name)

		city_df = pd.DataFrame()
		tmp_gdf_volumetrica = gpd.read_file("/tmp/" + city_name + "/dbt/Edificato/Unita_volumetrica.shp")
		city_df["id"] = tmp_gdf_volumetrica["cr_edf_uui"]
		tmp_gdf_volumetrica = tmp_gdf_volumetrica.to_crs(CRS('epsg:4326'))
		city_df["geometry"] = tmp_gdf_volumetrica["geometry"]
		city_df['city'] = city_name
		city_df['id_city'] = city_id
		cols = ["id", "id_city", "city", "geometry"]
		city_df = city_df[cols]
		city_df.to_csv(city_file_path, index=False)
		shutil.rmtree("/tmp/" + city_name)
		os.remove("/tmp/" + f'{city_name}.zip')
		return city_df



cit = city()
cit.get_city_data('brembate', 'ciao2.csv')

final_df = pd.DataFrame(columns = ['id','id_city','city','geometry'])

for city in list(city_region_mapping_df.loc[city_region_mapping_df['region_name'] == 'lombardia', 'city_name'])[:6]:
	tmp_city_df = cit.get_city_data(city, f'{city}.csv')
	final_df = final_df.append(tmp_city_df)

final_df.to_csv('final.csv')

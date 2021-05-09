import geopandas as gpd
import pandas as pd
import zipfile
import shutil
import requests
from pyproj import CRS
import os

from data_sources.basic_data_source import BaseDataSource

city_region_mapping_df = pd.read_csv("scripts/utils/city_region_mapping.csv")
link_catasto = "http://www.geoportale.regione.lombardia.it/rlregis_download/service/package?dbId=514&cod="
COLUMNS = ["id", "city_id", "city_name", "geometry"]

class GeoportaleLombardia(BaseDataSource):
	def __init__(self):
		super().__init__('geoportale_lombardia')

	def download_data(self, city_names_list = None):

		if city_names_list is None:
			# RESTRICTION TO REMOVE (top 5 cities)
			city_names_list = list(city_region_mapping_df.loc[city_region_mapping_df["region_name"] == 'lombardia', "city_name"].values)[:5] 

		final_df = pd.DataFrame(columns = COLUMNS)
		n = len(city_names_list)
		for i, city_name in enumerate(city_names_list):
			print(f'{i+1}/{n} - Downloading {city_name}')
			tmp_city_df = self._download_single_city(city_name)
			final_df = final_df.append(tmp_city_df)

		self.data = final_df

	def _download_single_city(self, city_name):

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
		city_df['city_name'] = city_name
		city_df['city_id'] = city_id

		city_df = city_df[COLUMNS]
		
		shutil.rmtree("/tmp/" + city_name)
		os.remove("/tmp/" + f'{city_name}.zip')
		
		return city_df

if __name__ == "__main__":

	# UNIT TEST 

	downloader = GeoportaleLombardia()
	downloader.download_data(['brembate', 'boltiere'])

	data = downloader.get_data()
	downloader.save_data_to_csv('unit_test')
import argparse

from data_sources.geoportale_lombardia import GeoportaleLombardia

parser = argparse.ArgumentParser()

parser.add_argument('--region', help='region to download')

args = parser.parse_args()

if args.region == 'lombardia':
    downloader = GeoportaleLombardia()
else:
    raise Exception(f'Region {args.region} not yet implemented!')

downloader.download_data()
downloader.save_data_to_csv('complete_dataset')

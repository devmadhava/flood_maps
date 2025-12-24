from shapely.geometry import Point, Polygon
import requests
from fastapi.responses import JSONResponse
from osgeo import gdal

def download_dem(lat, lon, dem_output_path):
    """
        Downloads DEM for a circular buffer around (lon, lat).
        Saves the DEM inside the request folder as: req_path/dem_4326.tif
        Returns the full path to the DEM.
    """
    
    # # DEAL WITH PATH
    # if not os.path.exists(req_path):
    #     os.makedirs(req_path, exist_ok=True)

    # dem_output_path = os.path.join(req_path, "dem_4326.tif")
    
    RADIUS_IN_METERS = 1000
    RADIUS_IN_DEGREE = RADIUS_IN_METERS / 111320
    # point = Point(lon, lat)
    # circle = point.buffer(RADIUS_IN_DEGREE)
    # circle_polygon_coords = [(y, x) for x, y in circle.exterior.coords]
    # Circle Polygon is the working Area
    # print("Circle polygon generated. Example coords:")
    # print(circle_polygon_coords[:5])
    # API DOWNLOAD
    south = lat - RADIUS_IN_DEGREE
    north = lat + RADIUS_IN_DEGREE
    west  = lon - RADIUS_IN_DEGREE
    east  = lon + RADIUS_IN_DEGREE
    print(f"BBOX: W={west}, S={south}, E={east}, N={north}")
    
    # Insert API KEY HERE
    # API_KEY = 
    
    # polygon = Polygon([(lon, lat) for lat, lon in circle_polygon_coords])
    # minx, miny, maxx, maxy = polygon.bounds
    # print("W:", minx, "S:", miny, "E:", maxx, "N:", maxy)
    url = (f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south={south}&north={north}&west={west}&east={east}&outputFormat=GTiff&outputFormat=GTiff&API_Key={API_KEY}")
    # url = (f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south={miny}&north={maxy}&west={minx}&east={maxx}&outputFormat=GTiff&outputFormat=GTiff&API_Key={API_KEY}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"DEM download failed: {str(e)}")
        with open(dem_output_path, "wb") as f:
            f.write(response.content)
            print("DEM saved as dem_4326.tif!")
    except Exception as e:
        raise RuntimeError(f"DEM download failed: {str(e)}")


def convert_dem(input_dem_4326, output_dem_3857):
    """
    Convert a DEM from EPSG:4326 to EPSG:3857.
    Raises exceptions if something goes wrong so FastAPI can catch it.
    """
    # gdal.UseExceptions()
    # src_ds = gdal.Open(input_dem_4326)
    # dst_srs = 'EPSG:3857'
    # gdal.Warp(output_dem_3857, src_ds, dstSRS=dst_srs)
    # src_ds = None
    # print(f"Reprojected DEM saved as {output_dem_3857}")
    try:
        src_ds = gdal.Open(input_dem_4326)
        if src_ds is None:
            raise RuntimeError(f"GDAL failed to open DEM: {input_dem_4326}")
        dst = gdal.Warp(output_dem_3857, src_ds, dstSRS="EPSG:3857")
        if dst is None:
            raise RuntimeError("GDAL Warp returned None (warp failed).")
        print(f"Reprojected DEM saved as {output_dem_3857}")
        return output_dem_3857
    except Exception as e:
        raise RuntimeError(f"DEM reprojection failed: {e}")
    finally:
        src_ds = None
        dst = None
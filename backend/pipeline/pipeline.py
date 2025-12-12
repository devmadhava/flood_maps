import os
from whitebox import WhiteboxTools
from concurrent.futures import ThreadPoolExecutor
from pipeline.download_dem import download_dem, convert_dem
from pipeline.terrain_utils import (
    fill_depressions,
    calc_d8_pointer,
    calc_d8_flow_acc,
    calc_slope_in_degrees,
    calc_slope_in_radians,
    calc_ponding_depth,
    calc_spi,
    calc_twi,
    calc_streams,
    calc_spi_threshold,
    calc_spi_hotspot
)
from pipeline.vector_utils import (
    vectorize_spi_hotspot,
    vectorize_streams,
    calc_polygon_to_line_intersection,
    draw_points_across_line,
    convert_vector_3857_to_4326,
    add_coords_to_points
)
from pipeline.check_dam import (
    add_check_dam_attributes, 
    finalize_check_dams,
    rank_check_dams
)
from models import CheckDamParams   # wherever you defined it

def run_pipeline(lat, lon, req_dir):
    """
    This is the manager for the GIS process.
    Here we will replicate all Google Collab Steps:
        1. Download DEM (EPSG:4326)
        2. Convert to 3857
        3. Fill depressions
        4. Run 5 terrain analyses concurrently (all need filled depressions):
            - D8 pointer
            - D8 flow accumulation
            - Slope (deg)
            - Slope (rad)
            - Ponding depth
    """
    
    if not os.path.exists(req_dir):
        os.makedirs(req_dir, exist_ok=True)
    
    # WBT Setup
    wbt = WhiteboxTools()
    wbt.set_working_dir(req_dir)
    
    # All Possible File paths for quick dev
    dem_4326 = os.path.join(req_dir, "dem_4326.tif")
    dem_3857 = os.path.join(req_dir, "dem_3857.tif")
    filled_dem = os.path.join(req_dir, "filled_dem.tif")
    
    # Terrain Values
    d8_pointer = os.path.join(req_dir,"d8_pointer.tif")
    d8_flow_acc = os.path.join(req_dir,"d8_flow_acc.tif")
    slope = os.path.join(req_dir,"slope.tif")
    slope_radian = os.path.join(req_dir,"slope_acc.tif")
    ponding_depth = os.path.join(req_dir,"ponding_depth.tif")
    
    # Calculated Values
    spi = os.path.join(req_dir,"spi.tif")
    twi = os.path.join(req_dir,"twi.tif")
    streams = os.path.join(req_dir,"streams.tif")
    
    # Downoad the DEM
    download_dem(lat, lon, dem_4326)
    # Turn CRS from 4326 to 3857
    convert_dem(dem_4326, dem_3857)
    # Fill the depressions
    fill_depressions(wbt, dem_3857, filled_dem)
    # Calculate everything that can be calculated with filled_dem i.e. filled depression
    with ThreadPoolExecutor(max_workers=5) as executor:
        commands = [
            executor.submit(calc_d8_pointer, wbt, filled_dem, d8_pointer),
            executor.submit(calc_d8_flow_acc, wbt, filled_dem, d8_flow_acc),
            executor.submit(calc_slope_in_degrees, wbt, filled_dem, slope),
            executor.submit(calc_slope_in_radians, wbt, filled_dem, slope_radian),
            executor.submit(calc_ponding_depth, filled_dem, dem_3857, ponding_depth)
        ]
        
        for c in commands:
            c.result()
    # Calculate SPI, TWI, and Streams
    with ThreadPoolExecutor(max_workers=3) as executor:
        commands = [
            executor.submit(calc_spi, wbt, d8_flow_acc, slope_radian, spi),
            executor.submit(calc_twi, wbt, d8_flow_acc, slope_radian, twi),
            executor.submit(calc_streams, wbt, d8_flow_acc, streams)
        ]
        
        for c in commands:
            c.result()
    
    # Calculate Check Dam Candidates
    # Calculate 95th Percentile [For SPI Hotspots]
    spi_hotspot = os.path.join(req_dir, "spi_hotspot.tif")
    spi_hotspot_vector = os.path.join(req_dir, "spi_hotspot.shp")
    streams_vector = os.path.join(req_dir, "streams.shp")
    spi_stream_clip = os.path.join(req_dir, "spi_stream_clip.shp")
    
    SPI_THRESHOLD = calc_spi_threshold(spi)
    # Calculate SPI Hotspot, Stream Vector, SPI Vector and Intersection
    calc_spi_hotspot(wbt, SPI_THRESHOLD, spi, spi_hotspot)
    vectorize_spi_hotspot(wbt, spi_hotspot, spi_hotspot_vector)
    vectorize_streams(wbt, streams, streams_vector)
    calc_polygon_to_line_intersection(wbt, streams_vector, spi_hotspot_vector, spi_stream_clip)

    # Check DAM Finalization
    check_dams_3857 = os.path.join(req_dir, "check_dams_3857.shp")
    # 50 Meter distance amongst the Check Dams as requried
    draw_points_across_line(50, spi_stream_clip, check_dams_3857)
    check_dam_params = CheckDamParams(
        wbt = wbt,
        slope = slope,
        spi = spi,
        twi = twi,
        filled_dem = filled_dem,
        check_dam_points = check_dams_3857,
        streams_vector = streams_vector
    )
    add_check_dam_attributes(check_dam_params)
    # # Convert Check Dams from meter based (3857) to degree based (4326)
    # # We can Add lon/lat coodinates to a 4326 only
    check_dams_4326 = os.path.join(req_dir, "check_dams_4326.shp")
    convert_vector_3857_to_4326 (check_dams_3857, check_dams_4326)

    # Add Coordinates
    add_coords_to_points(wbt, check_dams_4326)
    # Resulting Check Dams
    check_dams_csv = os.path.join(req_dir, "check_dams.csv")
    # check_dams_csv = os.path.join(req_dir, "check_dams.csv")
    ranked_check_dams = os.path.join(req_dir, "ranked_check_dams.csv")
    check_dams_json = finalize_check_dams(check_dams_4326, check_dams_csv)
    ranked_json = rank_check_dams(5, check_dams_csv, ranked_check_dams)
    # We will send both of these ranked CSV and Raw Data CSV
    
    # print(check_dams_json)
    # print(ranked_json)
    
    return {
        "lat": lat,
        "lon": lon,
        "message": "Reached",
        "check_dams": {
            "ranked_csv": "Future Implementation - URL TO DOWNLOAD",
            "raw_csv": "Future Implementation - URL TO DOWNLOAD",
            # "locations": ranked_json
            "locations": check_dams_json
        }
    }

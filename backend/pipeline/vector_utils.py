import geopandas as gpd
from shapely.geometry import LineString
from models import Convert3857VectorTo4326

# def vectorize_spi_hotspot(wbt, input_path, output_path):
#     "where input is spi_hotspot.tif and output is vector spi_hotspot.shp [etc]"
#     try:
#         wbt.raster_to_vector_polygons(
#             i = input_path,
#             output  = output_path
#         )
#         print("SPI Hotspots spi_hotpsot.tif")
#     except Exception as e:
#         raise RuntimeError(f"SPI Hotspots Calculation Failed: {str(e)}")
    

# def vectorize_streams(wbt, input_path, output_path):
#     "where input is streams.tif and output is vector streams.shp [etc]"
#     try:
#         wbt.raster_to_vector_lines(
#             i = input_path,
#             output  = output_path
#         )
#         print("SPI Hotspots spi_hotpsot.tif")
#     except Exception as e:
#         raise RuntimeError(f"SPI Hotspots Calculation Failed: {str(e)}")
    
# def calc_polygon_to_line_intersection(wbt, input_path, input_spi_hotspot, output_path):
#     "where input is streams.tif and output is vector streams.shp [etc]"
#     try:
#         wbt.clip(
#             i = input_path,
#             clip  = input_spi_hotspot,
#             output = output_path
#         )
#         print("SPI Hotspots spi_hotpsot.tif")
#     except Exception as e:
#         raise RuntimeError(f"SPI Hotspots Calculation Failed: {str(e)}")
from pipeline.utils import calc_raster_percentile


def vectorize_spi_hotspot(wbt, raster_hotspot_path, vector_output):
    """
    Vectorize the SPI hotspot raster into polygons.

    Args:
        wbt: WhiteboxTools instance.
        raster_hotspot_path: Input SPI hotspot raster (.tif).
        vector_output: Output vector file (.shp, .geojson, etc).
    """
    try:
        wbt.raster_to_vector_polygons(
            i=raster_hotspot_path,
            output=vector_output
        )
        print(f"SPI Hotspots vectorized → {vector_output}")
    except Exception as e:
        raise RuntimeError(f"SPI Hotspot Vectorization Failed: {str(e)}")


# def vectorize_streams(wbt, streams_raster_path, streams_vector_output):
#     """
#     Vectorize stream raster into line features.

#     Args:
#         wbt: WhiteboxTools instance.
#         streams_raster_path: Input streams raster.
#         streams_vector_output: Output vector file.
#     """
#     try:
#         wbt.raster_to_vector_lines(
#             i=streams_raster_path,
#             output=streams_vector_output
#         )
#         print(f"Streams vectorized → {streams_vector_output}")
#     except Exception as e:
#         raise RuntimeError(f"Stream Vectorization Failed: {str(e)}")


# def calc_polygon_to_line_intersection(wbt, line_vector_path, polygon_vector_path, intersection_output):
#     """
#     Clip line features by a polygon (line ∩ polygon).

#     Args:
#         wbt: WhiteboxTools instance.
#         line_vector_path: Input line dataset (e.g., vectorized streams).
#         polygon_vector_path: Input polygon dataset (e.g., SPI hotspots).
#         intersection_output: Output clipped vector dataset.
#     """
#     try:
#         wbt.clip(
#             i=line_vector_path,
#             clip=polygon_vector_path,
#             output=intersection_output
#         )
#         print(f"Line–polygon intersection computed → {intersection_output}")
#     except Exception as e:
#         raise RuntimeError(f"Line–Polygon Intersection Failed: {str(e)}")


# def draw_points_across_line(distance, line_vector, output_points):
#     try:
#         gdf = gpd.read_file(line_vector)
#         points = []
#         interval = distance
#         for idx, row in gdf.iterrows():
#             line = row.geometry
#             length = line.length
#             d = 0
#             while d <= length:
#                 pt = line.interpolate(d)
#                 points.append(pt)
#                 d += interval
#         gpd.GeoDataFrame(geometry=points).to_file(output_points)
#     except Exception as e:
#         raise RuntimeError(f"Line–Polygon Intersection Failed: {str(e)}")
    
# def convert_vector_3857_to_4326(params: Convert3857VectorTo4326):
#     try:
#         vector_3857 = params.vector_3857
#         vector_4326 = params.vector_4326
#         gdf = gpd.read_file(vector_3857)
#         gdf = gdf.set_crs(epsg=3857)
#         gdf = gdf.to_crs(epsg=4326)
#         gdf.to_file(vector_4326)
#     except Exception as e:
#         raise RuntimeError(f"Line–Polygon Intersection Failed: {str(e)}")

# def add_coords_to_points(wbt, vector_points):
#     try:
#         wbt.add_point_coordinates_to_table(
#             i=vector_points,
#         )
#     except Exception as e:
#         raise RuntimeError(f"Line–Polygon Intersection Failed: {str(e)}")
    
def vectorize_streams(wbt, streams_raster_path, streams_vector_output):
    """
    Vectorize a raster of streams into line features.

    Args:
        wbt (WhiteboxTools): Instance of WhiteboxTools for GIS processing.
        streams_raster_path (str): File path to the input raster representing streams.
        streams_vector_output (str): File path to the output vector file for stream lines.

    Raises:
        RuntimeError: If the raster to vector conversion fails.
    """
    try:
        wbt.raster_to_vector_lines(
            i=streams_raster_path,
            output=streams_vector_output
        )
        print(f"Streams successfully vectorized → {streams_vector_output}")
    except Exception as e:
        raise RuntimeError(f"Stream Vectorization Failed: {str(e)}")


def calc_polygon_to_line_intersection(wbt, line_vector_path, polygon_vector_path, intersection_output):
    """
    Clip line features by a polygon (line ∩ polygon).

    Args:
        wbt (WhiteboxTools): Instance of WhiteboxTools for GIS processing.
        line_vector_path (str): File path to the input vector file of lines (e.g., vectorized streams).
        polygon_vector_path (str): File path to the polygon vector file (e.g., SPI hotspots).
        intersection_output (str): File path to the output intersection vector dataset.

    Raises:
        RuntimeError: If the clip operation fails.
    """
    try:
        wbt.clip(
            i=line_vector_path,
            clip=polygon_vector_path,
            output=intersection_output
        )
        print(f"Line–polygon intersection computed → {intersection_output}")
    except Exception as e:
        raise RuntimeError(f"Line–Polygon Intersection Failed: {str(e)}")


def draw_points_across_line(distance, line_vector, output_points):
    """
    Generate points along a line at regular intervals.

    Args:
        distance (float): The distance between consecutive points along the line.
        line_vector (str): File path to the vector file containing line geometries.
        output_points (str): File path to save the output point dataset.

    Raises:
        RuntimeError: If generating points or saving the output fails.
    """
    try:
        gdf = gpd.read_file(line_vector)
        points = []
        interval = distance
        for idx, row in gdf.iterrows():
            line = row.geometry
            length = line.length
            d = 0
            while d <= length:
                pt = line.interpolate(d)
                points.append(pt)
                d += interval
        gdf_points = gpd.GeoDataFrame(geometry=points)
        gdf_points.to_file(output_points)
        print(f"Points drawn across lines → {output_points}")
    except Exception as e:
        raise RuntimeError(f"Point generation across lines failed: {str(e)}")


def convert_vector_3857_to_4326(vector_3857, vector_4326):
    """
    Convert vector data from EPSG:3857 to EPSG:4326.

    Args:
        params (Convert3857VectorTo4326): Object containing input and output vector file paths.
            Attributes:
                - vector_3857 (str): File path to the input vector in EPSG:3857.
                - vector_4326 (str): File path to save the converted vector in EPSG:4326.

    Raises:
        RuntimeError: If the coordinate reference system conversion fails.
    """
    try:
        # vector_3857 = params.vector_3857
        # vector_4326 = params.vector_4326
        gdf = gpd.read_file(vector_3857)
        gdf = gdf.set_crs(epsg=3857)
        gdf = gdf.to_crs(epsg=4326)
        gdf.to_file(vector_4326)
        print(f"Vector file converted from EPSG:3857 to EPSG:4326 → {vector_4326}")
    except Exception as e:
        raise RuntimeError(f"CRS conversion failed: {str(e)}")


def add_coords_to_points(wbt, vector_points):
    """
    Add point coordinates to a vector dataset.

    Args:
        wbt (WhiteboxTools): Instance of WhiteboxTools for GIS processing.
        vector_points (str): File path to the input vector points file.

    Raises:
        RuntimeError: If adding coordinates to the points fails.
    """
    try:
        wbt.add_point_coordinates_to_table(
            i=vector_points,
        )
        print(f"Coordinates added to points → {vector_points}")
    except Exception as e:
        raise RuntimeError(f"Adding coordinates to points failed: {str(e)}")
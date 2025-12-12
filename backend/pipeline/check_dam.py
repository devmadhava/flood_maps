from geopandas import gpd
from models import CheckDamParams
import pandas as pd

# # Slope is in degrees
# def add_check_dam_attributes(params: CheckDamParams):
#     wbt = params.wbt
#     check_dam_points = params.check_dam_points 
#     slope = params.slope # Degrees
#     spi = params.spi 
#     twi = params.twi 
#     filled_dem = params.filled_dem 
#     streams_vector = params.streams_vector
#     # Add Attributes
#     pts = gpd.read_file()
    
#     # Clean up
#     # Clean the old value table
#     pts = gpd.read_file(check_dam_points)
#     cols_to_remove = [c for c in pts.columns if c.startswith("VALUE")]
#     pts = pts.drop(columns=cols_to_remove, errors="ignore")
#     pts.to_file(check_dam_points)
    
#     # STREAM VALUE || STRM_VAL
#     # This tells us which stream does the check dam candidate belongs to
#     # If the candidate has no stream then it is no use building a check dam here
#     streams = gpd.read_file(streams_vector)
#     streams["STRM_VAL"] = streams["FID"]
#     points = gpd.read_file(check_dam_points)
#     points = points.set_crs(epsg=3857)
#     joined = gpd.sjoin(points, streams[["STRM_VAL", "geometry"]],
#                    how="left", predicate="intersects")
#     joined = joined.drop(columns=["index_right"], errors="ignore")
    
#     # Add DISTANCE to ascertaint the optimal dams which have atleast X amount of distance between them
#     joined["DISTANCE"] = None
#     for stream_id, group in joined.groupby("STRM_VAL"):
#         line = streams.loc[streams["STRM_VAL"] == stream_id].geometry.values[0]
#         joined.loc[group.index, "DISTANCE"] = group.geometry.apply(lambda pt: line.project(pt))
#     joined.to_file(check_dam_points)
    
#     # STEP 3 — Extract raster values (NOW CLEAN)
#     wbt.extract_raster_values_at_points(
#         inputs=f"{slope};{spi};{twi};{filled_dem}",
#         points=check_dam_points,
#     )
    
#     updated_points = gpd.read_file(check_dam_points)
#     # STEP 4 — merge clean raster values
#     joined = joined.merge(
#         updated_points[["FID", "VALUE1", "VALUE2", "VALUE3", "VALUE4"]],
#         on="FID"
#     )
#     W1 = 0.5
#     W2 = 0.5
#     joined["RANK_SCORE"] = W1 * joined["VALUE1"] + W2 * joined["VALUE2"]
#     joined.to_file(check_dam_points)
    

# def finalize_check_dams_csv(check_dams_4326, check_dams_csv):
#     gdf = gpd.read_file(check_dams_4326)
#     gdf = gdf.rename(columns={
#         "XCOORD": "LON",
#         "YCOORD": "LAT",
#         "VALUE1": "SLOPE",
#         "VALUE2": "SPI",
#         "VALUE3": "TWI",
#         "VALUE4": "ELEV",
#         "distance": "DISTANCE"
#     })
#     gdf = gdf.dropna(subset=["STRM_VAL", "DISTANCE"])
#     # gdf.to_file(check_dams_4326)
#     gdf_no_geom = gdf.drop(columns=["geometry"])
#     gdf_no_geom.to_csv(check_dams_csv, index=False)
#     # gdf_no_geom.to_json

# def rank_check_dams(top_n, check_dams_csv, check_dams_ranked_csv):
#     TOP_N = top_n
#     # Spacing / Hydraulic Design Parameters
#     H = 1.5       # Check dam height in meters
#     S = 0.025     # Desired slope (2.5%)
#     L = H / S     # Ideal horizontal spacing (60m)
#     min_spacing = L - 10  # Minimum acceptable spacing (50 m)
#     max_spacing = L + 10  # Maximum acceptable spacing (70 m)
    
#     # Reading CSV Again
#     # --- Data Loading and Initial Cleaning ---
#     df = pd.read_csv(check_dams_csv)
#     df = df.rename(columns={df.columns[0]: 'ORIGINAL_POINT_ID'})
#     df['ORIGINAL_POINT_ID'] = df['ORIGINAL_POINT_ID'].astype(int)
    
#     required_cols = ["STRM_VAL", "DISTANCE", "SLOPE", "SPI", "TWI", "ELEV",
#                  "RANK_SCORE", "LON", "LAT", "ORIGINAL_POINT_ID"]

#     missing = [c for c in required_cols if c not in df.columns]
#     if missing:
#         raise ValueError(f"Missing required columns in CSV: {missing}")

#     # Final Selected
#     final_selected = []
#     df = df.sort_values(by="RANK_SCORE", ascending=False)

#     # Loop through and compare each entry w.r.t. provided values
#     for stream_id, group in df.groupby("STRM_VAL"):
#     # Ensure within the stream, we iterate from highest rank to lowest
#         group = group.sort_values("RANK_SCORE", ascending=False)

#         selected_on_stream = []

#         for idx, row in group.iterrows():
#             is_valid_site = True

#             # Check against ALL previously selected points on this stream
#             for sel_point in selected_on_stream:
#                 horizontal_dist = abs(row["DISTANCE"] - sel_point["DISTANCE"])

#                 # Enforce Minimum Horizontal Spacing from all selected sites (50m)
#                 if horizontal_dist < min_spacing:
#                     is_valid_site = False
#                     break

#             if is_valid_site:
#                 selected_on_stream.append(row)

#         final_selected.extend(selected_on_stream)
    
#     # Final CSV File
#     final_df = pd.DataFrame(final_selected)
#     # Sort by Rank Score
#     final_df = final_df.sort_values(by="RANK_SCORE", ascending=False)
#     top_df = final_df.head(TOP_N)
#     # 3. Create the final output DataFrame with ONLY the required columns
#     output_cols = ['STRM_VAL', 'DISTANCE', 'SLOPE', 'SPI', 'TWI', 'ELEV', 'RANK_SCORE', 'LON', 'LAT']

#     final_output_df = top_df[output_cols].copy() # We explicitly drop the internal 'ORIGINAL_POINT_ID' column and the pandas index.
#     final_output_df.insert(0, 'DAM_ID', range(1, len(final_output_df) + 1))
#     # Output to a CSV File
#     final_output_df.to_csv(check_dams_ranked_csv, index=False)
#     records = final_output_df.to_dict(orient="records")
#     return records


# from geopandas import gpd
# from models import CheckDamParams
# from pandas import pd

# Slope is in degrees
def add_check_dam_attributes(params: CheckDamParams):
    """
    Add attributes to check dam candidate points, including stream membership, 
    distance to stream, and raster values for slope, SPI, TWI, and elevation.

    Args:
        params (CheckDamParams): Object containing parameters such as file paths for 
            check dam points, slope, SPI, TWI, filled DEM, and stream vectors.

    Raises:
        RuntimeError: If any step of the process (reading files, spatial join, raster extraction) fails.
    """
    try:
        wbt = params.wbt
        check_dam_points = params.check_dam_points 
        slope = params.slope # Degrees
        spi = params.spi 
        twi = params.twi 
        filled_dem = params.filled_dem 
        streams_vector = params.streams_vector

        # Clean up the check dam points data
        pts = gpd.read_file(check_dam_points)
        cols_to_remove = [c for c in pts.columns if c.startswith("VALUE")]
        pts = pts.drop(columns=cols_to_remove, errors="ignore")
        pts.to_file(check_dam_points)
        print(f"Old attributes removed from check dam points → {check_dam_points}")

        # Add STREAM VALUE (STRM_VAL) to check dam points
        streams = gpd.read_file(streams_vector)
        streams["STRM_VAL"] = streams["FID"]
        points = gpd.read_file(check_dam_points)
        points = points.set_crs(epsg=3857)
        joined = gpd.sjoin(points, streams[["STRM_VAL", "geometry"]],
                           how="left", predicate="intersects")
        joined = joined.drop(columns=["index_right"], errors="ignore")
        print("Stream membership added to check dam points.")

        # Add DISTANCE to stream lines for optimal spacing
        joined["DISTANCE"] = None
        for stream_id, group in joined.groupby("STRM_VAL"):
            line = streams.loc[streams["STRM_VAL"] == stream_id].geometry.values[0]
            joined.loc[group.index, "DISTANCE"] = group.geometry.apply(lambda pt: line.project(pt))
        joined.to_file(check_dam_points)
        print(f"Distance to nearest stream added → {check_dam_points}")

        # Step 3: Extract raster values at points (slope, SPI, TWI, ELEV)
        wbt.extract_raster_values_at_points(
            inputs=f"{slope};{spi};{twi};{filled_dem}",
            points=check_dam_points,
        )
        print(f"Raster values extracted for check dam points.")

        # Step 4: Merge raster values back into the check dam points dataset
        updated_points = gpd.read_file(check_dam_points)
        joined = joined.merge(
            updated_points[["FID", "VALUE1", "VALUE2", "VALUE3", "VALUE4"]],
            on="FID"
        )
        W1 = 0.5
        W2 = 0.5
        joined["RANK_SCORE"] = W1 * joined["VALUE1"] + W2 * joined["VALUE2"]
        joined.to_file(check_dam_points)
        print(f"Check dam points ranked and saved → {check_dam_points}")

    except Exception as e:
        raise RuntimeError(f"Error adding check dam attributes: {str(e)}")


def finalize_check_dams(check_dams_4326, check_dams_csv):
    """
    Finalize the check dams by renaming columns and saving the data to a CSV file.

    Args:
        check_dams_4326 (str): File path to the check dams vector dataset (in EPSG:4326).
        check_dams_csv (str): File path to save the final CSV of check dam attributes.

    Raises:
        ValueError: If required columns are missing in the input dataset.
    """
    try:
        gdf = gpd.read_file(check_dams_4326)
        gdf = gdf.rename(columns={
            "XCOORD": "LON",
            "YCOORD": "LAT",
            "VALUE1": "SLOPE",
            "VALUE2": "SPI",
            "VALUE3": "TWI",
            "VALUE4": "ELEV",
            "distance": "DISTANCE"
        })
        gdf = gdf.dropna(subset=["STRM_VAL", "DISTANCE"])
        gdf_no_geom = gdf.drop(columns=["geometry"])
        gdf_no_geom.to_csv(check_dams_csv, index=False)
        print(f"Check dam points saved as CSV → {check_dams_csv}")
        records = gdf_no_geom.to_dict(orient="records")
        return records

    except Exception as e:
        raise RuntimeError(f"Error finalizing check dams CSV: {str(e)}")


def rank_check_dams(top_n, check_dams_csv, check_dams_ranked_csv):
    """
    Rank the check dams based on their suitability and select the top N based on criteria.

    Args:
        top_n (int): The number of top-ranked check dams to select.
        check_dams_csv (str): Path to the CSV file containing the check dam data.
        check_dams_ranked_csv (str): Path to save the ranked check dams data.

    Raises:
        ValueError: If required columns are missing in the CSV file.
    """
    try:
        # Hydraulic Design Parameters
        H = 1.5  # Check dam height in meters
        S = 0.025  # Desired slope (2.5%)
        L = H / S  # Ideal horizontal spacing (60m)
        min_spacing = L - 10  # Minimum acceptable spacing (50 m)
        max_spacing = L + 10  # Maximum acceptable spacing (70 m)

        # Load and clean CSV data
        df = pd.read_csv(check_dams_csv)
        df = df.rename(columns={df.columns[0]: 'ORIGINAL_POINT_ID'})
        df['ORIGINAL_POINT_ID'] = df['ORIGINAL_POINT_ID'].astype(int)

        required_cols = ["STRM_VAL", "DISTANCE", "SLOPE", "SPI", "TWI", "ELEV",
                         "RANK_SCORE", "LON", "LAT", "ORIGINAL_POINT_ID"]

        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns in CSV: {missing}")
        
        # Rank check dams by score
        df = df.sort_values(by="RANK_SCORE", ascending=False)
        final_selected = []

        # Iterate through each stream and select valid check dams
        for stream_id, group in df.groupby("STRM_VAL"):
            group = group.sort_values("RANK_SCORE", ascending=False)
            selected_on_stream = []

            for idx, row in group.iterrows():
                is_valid_site = True

                # Check against previously selected points on this stream
                for sel_point in selected_on_stream:
                    horizontal_dist = abs(row["DISTANCE"] - sel_point["DISTANCE"])

                    # Enforce minimum horizontal spacing (50m)
                    if horizontal_dist < min_spacing:
                        is_valid_site = False
                        break

                if is_valid_site:
                    selected_on_stream.append(row)

            final_selected.extend(selected_on_stream)

        # Save top N ranked check dams
        final_df = pd.DataFrame(final_selected)
        final_df = final_df.sort_values(by="RANK_SCORE", ascending=False)
        top_df = final_df.head(top_n)

        # Create the final output DataFrame and add DAM_ID column
        output_cols = ['STRM_VAL', 'DISTANCE', 'SLOPE', 'SPI', 'TWI', 'ELEV', 'RANK_SCORE', 'LON', 'LAT']
        final_output_df = top_df[output_cols].copy()
        final_output_df.insert(0, 'DAM_ID', range(1, len(final_output_df) + 1))

        # Output the ranked check dams to CSV
        final_output_df.to_csv(check_dams_ranked_csv, index=False)
        records = final_output_df.to_dict(orient="records")
        print(f"Top {top_n} check dams ranked and saved → {check_dams_ranked_csv}")
        return records

    except Exception as e:
        raise RuntimeError(f"Error ranking check dams: {str(e)}")

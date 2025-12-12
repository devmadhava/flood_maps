from pipeline.utils import calc_raster_percentile
import rasterio
import numpy as np

# def fill_depressions(wbt, input_path, output_path):
#     """
#     Fill depressions in the DEM using WhiteboxTools.

#     Args:
#         wbt (WhiteboxTools): Initialized WhiteboxTools instance.
#         input_path (str): Path to input DEM (typically 3857).
#         output_path (str): Output filled DEM path.
#     """
#     try:
#         wbt.fill_depressions(
#             dem=input_path,
#             output=output_path
#         )
#         print("Depression Filled and Saved as: filled_demt.tif")
#     except Exception as e:
#         raise RuntimeError(f"Fill Depression Failed: {str(e)}")

# def calc_d8_pointer(wbt, input_path, output_path):
#     """
#     Calculate D8 pointer raster.

#     Args:
#         wbt: WhiteboxTools instance
#         input_path: Filled DEM path
#         output_path: Output pointer raster path
#     """
#     try:
#         wbt.d8_pointer(
#             dem=input_path,
#             output=output_path
#         )
#         print("Calculated D8 Pointers: d8_pointer.tif")
#     except Exception as e:
#         raise RuntimeError(f"D8 Pointers Calculation Failed: {str(e)}")
    
# def calc_d8_flow_acc(wbt, input_path, output_path):
#     """
#     Calculate D8 flow accumulation raster.

#     Args:
#         wbt: WhiteboxTools
#         input_path: Filled DEM path
#         output_path: Output flow accumulation raster path
#     """
#     try:
#         wbt.d8_flow_accumulation(
#             i=input_path,
#             output=output_path
#         )
#         print("Calculated D8 Flow Acc: d8_flow_acc.tif")
#     except Exception as e:
#         raise RuntimeError(f"D8 Flow Accumulation Calculation Failed: {str(e)}")
    
# def calc_slope_in_degrees(wbt, input_path, output_path):
#     """
#     Compute slope (degrees).

#     Args:
#         wbt: WhiteboxTools
#         input_path: DEM path
#         output_path: Output slope path
#     """
#     try:
#         wbt.slope(
#             dem=input_path,
#             output=output_path,
#             zfactor = 1.0,
#             units = "degrees"
#         )
#         print("Calculated Slope in degrees: slope.tif")
#     except Exception as e:
#         raise RuntimeError(f"Slope Calculation Failed: {str(e)}")
    
# def calc_slope_in_radians(wbt, input_path, output_path):
#     """
#     Compute slope (radians).

#     Args:
#         wbt: WhiteboxTools
#         input_path: DEM path
#         output_path: Output slope path
#     """
#     try:
#         wbt.slope(
#             dem = input_path,
#             output = output_path,
#             zfactor = 1.0,
#             units = "radians"
#         )
#         print("Calculated Slope in radians: slope_radians.tif")
#     except Exception as e:
#         raise RuntimeError(f"Slope (Radians) Calculation Failed: {str(e)}")
    
# def calc_ponding_depth(input_path_filled, input_path_original, output_path):
#     """
#     Compute ponding depth = filled_dem - original_dem.

#     Args:
#         filled_path: Filled DEM path
#         original_path: Original DEM in 3857 projection
#         output_path: Where ponding raster will be saved
#     """
#     try:
#         with rasterio.open(input_path_original) as orig, rasterio.open(input_path_filled) as filled:
#             orig_data = orig.read(1)
#             filled_data = filled.read(1)
#             pond_data = filled_data - orig_data
#             # Make sure there are no negatives in case dem clipping is wrong (did happen before)
#             pond_data = np.where(pond_data < 0, 0, pond_data)
#             profile = orig.profile
#             with rasterio.open(output_path, "w", **profile) as dst:
#                 dst.write(pond_data.astype(np.float32), 1)
#             # print("Ponding Depth saved as:", output_path)
#             print("Calculated Ponding Depth: ponding_depth.tif")
#     except Exception as e:
#         raise RuntimeError(f"Ponding Depth Calculation Failed: {str(e)}")
    
# def calc_spi(wbt, input_path_flow_acc, input_path_slope_radians, output_path):
#     """
#     Compute SPI.

#     Args:
#         wbt: WhiteboxTools
#         input_path_flow_acc: Flow Acc. Path
#         input_path_slope_radians: Slope (radians) Path
#         output_path: Output SPI path
#     """
#     try:
#         wbt.stream_power_index(
#             sca = input_path_flow_acc,
#             slope = input_path_slope_radians,
#             output = output_path,
#         )
#         print("Steam Power Index: spi.tif")
#     except Exception as e:
#         raise RuntimeError(f"SPI Calculation Failed: {str(e)}")
    
# def calc_twi(wbt, input_path_flow_acc, input_path_slope_radians, output_path):
#     """
#     Compute TWI.

#     Args:
#         wbt: WhiteboxTools
#         input_path_flow_acc: Flow Acc. Path
#         input_path_slope_radians: Slope (radians) Path
#         output_path: Output TWI path
#     """
#     try:
#         wbt.wetness_index(
#             sca = input_path_flow_acc,
#             slope = input_path_slope_radians,
#             output = output_path,
#         )
#         print("Topographic Wetness Index: twi.tif")
#     except Exception as e:
#         raise RuntimeError(f"TWI Calculation Failed: {str(e)}")

# def calc_streams(wbt, input_path, output_path):
#     """
#     Compute Streams.

#     Args:
#         wbt: WhiteboxTools
#         input_path: Flow Acc. Path
#         output_path: Output streams path
#     """
    
#     STREAM_THRESHOLD = 100 # 100 Threshold due to size of the DEM 30m
#     try:
#         wbt.extract_streams(
#             flow_accum = input_path,
#             threshold = STREAM_THRESHOLD,
#             output = output_path,
#         )
#         print("Streams stream.tif")
#     except Exception as e:
#         raise RuntimeError(f"Streams Calculation Failed: {str(e)}")
    
# def calc_spi_threshold(input_path):
#     """
#     Compute SPI THRESHOLD.

#     Args:
#         wbt: WhiteboxTools
#         input_path: SPI Input
#     """
#     calc_raster_percentile(input_path, 95)


# def calc_spi_hotspot(wbt, threhsold, input_path, output_path):
#     "input is spi layer"
#     expression = f'("{input_path}" > {threhsold})'
#     try:
#         wbt.raster_calculator(
#             statement = expression,
#             output  = output_path
#         )
#         print("SPI Hotspots spi_hotpsot.tif")
#     except Exception as e:
#         raise RuntimeError(f"SPI Hotspots Calculation Failed: {str(e)}")

# from pipeline.utils import calc_raster_percentile
# import rasterio
# import numpy as np


def fill_depressions(wbt, dem_input, dem_filled):
    """
    Fill depressions in the DEM using WhiteboxTools.

    Args:
        wbt (WhiteboxTools): Initialized WhiteboxTools instance.
        dem_input (str): Path to input DEM (typically EPSG:3857).
        dem_filled (str): Output filled DEM path.
    """
    try:
        wbt.fill_depressions(
            dem=dem_input,
            output=dem_filled
        )
        print(f"Depressions filled → {dem_filled}")
    except Exception as e:
        raise RuntimeError(f"Fill Depression Failed: {str(e)}")


def calc_d8_pointer(wbt, dem_filled, d8_pointer_path):
    """
    Calculate D8 pointer raster.

    Args:
        wbt: WhiteboxTools instance.
        dem_filled: Path to filled DEM.
        d8_pointer_path: Output pointer raster path.
    """
    try:
        wbt.d8_pointer(
            dem=dem_filled,
            output=d8_pointer_path
        )
        print(f"D8 pointer calculated → {d8_pointer_path}")
    except Exception as e:
        raise RuntimeError(f"D8 Pointer Calculation Failed: {str(e)}")


def calc_d8_flow_acc(wbt, dem_filled, flow_acc_path):
    """
    Calculate D8 flow accumulation raster.

    Args:
        wbt: WhiteboxTools instance.
        dem_filled: Path to filled DEM.
        flow_acc_path: Output accumulation raster path.
    """
    try:
        wbt.d8_flow_accumulation(
            i=dem_filled,
            output=flow_acc_path
        )
        print(f"D8 flow accumulation calculated → {flow_acc_path}")
    except Exception as e:
        raise RuntimeError(f"D8 Flow Accumulation Failed: {str(e)}")


def calc_slope_in_degrees(wbt, dem_input, slope_deg_path):
    """
    Compute slope in degrees.

    Args:
        wbt: WhiteboxTools instance.
        dem_input: DEM path.
        slope_deg_path: Output slope path.
    """
    try:
        wbt.slope(
            dem=dem_input,
            output=slope_deg_path,
            zfactor=1.0,
            units="degrees"
        )
        print(f"Slope (degrees) calculated → {slope_deg_path}")
    except Exception as e:
        raise RuntimeError(f"Slope Degrees Calculation Failed: {str(e)}")


def calc_slope_in_radians(wbt, dem_input, slope_rad_path):
    """
    Compute slope in radians.

    Args:
        wbt: WhiteboxTools instance.
        dem_input: DEM path.
        slope_rad_path: Output slope raster path.
    """
    try:
        wbt.slope(
            dem=dem_input,
            output=slope_rad_path,
            zfactor=1.0,
            units="radians"
        )
        print(f"Slope (radians) calculated → {slope_rad_path}")
    except Exception as e:
        raise RuntimeError(f"Slope Radians Calculation Failed: {str(e)}")


def calc_ponding_depth(filled_dem_path, original_dem_path, ponding_output):
    """
    Compute ponding depth = filled_dem - original_dem.

    Args:
        filled_dem_path: Path to filled DEM.
        original_dem_path: Path to original DEM.
        ponding_output: Output ponding raster path.
    """
    try:
        with rasterio.open(original_dem_path) as orig, rasterio.open(filled_dem_path) as filled:
            orig_data = orig.read(1)
            filled_data = filled.read(1)

            pond_data = filled_data - orig_data
            pond_data = np.where(pond_data < 0, 0, pond_data)  # safety

            profile = orig.profile
            profile.update(dtype=rasterio.float32)

            with rasterio.open(ponding_output, "w", **profile) as dst:
                dst.write(pond_data.astype(np.float32), 1)

        print(f"Ponding depth calculated → {ponding_output}")
    except Exception as e:
        raise RuntimeError(f"Ponding Depth Calculation Failed: {str(e)}")


def calc_spi(wbt, flow_acc_path, slope_rad_path, spi_output):
    """
    Compute Stream Power Index (SPI).
    """
    try:
        wbt.stream_power_index(
            sca=flow_acc_path,
            slope=slope_rad_path,
            output=spi_output,
        )
        print(f"Stream Power Index calculated → {spi_output}")
    except Exception as e:
        raise RuntimeError(f"SPI Calculation Failed: {str(e)}")


def calc_twi(wbt, flow_acc_path, slope_rad_path, twi_output):
    """
    Compute Topographic Wetness Index (TWI).
    """
    try:
        wbt.wetness_index(
            sca=flow_acc_path,
            slope=slope_rad_path,
            output=twi_output,
        )
        print(f"Topographic Wetness Index calculated → {twi_output}")
    except Exception as e:
        raise RuntimeError(f"TWI Calculation Failed: {str(e)}")


def calc_streams(wbt, flow_acc_path, streams_output, threshold=100):
    """
    Extract streams using a flow accumulation threshold.

    Args:
        threshold (int): Flow accumulation threshold for stream extraction.
    """
    try:
        wbt.extract_streams(
            flow_accum=flow_acc_path,
            threshold=threshold,
            output=streams_output,
        )
        print(f"Streams extracted → {streams_output}")
    except Exception as e:
        raise RuntimeError(f"Streams Calculation Failed: {str(e)}")


def calc_spi_threshold(spi_path):
    """
    Compute the 95th percentile threshold for SPI.
    """
    return calc_raster_percentile(spi_path, 95)


def calc_spi_hotspot(wbt, threshold, spi_path, hotspot_output):
    """
    Create SPI hotspot raster (1 = hotspot).

    Args:
        threshold: SPI threshold value.
        spi_path: Path to SPI raster.
        hotspot_output: Output hotspot raster path.
    """
    expression = f'("{spi_path}" > {threshold})'
    try:
        wbt.raster_calculator(
            statement=expression,
            output=hotspot_output
        )
        print(f"SPI Hotspots created → {hotspot_output}")
    except Exception as e:
        raise RuntimeError(f"SPI Hotspot Calculation Failed: {str(e)}")

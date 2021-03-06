"""Transform raw Hillsborough, FL data to prepared CSV files."""

import pandas as pd
import numpy as np
import geopandas as gpd
import logging
# from tqdm import tqdm
import click
import yaml
from functools import reduce
import datetime
import re
import json

pd.options.mode.chained_assignment = None


def get_month_as_str_col(df, date_col):
    """Generate a pandas series of the month as a string in YYYY-MM format from the date column.

    Parameters
    ----------
    df : pandas df
        Pandas dataframe
    date_col : str
        Name of the column in the dataframe containing the timestamp

    Returns
    -------
    pandas series
        Pandas series with the month as string in YYYY-MM format
    """
    return df[date_col].dt.to_period("M").astype(str)


def clean_zips(zip_code: str) -> str:
    """Helper function to format input zip codes for input in the PD&R API.

    Parameters
    ----------
    zip : A string
        The zip code we want to clean up.

    Returns
    -------
    str
    """

    # Extract the first five digits from the input
    res = re.search(r"^\d{5}", zip_code)
    return res.group() if res != None else "00000"


def load_evictions_data(data_path, date_col, min_year, max_year, create_geoid = True):
    """Load the evictions data, filter for the correct years, and add a column that 
    contains the month.

    Parameters
    ----------
    data_path : str
        Path to raw mortgage foreclosures data in CSV format
    date_col : str
        The eviction date column from which to extract the month and year
    min_year : int
        Earliest year to include in analysis
    max_year : int
        Latest year to include in analysis

    Returns
    -------
    pandas df
        Dataframe containing evictions data
    """
    ev_raw = (
        pd.read_csv(
            data_path,
            parse_dates=[date_col],
            infer_datetime_format=True,
        )
        .dropna(how="all")
        .drop_duplicates()
    )
    ev_raw["year"] = ev_raw[date_col].dt.year
    ev_df = ev_raw[(ev_raw.year >= min_year) & (ev_raw.year <= max_year)]
    ev_df["year"] = ev_df["year"].astype(int)
    ev_df["month"] = get_month_as_str_col(ev_df, date_col)
    
    if create_geoid == True:
        # Convert to strings
        ev_df["state_code"] = ev_df["state_code"].astype(str).replace(r'\.0', '', regex = True)  
        ev_df["county_code"] = ev_df["county_code"].astype(str).replace(r'\.0', '', regex = True)  
        ev_df["tract_code"] = ev_df["tract_code"].astype(str).replace(r'\.0', '', regex = True)
        # Add zeroes as necessary
        ev_df["state_code"] = ev_df["state_code"].apply(lambda x: (((2-len(x)) * "0") + x) if len(x) < 2 else x)
        ev_df["county_code"] = ev_df["county_code"].apply(lambda x: (((3-len(x)) * "0") + x) if len(x) < 3 else x)
        ev_df["tract_code"] = ev_df["tract_code"].apply(lambda x: (((6-len(x)) * "0") + x) if len(x) < 6 else x)
        # Finally, concat everything
        ev_df["GEOID"] = (
            ev_df["state_code"] + ev_df["county_code"] + ev_df["tract_code"]
        )
    
    return ev_df


def load_mortgage_data(data_path, date_col, min_year, max_year, create_geoid = True):
    """Load the evictions data, filter for the correct years, and add a column that 
    contains the month.

    Parameters
    ----------
    data_path : str
        Path to raw mortgage foreclosures data in CSV format
    date_col : str
        The eviction date column from which to extract the month and year
    min_year : int
        Earliest year to include in analysis
    max_year : int
        Latest year to include in analysis

    Returns
    -------
    pandas df
        Dataframe containing foreclosure data
    """
    mf_raw = (
        pd.read_csv(
            data_path,
            parse_dates=[date_col],
            infer_datetime_format=True,
        )
        .dropna(how="all")
        .drop_duplicates()
    )
    mf_raw["year"] = mf_raw[date_col].dt.year
    mf_df = mf_raw[(mf_raw.year >= min_year) & (mf_raw.year <= max_year)]
    mf_df["year"] = mf_df["year"].astype(int)
    mf_df["month"] = get_month_as_str_col(mf_df, date_col)
    
    if create_geoid == True:
        # Convert to strings
        mf_df["state_code"] = mf_df["state_code"].astype(str).replace(r'\.0', '', regex = True)  
        mf_df["county_code"] = mf_df["county_code"].astype(str).replace(r'\.0', '', regex = True)  
        mf_df["tract_code"] = mf_df["tract_code"].astype(str).replace(r'\.0', '', regex = True)
        # Add zeroes as necessary
        mf_df["state_code"] = mf_df["state_code"].apply(lambda x: (((2-len(x)) * "0") + x) if len(x) < 2 else x)
        mf_df["county_code"] = mf_df["county_code"].apply(lambda x: (((3-len(x)) * "0") + x) if len(x) < 3 else x)
        mf_df["tract_code"] = mf_df["tract_code"].apply(lambda x: (((6-len(x)) * "0") + x) if len(x) < 6 else x)
        # Finally, concat everything
        mf_df["GEOID"] = (
            mf_df["state_code"] + mf_df["county_code"] + mf_df["tract_code"]
        )
    
    return mf_df


def aggregate_evictions(data_frame, filter_col, filter_criteria: list, time_group = "year"):
    # Check for correct judgments
    filter_bool = data_frame[filter_col].isin(filter_criteria)
    """
        
    """
    
    # Aggregate all rows to count eviction filings
    filings_df = data_frame.groupby(by=["GEOID", time_group]).size().to_frame('eviction-filings').reset_index()
    # Aggregate rows with the above judgements to count as actual evictions
    evictions_df = data_frame[filter_bool].groupby(by=["GEOID", time_group]).size().to_frame('evictions').reset_index()
    
    # Returning final data frame
    evictions_final = filings_df.merge(evictions_df, how = 'left', on = ["GEOID", time_group])
    evictions_final["eviction-rate"] = evictions_final["evictions"]/evictions_final["eviction-filings"]

    # Filtering to desired county's GEOIDs only
    # evictions_final = evictions_final[evictions_final.GEOID.str.contains('^12086')]

    return evictions_final


def aggregate_evictions_using_rate_estimates(data_frame, eviction_rates_path, estimate_var = "evictions", time_group = "year"):

    if estimate_var == "evictions":
        # Aggregate all rows to count eviction filings
        filings_df = data_frame.groupby(by=["GEOID", time_group]).size().to_frame('eviction-filings').reset_index()
        
        # Loading eviction rates by tract, using Eviction Lab data for 2014-2016
        eviction_rates_by_tract = pd.read_csv(eviction_rates_path)
        overall_eviction_rate = sum(eviction_rates_by_tract["Total_Evictions"])/sum(eviction_rates_by_tract["Total_Filings"])
        
        eviction_rates_by_tract = eviction_rates_by_tract[["GEOID", "eviction-rate"]]
        eviction_rates_by_tract["GEOID"] = eviction_rates_by_tract["GEOID"].astype(str)
        
        # Returning final data frame
        evictions_final = filings_df.merge(eviction_rates_by_tract, how='left', on='GEOID')
        evictions_final["eviction-rate"].fillna(overall_eviction_rate, inplace=True)
        evictions_final["evictions"] = evictions_final["eviction-filings"] * evictions_final["eviction-rate"]
        evictions_final = evictions_final[["GEOID", time_group, "eviction-filings", "evictions", "eviction-rate"]]
        
        # Filtering to desired county's GEOIDs only
        # evictions_final = evictions_final[evictions_final.GEOID.str.contains('^12057')]

    if estimate_var == "filings":
        # Aggregate all rows to count eviction filings
        filings_df = data_frame.groupby(by=["GEOID", time_group]).size().to_frame('evictions').reset_index()
        
        # Loading eviction rates by tract, using Eviction Lab data for 2014-2016
        eviction_rates_by_tract = pd.read_csv(eviction_rates_path)
        overall_eviction_rate = sum(eviction_rates_by_tract["Total_Evictions"])/sum(eviction_rates_by_tract["Total_Filings"])

        eviction_rates_by_tract = eviction_rates_by_tract[["GEOID", "eviction-rate"]]
        eviction_rates_by_tract["GEOID"] = eviction_rates_by_tract["GEOID"].astype(str)
        
        # Returning final data frame
        evictions_final = filings_df.merge(eviction_rates_by_tract, how='left', on='GEOID')
        evictions_final["eviction-rate"].fillna(overall_eviction_rate, inplace=True)
        evictions_final["eviction-filings"] = evictions_final["evictions"] / evictions_final["eviction-rate"]
        evictions_final = evictions_final[["GEOID", time_group, "eviction-filings", "evictions", "eviction-rate"]]
        
        # Filtering to desired county's GEOIDs only
        # evictions_final = evictions_final[evictions_final.GEOID.str.contains('^12057')]
    return evictions_final


def load_census_data(data_path):
    """Load the ACS data and generate relevant columns.

    Parameters
    ----------
    data_path : str
        Path to ACS data in CSV format

    Returns
    -------
    pandas df
        Dataframe containing ACS data
    """
    census_cols = {
        "DP03_0051E": "total-households",
        "DP04_0047E": "total-renter-occupied-households",
        "DP04_0046E": "total-owner-occupied-households",
        "S2506_C01_001E": "total-owner-occupied-households-mortgage",
        "B25064_001E": "median-gross-rent",
        "DP03_0062E": "median-household-income",
        "B25077_001E": "median-property-value",
        "S2506_C01_039E": "median-monthly-housing-cost",
        "S2502_C01_002E": "pct-white",
        "S2502_C01_003E": "pct-af-am",
        "S2502_C01_009E": "pct-hispanic",
        "S2502_C01_004E": "pct-am-indian",
        "S2502_C01_005E": "pct-asian",
        "S2502_C01_006E": "pct-nh-pi",
        "S2502_C01_008E": "pct-multiple",
        "S2502_C01_007E": "pct-other",
        "DP03_0119E": "pct-below-poverty-level",
        "DP03_0099E": "without-health-insurance",
        "DP03_0096E": "with-health-insurance",
        "DP02_0003E": "households-children",
        "DP02_0009E": "single-parent-household",
        "DP02_0012E": "older-adult-alone",
        "DP02_0058E": "level-of-education",
        "DP02_0095E": "immigrant-status",
        "DP02_0112E": "english-fluency",
        "DP03_0019E": "drive-to-work",
        "DP03_0021E": "public-transport-to-work",
        "DP04_0003E": "vacant-properties",
        "DP04_0014E": "live-in-mobile-home",
        "B25035_001E": "median-year-structure-built",
    }

    census_df = pd.read_csv(data_path, dtype={"GEOID": str})[
        ["GEOID"] + list(census_cols.keys())
    ].rename(columns=census_cols)

    census_df["pct-renter-occupied"] = (
        census_df["total-renter-occupied-households"] / census_df["total-households"]
    ) * 100
    census_df["pct-owner-occupied"] = (
        census_df["total-owner-occupied-households"] / census_df["total-households"]
    ) * 100
    census_df["pct-owner-occupied-mortgage"] = (
        census_df["total-owner-occupied-households-mortgage"]
        / census_df["total-households"]
    ) * 100
    census_df["pct-owner-occupied-without-mortgage"] = (
        (
            census_df["total-owner-occupied-households"]
            - census_df["total-owner-occupied-households-mortgage"]
        )
        / census_df["total-households"]
        * 100
    )
    census_df["median-house-age"] = (
        datetime.datetime.now().year - census_df["median-year-structure-built"]
    )
    census_df["pct-non-white"] = 100 - census_df["pct-white"]
    census_df["pct-without-health-insurance"] = (
        census_df["without-health-insurance"]
        / (census_df["without-health-insurance"] + census_df["with-health-insurance"])
        * 100
    )
    return census_df.drop(
        [
            "without-health-insurance",
            "with-health-insurance",
            "median-year-structure-built",
        ],
        axis=1,
    )


def get_totals_across_years(df, tract_col, data_col):
    """Get the sum and average of a datapoint across all years for a given geography.

    Parameters
    ----------
    df : pandas df
        Dataframe where each row contains a datapoint by year by geography, e.g. columns = 
        ['year', 'tract', 'num_evictions']
    tract_col : str
        Name of the column that contains the tract/geography identifier
    data_col : str
        Name of the column that contains the data point to be aggregated
    
    Returns
    -------
     : pandas df
        Dataframe containing the sum and average of the data point across all years for each 
        geography
    """
    return df.groupby(tract_col)[data_col].agg(["sum", "mean"]).reset_index()


def create_year_cols_from_df(df, data_cols, data_col_prefix_mapper, year_col, geo_col):
    """Generate the year columns from the dataframe containing yearly data in separate rows. The 
    resulting dataframe will be reduced to only one row for each geography, with the yearly data
    included in separate columns with the suffix of that year. For example, "evictions" will become
    "evictions-2014".

    Parameters
    ----------
    df : pandas df
        Dataframe with yearly data, with columns containing [year, geo_col, data_col]
    data_cols : list of str
        List of data column names to retain
    data_col_prefix_mapper : dict
        Dictionary mapping original data columns to new prefixes, e.g. {'evictions': 'total-evictions'}
    year_col : str
        Name of the column containing the year information
    geo_col : str
        Name of the geographic identifier column. This will be used as the primary key

    Returns
    -------
    df
        Dataframe with the geo_col column and len(data_cols) * len(years) columns (one column per
        year per data point)
    """
    # Get the unique list of years that are present in the dataframe
    years_list = set(df[year_col].tolist())
    year_dfs = []

    # For each year, generate a dataframe containing only that year's information. Add the year to
    # the end of the data column name and rename as necessary
    for year in years_list:
        year_df = df[df[year_col] == year][[geo_col] + data_cols].rename(
            columns={
                data_col: f"{data_col_prefix_mapper.get(data_col, data_col)}-{str(year)}"
                for data_col in data_cols
            }
        )
        year_dfs.append(year_df)

    # Combine all the year dataframes
    # result = reduce(lambda left, right: pd.merge(left, right, on=geo_col), year_dfs)
    result = reduce(lambda left, right: pd.merge(left, right, on=geo_col, how="outer"), year_dfs)
    result = result.fillna(0)
    return result


def build_rename_mapper_from_df(df, chunk_name_mapper):
    """Build a dictionary where the keys are the current column names and the values are new
    column names based on an input dictionary that contains substrings to rename. For example,
    if the dataframe contains the columns 'evictions-2016' and 'evictions-2017', and the 
    chunk_name_mapper contains {'evictions': 'total-evictions'}, this function would generate a new
    dictionary containing {'evictions-2016': 'total-evictions-2016', 'evictions-2017', 
    'total-evictions-2017'}. This allows us to generate a dictionary to rename columns that contain 
    yearly data without having to manually specify the year.

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing columns to rename
    chunk_name_mapper : dict of str
        Dict mapping the old substring to the new substring, e.g. {'evictions': 'total-evictions'}

    Returns
    -------
    dict of str
        Dict mapping the old column names to new column names
    """
    rename_mapper = {}
    for column_name_chunk in chunk_name_mapper:
        for c in df.columns:
            if column_name_chunk in c:
                rename_mapper[c] = c.replace(
                    column_name_chunk, chunk_name_mapper[column_name_chunk]
                )
    return rename_mapper


def add_yearly_rates_to_merged_df(
    merged_df, counts_to_rate_name_mapper, rate_denom_col
):
    """Add the yearly rates columns to the merged dataframe by dividing the yearly counts column by 
    the rate denominator column. 

    Parameters
    ----------
    merged_df : pandas df
        Dataframe containing the year counts and rate denominator columns
    counts_to_rate_name_mapper : dict
        Dictionary that maps the count column name to the rate column name, e.g.
        {'eviction-filings': 'eviction-filing-rate'}
    rate_denom_col : str
        Column containing the data to use as the denominator

    Returns
    -------
    pandas df
        Dataframe containing the yearly rates
    """
    rename_mapper = build_rename_mapper_from_df(merged_df, counts_to_rate_name_mapper)
    rates_df = (
        merged_df[rename_mapper.keys()]
        .div(merged_df[rate_denom_col], axis=0)
        .multiply(100)
        .rename(columns=rename_mapper)
    )
    return pd.concat([merged_df, rates_df,], axis=1,)


def merge_street_address(*address_vals):
    """Merge the different pieces of a street address into a single, space-separated string.

    Returns
    -------
    str
        The merged address
    """
    valid_vals = [str(c).strip() for c in address_vals if str(c) not in ("nan", "None")]
    return " ".join(valid_vals)


def get_counts_by_tract(mf_with_tract, output_col_name):
    """Return a dataframe containing the the mortgage foreclosure counts by Census Tract by year.

    Parameters
    ----------
    mf_with_parcels : pandas df
        Mortgage foreclosure data, where each row represents a foreclosed property and its parcel
        ID

    Returns
    -------
    pandas df
        Dataframe with columns ['year', 'GEOID', 'num_mortgage_foreclosures']
    """
    
    # Get the counts by census tract by year
    counts_by_ct_by_year = mf_with_tract.groupby(["year", "GEOID"]).size().to_frame('num').reset_index()

    # Reset index to add year column & clean up
    mf_counts_by_ct = (
        counts_by_ct_by_year
        .rename(columns={"num": output_col_name},) # "num_mortgage_foreclosures" or "lien-foreclosures"
    )
    return mf_counts_by_ct


def add_housing_loss_index(merged, eviction_counts_df, mortgage_counts_df, year_col):
    """Add the housing loss index columns to the merged dataframe containing all the housing loss
    rates.

    Parameters
    ----------
    merged : pandas df
        Dataframe containing housing loss rates for different housing loss types

    Returns
    -------
    pandas df
        The input df with housing loss index columns
    """
    merged["avg-eviction-rate"] = (
        merged["avg-evictions"] / merged["total-renter-occupied-households"]
    ) * 100

    # Temporary columns for ratio-to-mean-calculations
    merged["overall-county-foreclosure-rate"] = ((np.sum(merged["avg-foreclosure-sales"][np.isfinite(merged["avg-foreclosure-sales"])]))/sum(merged["total-owner-occupied-households-mortgage"]))*100
    merged["overall-county-eviction-rate"] = ((np.sum(merged["avg-evictions"][np.isfinite(merged["avg-evictions"])]))/sum(merged["total-renter-occupied-households"]))*100
    merged["overall-county-housing-loss-rate"] = ((((np.sum(merged["avg-evictions"][np.isfinite(merged["avg-evictions"])])) + (np.sum(merged["avg-foreclosure-sales"][np.isfinite(merged["avg-foreclosure-sales"])])))/((sum(merged["total-renter-occupied-households"]) + sum(merged["total-owner-occupied-households-mortgage"]))))*100)

    merged["ratio-to-mean-foreclosure-rate"] = (
        merged["avg-foreclosure-rate"] / merged["overall-county-foreclosure-rate"]
    )
    merged["ratio-to-mean-eviction-rate"] = (
        merged["avg-eviction-rate"] / merged["overall-county-eviction-rate"]
    )

    # Check to make sure that the mortgage foreclosure and evictions data cover the same
    # date range; if they don't match, we won't generate any data for these next columns.
    eviction_years = set(eviction_counts_df[year_col].tolist())
    mortgage_years = set(mortgage_counts_df[year_col].tolist())
    if eviction_years != mortgage_years:
        logging.info(
            "Available eviction data years (%s) don't match mortgage years (%s). No housing loss index data will be computed."
            % (sorted(eviction_years), sorted(mortgage_years))
        )
        fill_in_str = "Not available for this time frame."
        merged["avg-housing-loss-rate"] = fill_in_str
        merged["evictions-pct-total-housing-loss"] = fill_in_str
        merged["housing-loss-index"] = fill_in_str
        return merged

    # If they do match, we compute the HLI and other housing loss columns.
    merged["avg-lost-housing"] = (
        merged["avg-evictions"] + merged["avg-foreclosure-sales"]
    )
    merged["avg-housing-loss-rate"] = (
        merged["avg-lost-housing"]
        / (
            merged["total-renter-occupied-households"]
            + merged["total-owner-occupied-households-mortgage"]
        )
        * 100
    )
    merged["evictions-pct-total-housing-loss"] = (
        merged["avg-evictions"] / merged["avg-lost-housing"]
    )
    merged["housing-loss-index"] = (
        merged["avg-housing-loss-rate"] / merged["overall-county-housing-loss-rate"]
    )
    return merged.drop(['avg-lost-housing', 'overall-county-eviction-rate', 'overall-county-foreclosure-rate' , 'overall-county-housing-loss-rate'], axis=1)


def get_counts_by_month(df, month_col, counts_col_name):
    """Get the count of rows by a given column and rename the counts column.

    Parameters
    ----------
    df : pandas df
        Dataframe containing rows to count and the month column to group by
    month_col : str
        Name of the column containing the month; will be grouped by this column
    counts_col_name : str
        Name to give the column with the counts by month

    Returns
    -------
    pandas df
        Dataframe with columns = ['month', counts_col_name]
    """
    return (
        df.groupby(month_col)
        .count()[df.columns[0]]
        .reset_index()
        .rename(columns={df.columns[0]: counts_col_name})
    )


def generate_time_series_df(eviction_df, mortgage_df, tax_df):
    """Generate the dataframe containing the count of housing loss events by month. Only includes
    mortgage and tax foreclosures since we do not have the evictions by month.

    Parameters
    ----------
    mortgage_df : pandas df
        Dataframe containing the mortgage data; must include "month" column
    tax_df : pandas df
        Dataframe containing the tax data; must include "month" column

    Returns
    -------
    pandas df
        Dataframe containing the mortgage and tax foreclosures counts by month,
        columns = ['month', 'total-foreclosures', 'total-lien-foreclosures']
    """
    evictions_by_month = get_counts_by_month(eviction_df, "month", "total-eviction-filings")
    mortgage_by_month = get_counts_by_month(mortgage_df, "month", "total-foreclosures")
    tax_by_month = get_counts_by_month(tax_df, "month", "total-lien-foreclosures")
    timeseries_df = evictions_by_month.merge(mortgage_by_month, on="month", how="outer")
    timeseries_df = timeseries_df.merge(tax_by_month, on="month", how="outer")
    return timeseries_df


def reformat_tract_code(tract: str, state_code: str, county_code: str) -> str:
    """Helper function to return GEOIDs compatible with those in deep-dive data files.

    Parameters
    ----------
    tract : A string
        An unformatted tract code, e.g. '53.38'
    state_code : A string
        The FIPS code for the state that we want to append.
    county_code : A string
        The FIPS code for the county that we want to append.

    Returns
    -------
    str
    """
    
    # If the tract code contains a period, remove it, then prepend zeroes until length is 6
    if "." in tract:
        tract = tract.replace(".", "")
        num_zeroes = 6 - len(tract)
        tract = ("0" * num_zeroes) + tract
    # Else prepend zeroes until the length is 4, then add 2 zeroes to the end
    else:
        num_zeroes = 4 - len(tract)
        tract = ("0" * num_zeroes) + tract + "00"
    
    # Prepend state and county FIPS codes
    geoid = state_code + county_code + tract
    
    return geoid


def order_columns(output_df, census_cols):
    """Orders the columns according to required csv format
    Parameters
    ----------
    output_df : DataFrame
        Dataframe containing all output columns
        
    census_cols : list
        list containing all census variable names to keep in output, defined in config.json
        
    
    Returns
    -------
    list
        list of ordered columns
    """
    ordered_columns = []
    # geo columns
    ordered_columns.extend([
        'county_GEOID', 'census_tract_GEOID', 'bloc-group-code', 'county',
        'state'
    ])

    #eviction columns
    ordered_columns.extend(
        [col for col in output_df.columns if 'tract-avg-eviction' in col])
    ordered_columns.extend(
        [col for col in output_df.columns if col.startswith('eviction-rate')])
    ordered_columns.extend([
        col for col in output_df.columns if col.startswith('total-evictions')
    ])

    #foreclosure columns
    ordered_columns.extend(
        [col for col in output_df.columns if 'tract-avg-foreclosure' in col])
    ordered_columns.extend([
        col for col in output_df.columns if col.startswith('foreclosure-rate')
    ])
    ordered_columns.extend([
        col for col in output_df.columns if col.startswith('foreclosure-sales')
    ])

    # lien foreclosure
    ordered_columns.extend(
        [col for col in output_df.columns if 'lien-foreclosure-rate-' in col])
    ordered_columns.extend([
        col for col in output_df.columns
        if col.startswith('lien-foreclosures-')
    ])

    #housing loss
    ordered_columns.extend(
        [col for col in output_df.columns if 'avg-housing-loss-rate' in col])
    ordered_columns.extend(
        [col for col in output_df.columns if 'housing-loss-index' in col])
    ordered_columns.extend(
        ["ratio-to-mean-eviction-rate", "ratio-to-mean-foreclosure-rate"])

    #census
    ordered_columns.extend(census_cols)

    return output_df[[
        col for col in ordered_columns if col in output_df.columns
    ]]


@click.command()
@click.option(
    "--config_path",
    type=click.File("r"),
    help="Path to yaml containing config parameters.",
)
def main(config_path):
    """Process raw Marion, IN housing loss data and write timeseries (counts by month) data and
    aggregate data (by census tract) to CSV.

    Parameters
    ----------
    config_path : str
        Path to the yaml config file containing the input and output file paths
    """
    logging.info("Loading raw data files. This may take a few minutes.")
    config = yaml.load(config_path, yaml.SafeLoader)
    min_year = config["min_year"]
    max_year = config["max_year"]

    # The Eviction Lab data came in two files (2014-2016 and 2017-2018) with different formats, so
    # we need to read them in separately and merge them later.
    eviction_df = load_evictions_data(
        config["eviction_data_path"],
        "Disposition Date",
        min_year,
        max_year,
        create_geoid = True
    )
    mortgage_df = load_mortgage_data(
        config["mortgage_foreclosure_data_path"], 
        "Disposition Date",
        min_year, 
        max_year,
        create_geoid = True
    )
    tax_df = load_mortgage_data(
        config["tax_foreclosure_data_path"],
        "Disposition Date", 
        min_year, 
        max_year
        )
    census_df = load_census_data(config["acs_data_path"])

    # Generate the time series data and save output
    logging.info("Generating time series data (monthly counts of housing loss events).")

    # Calculating eviction totals separately because number of evictions does not always equal number of rows in the df
    # Calculating eviction totals separately because number of evictions does not always equal number of rows in the df
    evictions_monthly = aggregate_evictions_using_rate_estimates(
        eviction_df,
        config["path_to_eviction_filing_rates"],
        estimate_var = "evictions",
        time_group = "month"
    )
    evictions_monthly = evictions_monthly[["evictions", "month"]].groupby("month").sum().reset_index()


    # Creating timeseries df and merging on separate eviction counts
    timeseries_df = generate_time_series_df(eviction_df, mortgage_df, tax_df)
    timeseries_df = timeseries_df.merge(evictions_monthly, how="outer")
    timeseries_df.drop_duplicates().to_csv(
        config["timeseries_output_csv_path"], index=False
    )
    logging.info(
        "Output timeseries CSV saved to %s." % config["timeseries_output_csv_path"]
    )

    # Process evictions data--get totals/rates across the analysis period & totals/rates
    # by year
    eviction_df = aggregate_evictions_using_rate_estimates(
        eviction_df,
        config["path_to_eviction_filing_rates"],
        estimate_var = "evictions",
        time_group = "year"
    )
    eviction_years_df = create_year_cols_from_df(
        eviction_df,
        ["evictions", "eviction-filings", "eviction-rate"], # "eviction-filing-rate"
        {"evictions": "total-evictions"},
        "year",
        "GEOID",
    )

    eviction_totals = get_totals_across_years(eviction_df, "GEOID", "evictions").rename(
        columns={"sum": "total-evictions", "mean": "avg-evictions"}
    )
    eviction_filing_totals = get_totals_across_years(
        eviction_df, "GEOID", "eviction-filings",
    ).rename(columns={"sum": "total-eviction-filings", "mean": "avg-eviction-filings"})

    # Process mortgage foreclosures data -- 
    logging.info("Computing mortgage foreclosure rate by tract.")
    mortgage_counts_by_tract = get_counts_by_tract(
        mortgage_df,
        "num_mortgage_foreclosures"
    )

    mortgage_totals = get_totals_across_years(
        mortgage_counts_by_tract, "GEOID", "num_mortgage_foreclosures"
    ).rename(
        columns={"sum": "total-foreclosure-sales", "mean": "avg-foreclosure-sales",}
    )
    mortgage_totals["GEOID"] = mortgage_totals["GEOID"].astype(str)

    # Compute the yearly mortgage data
    mortgage_years_df = create_year_cols_from_df(
        mortgage_counts_by_tract,
        ["num_mortgage_foreclosures"],
        {"num_mortgage_foreclosures": "foreclosure-sales"},
        "year",
        "GEOID",
    )
    mortgage_years_df["GEOID"] = mortgage_years_df["GEOID"].astype(str)

    # Compute the yearly tax lien df
    tax_counts_by_tract = get_counts_by_tract(
        tax_df,
        "num_deeds_issued"

    )
    tax_totals = get_totals_across_years(
        tax_counts_by_tract, "GEOID", "num_deeds_issued"
    ).rename(
        columns={"sum": "total-lien-foreclosures", "mean": "avg-lien-foreclosures",}
    )

    # Compute the yearly tax foreclosures data
    tax_years_df = create_year_cols_from_df(
        tax_counts_by_tract,
        ["num_deeds_issued"],
        {"num_deeds_issued": "lien-foreclosures"},
        "year",
        "GEOID",
    )

    # Join evictions, mortgage, tax, and ACS data together into a single dataframe
    merged = (
        census_df
        .merge(eviction_totals, on="GEOID", how="left")
        .merge(mortgage_totals, on="GEOID", how="left")
        .merge(tax_totals, on="GEOID", how="left")
        .merge(eviction_df[["GEOID"]].dropna().drop_duplicates(),on="GEOID",how="left",)
        .merge(eviction_years_df, on="GEOID", how="left")
        .merge(mortgage_years_df, on="GEOID", how="left")
        .merge(tax_years_df, on="GEOID", how="left")
        )

    # Add yearly rates
    merged = add_yearly_rates_to_merged_df(
        merged,
        {"foreclosure-sales": "foreclosure-rate"},
        "total-owner-occupied-households-mortgage",
    ).drop("total-foreclosure-rate", axis=1)
    merged = add_yearly_rates_to_merged_df(
        merged,
        {"lien-foreclosures": "lien-foreclosure-rate"},
        "total-owner-occupied-households",
    ).drop("total-lien-foreclosure-rate", axis=1)

    # Add housing loss index
    merged = add_housing_loss_index(
        merged, eviction_df, mortgage_counts_by_tract, "year",
    )

    # Add geographic identifier columns
    merged = merged.rename(columns={"GEOID": "census_tract_GEOID"})
    merged["county_GEOID"] = merged["census_tract_GEOID"].apply(lambda x: x[:5])
    merged["county"] = "Hillsborough County"
    merged["state"] = "Florida"


    # Write main output file to CSV
    merged.drop_duplicates().to_csv(config["output_csv_path"], index=False)
    logging.info("Output CSV saved to %s." % config["output_csv_path"])


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
    )
    main()

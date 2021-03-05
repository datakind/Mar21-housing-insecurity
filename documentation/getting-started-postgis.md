# Getting Started With PostGIS

This document discusses how to access a PostgreSQL/PostGIS instance that's been setup for this weekend's project.

[PostGIS](https://postgis.net) is an extension for PostgreSQL that allows for a wide array of geospatial processing fuctions including distance functions, polygon simplification, point-in-polygon, and spatial joins. [Here](https://www.azavea.com/blog/2018/10/11/creating-leaflet-tiles-from-open-data/) is a great discussion of how Azavea used QGIS and PostGIS in tandem to analyze millions of building footprints.

This may be a good place to start if you're familiar with analyzing data in SQL, writing queries, or working with geospatial data in Tableau or QGIS. There are many other UI-based tools that allow you to view and query PostGIS databases. If you don't already have a favorite, I'd recommend starting with [DBeaver](https://dbeaver.io), which offers an interactive mapping panel when you're querying spatial databases.

Please refer to this [workshop](https://postgis.net/workshops/postgis-intro/) from the PostGIS Docs for a great primer on common geospatial operations (Code examples in R + general examples/theory).

## Accessing the DB

Depending on the tool that you're using the DB connection process may be quite different.

Regardless of tool, to connect to this DB you'll need a username (`diver`), dbname (`flh`), hostname (Please Ask), and password (Please Ask). If you post in `#proj-housing-insecurity` one of the Project Ambassadors should be able to provide this information.

The shared role for all volunteers has read access to several schemas. See below:

| schema | content | permissions |
| --- | ---- | ---- |
|geo | geospatial and geocoded data from the project rpeo | read-only |
|public| Any intermediate results |read and write|

You'll have the ability to query the `geo` schema, and read and write access to the `exp` and `public` schemas, where you may persist any intermediate tables or results.

A good first query to test that you're connected properly might be something like the following, a spatial join that displays all evictions in a given area.

```sql
select id, geom
    from (
        -- Select a Tract
        select * from geo.nyc_2010_tracts limit 1
    ) g,
    geo.nyc_evictions ne -- And Intersect Geometries from Tracts and Evictions w. ST_INTERSECTS()
where st_intersects(
    g.wkb_geometry,
    ne.geom
);
```

## What's available on the DB

So far the following tables have been loaded to the PostGIS instance, the remaining local files may need some additional cleaning before upload.

### Completed

| Repo filepath | Database Table | Status | Geometry Column Name |
| ---- | ---- | ---- | ---- |
| ./geo/florida_sdist_2021.zip | geo.fl_sdist_2021 | :white_check_mark: | wkb_geometry |
| ./geo/florida_usdist_2021.zip | geo.fl_usdist_2021 | :white_check_mark: | wkb_geometry |
| ./geo/hillsborough_fl_2010_tracts_formatted.geojson | geo.hboro_2010_tracts | :white_check_mark: | wkb_geometry |
| ./geo/nyc_2010_tracts_formatted.geojson | geo.nyc_2010_tracts | :white_check_mark: | wkb_geometry |
| ./geo/nyc_school_districts.geojson | geo.nyc_districts | :white_check_mark: | wkb_geometry |
| ./raw/nyc_evictions.csv | geo.nyc_evictions | :white_check_mark: | geom |
| ./raw/hillsborough_county_tax_liens.csv | geo.hillsborough_liens | :white_check_mark: | geom |

### Pending

- [ ] hillsborough_county_evictions_geocoded.csv
- [ ] hillsborough_county_mortgage_foreclosures_geocoded.csv

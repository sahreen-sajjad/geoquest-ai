from mcp.server.fastmcp import FastMCP
import random
from countryinfo import CountryInfo, all_countries

mcp = FastMCP("GeoQuest Geography")


@mcp.tool()
def get_country_info(country: str) -> dict:
    """Retrieve geographical information about a country."""

    info = CountryInfo(country)

    return {
        "name": info.name(),
        "capital": info.capital(),
        "region": info.region(),
        "languages": info.languages(),
        "latlng": info.latlng()
    }


@mcp.tool()
def get_street_view_url(lat: float, lon: float) -> str:
    """Generate a Google Street View link for coordinates."""

    return (
        "https://www.google.com/maps/@"
        f"?api=1&map_action=pano&viewpoint={lat},{lon}"
    )

@mcp.tool()
@mcp.tool()
def get_random_country(region: str = "Any") -> dict:
    """Select a random country, optionally filtered by region."""

    countries = all_countries()

    eligible = [
        country
        for country in countries
        if country.name()
        and country.capital()
        and country.region()
        and (
            region.lower() == "any"
            or country.region().lower() == region.lower()
        )
    ]

    if not eligible:
        return {"error": "No matching countries found"}

    country = random.choice(eligible)

    return {
        "name": country.name(),
        "capital": country.capital(),
        "region": country.region(),
        "languages": country.languages(),
        "latlng": country.latlng()
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
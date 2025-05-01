# Parking Meters Data Description

The data comes from [__DataSF__](https://data.sfgov.org/Transportation/Parking-Meters/8vzz-qzz9).

### Important features:

| Column Name | Description | Type |
| --- | --- | --- |
| POST_ID | Unique identifier of meter | Text |
| MS_PAY_STATION_ID || Text |
| MS_SPACE_NUM || Number |
| ON_OFFSTREET_TYPE | Whether the space is on the street or off‐street, e.g. metered parking lot-- OFF Off‐street, ON On‐street | Categorical |
| OSP_ID | Unique identifier of SFMTA‐owned off‐street parking space-- Null - Meter located on‐street, 890 - Pier 48 Lot, 891 - Pier 52 Lot, 892 - Pier 1/2 Motorcycle Lot, 901 - 24th and Capp Lot, 902 - California and Steiner Lot, 903 - 8th and Clement Lot, 904 - 9th and Clement Lot, 905 - Castro Theater Lot, 906 - 18th and Collingwood Lot, 907 - Mission and Norton Lot, 908 - 21st and Geary Lot, 909 - 18th and Geary Lot, 910 - 20th and Irving Lot, 911 - 8th and Irving Lot,913 - 7th and Irving Lot, 914 - Junipero Serra and Ocean Lot, 915 - 19th and Ocean Lot, 916 - Pierce Street Garage, 918 - 24th and Noe Lot, 919 - Felton and San Bruno Lot, 920 - SF General Hospital Lot, 922 - West Portal Lot, 923 - Claremont and Ulloa Lot, 924 - Phelan Loop Lot | Categorical |
| PM_DISTRICT_ID | Parking Management District ID | Number |
| BLOCKFACE_ID | Blockface (side of street) ID | Number |
| METER_TYPE | How many spaces the meter manages-SS - Single‐space, MS - Multi‐space | Categorical |
| CAP_COLOR | Cap color describes the use and restrictions of the meter-- Black - Motorcycle parking, Brown - Tour bus parking, Green - Short term parking, Grey - General metered parking, Purple - Boat trailer parking, Red - Six wheeled commercial vehicle parking, Yellow - Commercial vehicle parking | Categorical |
| OLD_RATE_AREA | Hourly rate zone of the meter; some variations within each zone-- Area 1 - Downtown primarily \$3.50, Area 2 -Surrounding downtown primarily \$3.00, Area 3 -Residential neighborhood primarily \$2.00, Area 5 -SFpark area variable rates ranging from \$0.25 to \$6.00, MC1 -Motorcycle in Area 1 primarily \$0.70, MC2 -Motorcycle in Area 2 primarily \$0.60, MC3 -Motorcycle in Area 3 primarily \$0.40, MC5 -Motorcycle in SFpark area variable rates ranging from \$0.25 to \$6.00, Port 1 -Port‐owned at Fisherman’s Wharf \$2.50,Port 2 -Port‐owned at Fisherman’s Wharf \$2.50, Port 3 -Port‐owned at North Embarcadero \$2.00, Port 4 -Port‐owned at North Embarcadero \$2.00, Port 5 -Port‐owned at Downtown \$3.00, Port 6 -Port‐owned at Downtown \$3.00, Port 7 -Port‐owned at Downtown \$3.00, Port 8 -Port‐owned at Downtown \$3.00, Port 9 -Port‐owned at South Embarcadero \$1.00,Port 10 -Port‐owned at South Embarcadero \$1.00,  Port 11 -Port‐owned at South Embarcadero \$1.00, Port 12 -Port‐owned at South Embarcadero \$1.00, PortMC1 -Port‐owned motorcycle rate \$0.25, PortMC2 -Port‐owned motorcycle rate at Ferry Building \$0.50, Tour Bus - \$9.00 for two hours | Categorical |
| STREET_ID | Street identifier | Number |
| STREET_NAME | Street name | Text |
| STREET_NUM | Approximate street number of meter | Number |
| ORIENTATION || Number |
| LONGITUDE | Longitude of meter | Number |
| LATITUDE | Latitude of meter| Number |
| COLLECTION_ROUTE_DESC || Categorical |
| COLLECTION_SUBROUTE_DESC || Categorical |
| Neighborhoods || Number|
| Analysis Neighborhoods || Number |


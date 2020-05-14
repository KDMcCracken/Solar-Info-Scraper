# Solar-Info-Scraper
Outputs a variety of information regarding solar roof installation such as, cost, increase in home value, hours of useable sunlight, room for panels, etc...

•	Need to download file for the state that the address you are looking at is in from this link. These files are large, so I opted out of sending them with in the project folder.
o	https://github.com/Microsoft/USBuildingFootprints
•	When entering the address on the initial screen, ensure it is formatted without spaces after commas. This was a design decision to reduce necessary tampering with strings.
o	EX: “127 11th Street South,La Crosse,WI 54601”
•	May need to have chromedriver in path… I attached one to project but this can be downloaded from:
o	https://chromedriver.chromium.org/downloads
•	The “building_footprint.py” takes a while to run…. Expect 45-200 seconds before it completes.

This is the interview challenge for a senior full stack python developer role with Carbon Intelligence

### Setup

To set the project up, you will need docker and docker compose installed.

Then, run `$ docker-compose up --build` to build and start the project.

### Usage

To upload files, open localhost:8000/upload/ in your browser.
You can use the data in /data directory.
The data must be uploaded in the following order- building_data.csv, halfhourly_data.csv, meter_data.csv. This is due to foreign key dependencies within the database.

Once this is done, you can browse through the data from localhost:8000/buildings/. From there on in it should be self explanatory!

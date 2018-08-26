ota_insights_scrape.py

Copyright 2018 Paul <paul@Paul-jc>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
 
 


This program is to scrape files from the website OTA Insights in order to process in bulk with the 
intention of concatinating them using my other program OTA-data-compiler.
It will prompt for username and password (input feedback hidden from password).

To use this program change line 153 to your default download location and the desired folder to store 
processed files on line 135.

Future development will include developing a GUI for date and offset as well as including the ability 
to run multiple offsets in one functions. Also dynamicallly select download location and where files 
will be saved once processed.

Later development will also integrate the OTA-data-compiler program into the same GUI for downloading
and processing of all files in one program.

Eventually this will also include a machine learning process and price recommendation facility.

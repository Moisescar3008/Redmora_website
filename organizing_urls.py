import aiohttp, csv, asyncio, json, csv
import pandas as pd
from bs4 import BeautifulSoup
import os

class MexicanStatesScraper:
    def __init__(self, mexican_states):
        self.mexican_states = mexican_states
        self.state_urls_dict = {}
        self.coordinates = {
            'Aguascalientes': [21.896817, -102.289323], 
            'Baja California': [30.256420, -115.117307],
            'Baja California Sur': [25.615943, -111.591458],
            'Campeche': [19.398385, -90.266522],
            'Chiapas': [16.903551, -93.133953],
            'Chihuahua': [29.030790, -106.742140],
            'Coahuila': [27.420884, -102.137957],
            'Colima': [19.120686, -103.938732],
            'Durango': [25.229601, -104.847439],
            'Guanajuato': [21.004562, -101.054656],
            'Guerrero': [17.469087, -99.915571],
            'Hidalgo': [20.529168, -98.929234],
            'Jalisco': [20.354979, -103.807038],
            'Ciudad de México': [19.4326, -99.1332],
            'Estado de México': [19.383855, -99.889495],
            'Michoacán': [19.413327, -101.722531],
            'Morelos': [18.788098, -99.097011],
            'Nayarit': [21.767209, -104.799304],
            'Nuevo León': [25.503357, -99.618053],
            'Oaxaca': [17.062235, -96.612126],
            'Puebla': [19.054902, -98.199071],
            'Queretaro': [20.842591, -99.892720],
            'Quintana Roo': [19.533739, -87.943953],
            'San Luis Potosí': [22.133713, -100.946852],
            'Sinaloa': [24.701605, -107.250186],
            'Sonora': [29.844990, -110.773454],
            'Tabasco': [18.066832, -92.571346],
            'Tamaulipas': [24.635377, -98.160134],
            'Tlaxcala': [19.444296, -98.098624],
            'Veracruz': [19.515917, -96.568607],
            'Yucatán': [20.836305, -89.035138],
            'Zacatecas': [23.051459, -102.894650]
        }

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def check_for_mexican_states(self, session, url_data, Title, Source, Date):
        try:
            async with session.get(url_data['Link'], timeout=30) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    page_text = soup.get_text()
                    found_states = [state for state in self.mexican_states if state.lower() in page_text.lower()]
                    return found_states, Title, url_data['Link'], Source, Date
                else:
                    print(f"Error accessing URL {url_data['Link']}: Status {response.status}")
                    return [], Title, url_data['Link'], Source, Date
        except Exception as e:
            print(f"Error processing URL {url_data['Link']}: {str(e)}")
            return [], Title, url_data['Link'], Source, Date

    async def process_url(self, session, Title, url_data):
        found_states, Title, url, Source, Date = await self.check_for_mexican_states(session, url_data, Title, url_data['Source'], url_data['Date'])

        # Collecting the URLs found per state in the dictionary
        for state in found_states:
            if state not in self.state_urls_dict:
                self.state_urls_dict[state] = []
            self.state_urls_dict[state].append({"Link": url, "Title": Title, "Source": Source, "Date": Date})

    async def process_urls(self, url_data):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=20)) as session:
            tasks = [self.process_url(session, Title, data) for Title, data in url_data.items()]
            await asyncio.gather(*tasks)

    def save_to_dataframe(self):
        df = pd.DataFrame.from_dict(self.state_urls_dict, orient = 'index')
        df.to_csv('archivos/organized_URLs2.csv', encoding='UTF-8')
        #return os.path.join('archivos', 'organized_URLs2.csv')
    
    def to_map(self):
        data = []

        with open(f'archivos/organized_URLs2.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            for row in csv_reader:
                state = row[0]  # Get the Mexican state
                num_elements = sum(1 for cell in row[1:] if cell.strip())  # Count non-empty elements in the row, excluding the first column
                if state in self.coordinates:
                    data.append([*self.coordinates[state], num_elements])  # Append data tuple to the list

        return data
    
    def to_json(self, csv_filename, json_filename):
        json_data = {}
        with open(csv_filename, mode='r', newline='', encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                for cell_value in row:
                    if cell_value:  # Check if cell is not empty
                        try:
                            json_obj = json.loads(cell_value.replace("'", '"'))
                            title = json_obj['Title']
                            del json_obj['Title']
                            states = self.get_states_for_news(json_obj)
                            json_obj['State'] = states
                            json_data[title] = json_obj
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON: {e}")
                            continue  # Skip to the next cell if JSON parsing fails

        # Write the JSON data to a file
        with open(json_filename, mode='w', encoding='UTF-8') as jsonfile:
            json.dump(json_data, jsonfile, indent=4)


    def get_states_for_news(self, news_obj):
        states = []
        for state, urls in self.state_urls_dict.items():
            for url_info in urls:
                if url_info["Link"] == news_obj["Link"]:
                    states.append(state)
        return states
    
async def states():
    try:
        # Verificar si el archivo existe
        if not os.path.exists('archivos/links.json'):
            print("File links.json not found")
            return []

        # Cargar URLs del archivo JSON
        try:
            with open('archivos/links.json', 'r', encoding='UTF-8') as json_file:
                url_data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

        if not url_data:
            print("No URLs found in JSON file")
            return []
            
        mexican_states = ["Aguascalientes", "Baja California", "Baja California Sur", "Ciudad de México", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Estado de México", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"]

        scraper = MexicanStatesScraper(mexican_states)
        try:
            await scraper.process_urls(url_data)
            scraper.save_to_dataframe()
            result = scraper.to_map()
            scraper.to_json('archivos/organized_URLs2.csv', 'archivos/dict_news.json')
            
            if not result:
                print("No data points generated for map")
                return [[21.284259, -99.417428, 1]]  # Retorna un punto por defecto en México
                
            return result
        except Exception as e:
            print(f"Error processing URLs: {e}")
            return [[21.284259, -99.417428, 1]]  # Retorna un punto por defecto en México
            
    except Exception as e:
        print(f"General error in states(): {e}")
        return [[21.284259, -99.417428, 1]]  # Retorna un punto por defecto en México
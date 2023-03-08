import folium
from datetime import datetime
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow


# Create Class MapWindow to Display map
class MapWindow(QMainWindow):
    def __init__(self,option ,df):
        super().__init__()
        self.setWindowTitle("AquaSpot")
        color = {1:'green',-1:'red'}
        # Create a Folium map with latitude and longitude coordinates
        self.m = folium.Map(location=[48.85, 2.35], width='100%', height='100%', left='0%', top='0%', tiles=None, zoom_start=3)
        folium.TileLayer('openstreetmap').add_to(self.m)
        folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(self.m)
        folium.TileLayer('Stamenwatercolor', attr="Stamen Watercolor").add_to(self.m)
        folium.TileLayer('Stamen Toner', attr="Stamen Toner" ).add_to(self.m)
        folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter").add_to(self.m)
        folium.TileLayer('cartodbpositron').add_to(self.m)
        folium.TileLayer( "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", name='OpenTopoMap', attr='OpenTopoMap' ).add_to( self.m )

        # add layers control over the map
        folium.LayerControl().add_to(self.m)
        for i in range(len(df['mmsi'])):
            df.loc[:,"date_time"]=datetime.fromtimestamp(df['timestamp'][i])
        new = df['date_time'].astype(str).str.split(" ", n=1, expand=True)
        df['date'] = new[:][0]
        df['time'] = new[:][1]
        df['type'] = df['type'].str.lower()
        
        # Plot the Marker 
        for index, row in df.iterrows():
            if((row['speed']<3) and (row['distance_from_shore']>0) and (row['distance_from_port']>0)):
                row['is_fishing']=1
            tooltip = f"<b>MMSI: {row['mmsi']}</b><br>Speed: {row['speed']}<br>Latitude: {row['lat']} <br>Longitude: {row['lon']}<br>Course: {row['course']} <br>Distance_from_shore: {row['distance_from_shore']}<br> Distance_from_port: {row['distance_from_port']}<br> Date :{row['date']}<br> Time:{row['time']} <br> Type: {row['type']}"
            if( option == 1):
                if(row['is_fishing'] == 1):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']],icon="info-sign")).add_to(self.m)
            elif( option == 2):
                if(row['is_fishing'] == -1):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            elif( option == 0):
                folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            elif( option == 3):
                if(row['type'] == "drifting_longlines"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            elif( option == 4):
                if(row['type'] == "fixed_gear"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            elif( option == 5):
                if(row['type'] == "pole_and_line"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            elif( option == 6):
                if(row['type'] == "trollers"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            elif( option == 7):
                if(row['type'] == "purse_seines"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)
            else:
                folium.Marker(location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(self.m)

        # Convert the Folium map to HTML
        self.map_html = self.m._repr_html_()

        # Create a webview widget and set the HTML content to the Folium map HTML
        webview = QWebEngineView()
        webview.setHtml(self.map_html)
        self.setCentralWidget(webview)


    def get_html(self):
        return self.m


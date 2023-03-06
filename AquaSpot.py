from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFileDialog
from pandas import pandas as pd
import folium
from datetime import datetime

class MapWindow(QMainWindow):
    def __init__(self,x,df):
        super().__init__()
        self.setWindowTitle('Folium Map')
        color ={1:'green',-1:'red'}
        # Create a Folium map with latitude and longitude coordinates
        m = folium.Map(location=[48.85, 2.35], tiles=None, zoom_start=3)
        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(m)
        folium.TileLayer('stamenwatercolor', attr="stamenwatercolor").add_to(m)
        folium.TileLayer('stamen Toner', attr="stamen Toner" ).add_to(m)

        # add layers control over the map
        folium.LayerControl().add_to(m)
        for i in range(len(df['mmsi'])):
            df['date_time'][i]=datetime.fromtimestamp(df['timestamp'][i])
        new = df['date_time'].astype(str).str.split(" ", n=1, expand=True)
        df['date'] = new[:][0]
        df['time'] = new[:][1]
        
        for index, row in df.iterrows():
            if((row['speed']<3) and (row['distance_from_shore']>0) and (row['distance_from_port']>0)):
                row['is_fishing']=1
            tooltip = f"<b>MMSI: {row['mmsi']}</b><br>Speed: {row['speed']}<br>Latitude: {row['lat']} <br>Longitude: {row['lon']}<br>Course: {row['course']} <br>Distance_from_shore: {row['distance_from_shore']}<br> Distance_from_port: {row['distance_from_port']}<br> Date :{row['date']}<br> Time:{row['time']} <br> Type: {row['Type']}"
            if(x == 1):
                if(row['is_fishing'] == 1):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            elif(x == 2):
                if(row['is_fishing'] == -1):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            elif( x == 0):
                folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            elif( x == 3):
                if(row['Type'] == "drifting_longlines"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            elif( x == 4):
                if(row['Type'] == "Fixed_gear"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            elif( x == 5):
                if(row['Type'] == "Pole_and_line"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            elif( x == 6):
                if(row['Type'] == "trollers"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            else:
                if(row['Type'] == "purse_seines"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
           

        # Convert the Folium map to HTML
        map_html = m._repr_html_()

        # Create a webview widget and set the HTML content to the Folium map HTML
        webview = QWebEngineView()
        webview.setHtml(map_html)

        self.setCentralWidget(webview)

class SampleWindow(QMainWindow):
    def __init__(self,x,df):
        super().__init__()
        self.setWindowTitle('Sample Window')

        # Create a QVBoxLayout
        layout = QVBoxLayout()
       
        # calling MapWindow Function
        self.map_window = MapWindow(x,df)
        
        # Add map_window to Vertical Layout
        layout.addWidget(self.map_window)
        
        # Create Horizontal Layout 
        self.horizontal_layout1 = QHBoxLayout()


        layout.addLayout(self.horizontal_layout1)
        # Create QHBoxLayout
        self.horizontal_layout2 = QHBoxLayout()
        
        # Add label and button 
        label1 = QLabel("Options")
        button1 = QPushButton("Fishing")
        button2 = QPushButton("Non Fishing")
        button3 = QPushButton("Fishing and Non Fishing")

       
        # Add function to display the map
        button1.clicked.connect(lambda: self.fishing_window())
        button2.clicked.connect(lambda: self.non_fishing_window())
        button3.clicked.connect(lambda: self.both_fishing_non_fishing())
        
        
        #Adding buttons to horizontal layout 
        self.horizontal_layout2.addWidget(label1)
        self.horizontal_layout2.addWidget(button1)
        self.horizontal_layout2.addWidget(button2)
        self.horizontal_layout2.addWidget(button3)

        # Add the horizontal layout to the main layout
        layout.addLayout(self.horizontal_layout2)
        
    
        # Create the horizontal layout and add widgets to it
        horizontal_layout = QHBoxLayout()
        horizontal_layout1 = QHBoxLayout()
        # Add widgets to the horizontal layout
        label = QLabel("Select a map plot")
        
        label0 = QLabel("Vessel Type")
        button5 = QPushButton("Drifting_longlines")
        button6 = QPushButton("Fixed_gear")
        button7 = QPushButton("Pole_and_line")
        button8 = QPushButton("trollers")
        button9 = QPushButton("Purse_seines")

        button5.clicked.connect(lambda: self.drifting_longlines())
        button6.clicked.connect(lambda: self.fixed_gear())
        button7.clicked.connect(lambda: self.pole_and_line())
        button8.clicked.connect(lambda: self.trollers())
        button9.clicked.connect(lambda: self.purse_seiners())

        horizontal_layout.addWidget(label)
        horizontal_layout.addWidget(label0)

        horizontal_layout1.addWidget(button5)
        horizontal_layout1.addWidget(button6)
        horizontal_layout1.addWidget(button7)
        horizontal_layout1.addWidget(button8)
        horizontal_layout1.addWidget(button9)
        # Add the horizontal layout to the main layout
        layout.addLayout(horizontal_layout)
        layout.addLayout(horizontal_layout1)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
    
        

    def fishing_window(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(1,df)
        self.horizontal_layout1.addWidget(self.map_window)
        
        
        
    def non_fishing_window(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(2,df)
        self.horizontal_layout1.addWidget(self.map_window)

    def both_fishing_non_fishing(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(0,df)
        self.horizontal_layout1.addWidget(self.map_window)


if __name__ == '__main__':
    app = QApplication([])
    df = pd.read_csv('Dataset/Dataset.csv')
    df['date_time']=0  
    sample_window = SampleWindow(0,df)
    sample_window.show()
    app.exec()





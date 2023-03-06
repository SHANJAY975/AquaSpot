from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFileDialog,QMessageBox
from pandas import pandas as pd
import folium
from datetime import datetime

# Create Class MapWindow to Display map
class MapWindow(QMainWindow):
    def __init__(self,x,df):
        super().__init__()
        self.setWindowTitle('Folium Map')
        color ={1:'green',-1:'red'}
        # Create a Folium map with latitude and longitude coordinates
        m = folium.Map(location=[48.85, 2.35], width='100%', height='100%', left='0%', top='0%',tiles=None, zoom_start=3)
        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('stamenterrain', attr="stamenterrain").add_to(m)
        folium.TileLayer('Stamenwatercolor', attr="Stamen Watercolor").add_to(m)
        folium.TileLayer('Stamen Toner', attr="Stamen Toner" ).add_to(m)
        folium.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter").add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)

        # add layers control over the map
        folium.LayerControl().add_to(m)
        for i in range(len(df['mmsi'])):
            df.loc[:,"date_time"]=datetime.fromtimestamp(df['timestamp'][i])
        new = df['date_time'].astype(str).str.split(" ", n=1, expand=True)
        df['date'] = new[:][0]
        df['time'] = new[:][1]
        
        # Plot the Marker
        for index, row in df.iterrows():
            if((row['speed']<3) and (row['distance_from_shore']>0) and (row['distance_from_port']>0)):
                row['is_fishing']=1
            tooltip = f"<b>MMSI: {row['mmsi']}</b><br>Speed: {row['speed']}<br>Latitude: {row['lat']} <br>Longitude: {row['lon']}<br>Course: {row['course']} <br>Distance_from_shore: {row['distance_from_shore']}<br> Distance_from_port: {row['distance_from_port']}<br> Date :{row['date']}<br> Time:{row['time']} <br> Type: {row['Type']}"
            
            if(x == 1):
                if(row['is_fishing'] == 1):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']],icon="info-sign")).add_to(m)
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
            elif( x == 7):
                if(row['Type'] == "purse_seines"):
                    folium.Marker(radius=100, location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)
            else:
                folium.Marker(location=[row['lat'], row['lon']], tooltip=tooltip, icon=folium.Icon(color=color[row['is_fishing']], icon="info-sign")).add_to(m)

        # Convert the Folium map to HTML
        map_html = m._repr_html_()

        # Create a webview widget and set the HTML content to the Folium map HTML
        webview = QWebEngineView()
        webview.setHtml(map_html)

        self.setCentralWidget(webview)

# Create class SampleWindow to Display window
class SampleWindow(QMainWindow):
    def __init__(self,x,df):
        super().__init__()
        self.setWindowTitle('Map Window')

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
        label1 = QLabel("Select View Options")
        button1 = QPushButton("Fishing")
        button2 = QPushButton("Non Fishing")
        button3 = QPushButton("Fishing and Non Fishing")

       
        # Add function to display the map
        button1.clicked.connect(lambda: self.fishing_window())
        button2.clicked.connect(lambda: self.non_fishing_window())
        button3.clicked.connect(lambda: self.both_fishing_and_non_fishing())
        
        
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
        label = QLabel("Vessel Type")
        button5 = QPushButton("Drifting_longlines")
        button6 = QPushButton("Fixed_gear")
        button7 = QPushButton("Pole_and_line")
        button8 = QPushButton("trollers")
        button9 = QPushButton("Purse_seines")
        button10 = QPushButton("ALL Types")
     
        button5.clicked.connect(lambda: self.drifting_longlines())
        button6.clicked.connect(lambda: self.fixed_gear())
        button7.clicked.connect(lambda: self.pole_and_line())
        button8.clicked.connect(lambda: self.trollers())
        button9.clicked.connect(lambda: self.purse_seiners())
        button10.clicked.connect(lambda: self.all_boats())

        # Add Label to the horizontal Layout
        horizontal_layout.addWidget(label)
        
        # Add buttons to the Horizontal Layout
        horizontal_layout1.addWidget(button5)
        horizontal_layout1.addWidget(button6)
        horizontal_layout1.addWidget(button7)
        horizontal_layout1.addWidget(button8)
        horizontal_layout1.addWidget(button9)
        horizontal_layout1.addWidget(button10)

        # Add the horizontal layout to the main layout
        layout.addLayout(horizontal_layout)
        layout.addLayout(horizontal_layout1)
        
        # Create QHBoxLayout to import data
        horizontal_layout0 = QHBoxLayout()
        label2 = QLabel("Click to View your data")
        button0 = QPushButton("Import")
        button0.clicked.connect(lambda: self.import_data())

        # Add widgets to Layout
        horizontal_layout0.addWidget(label2)
        horizontal_layout0.addWidget(button0)

        #Add QHBoxLayout to main Layout
        layout.addLayout(horizontal_layout0)


        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
    # Create drifting_longlines function to Display drifting_longline vessels
    def drifting_longlines(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(3,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create fixed_gear function to Display fixed_gear vessels
    def fixed_gear(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(4,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
    # Create pole_and_line function to Display pole_and_line vessels
    def pole_and_line(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(5,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create trollers function to Display troller vessels
    def trollers(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(6,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create purse_seiners function to Display purse_seiners vessels
    def purse_seiners(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(7,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
    # Create all_boats function to Display All types of Boats
    def all_boats(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(8,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create import_data function to import data from the user
    def import_data(self):
        # open a file dialog to select the data file to import
        message_box = QMessageBox()
        message_box.setWindowTitle("Import CSV")
        message_box.setText("Please select a CSV file to import with Following data mmsi,timestamp,distance_from_shore,distance_from_port,speed,lat,lon,Type ")
        message_box.exec()
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            # save the data to the new file
            data = pd.read_csv(file_path)
            data['date_time']=0
            print(df.head())
            self.map_window.deleteLater()
            self.map_window = MapWindow(0,data)
            self.horizontal_layout1.addWidget(self.map_window)
        
    # Create fishing_window to Display fishing vessels
    def fishing_window(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(1,df)
        self.horizontal_layout1.addWidget(self.map_window)
        
    # Create non_fishing_window to Display non fishing vessels
    def non_fishing_window(self):
        self.map_window.deleteLater()
        self.map_window = MapWindow(2,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
    # Create both_fishing_and_non_fishing function to Display fishing and non fishing vessels
    def both_fishing_and_non_fishing(self):
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

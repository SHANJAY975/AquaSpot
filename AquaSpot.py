from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFileDialog,QMessageBox
import pandas as pd
import folium
from datetime import datetime

# Create Class MapWindow to Display map
class MapWindow(QMainWindow):
    def __init__(self,option ,df):
        super().__init__()
        self.setWindowTitle("Fishing spot")
        color ={1:'green',-1:'red'}
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

# Create class SampleWindow to Display window
class SampleWindow(QMainWindow):
    def __init__( self, option, df ):
        super().__init__()
        self.setWindowTitle('Map Window')
        self.setMinimumSize(1200, 800)


        # Create a QVBoxLayout
        Vertical_main_layout = QVBoxLayout()
       
        # calling MapWindow Function
        self.map_window = MapWindow( option, df )
        
        # Add map_window to Vertical Layout
        Vertical_main_layout.addWidget(self.map_window)
        
        # Create Horizontal Layout 
        self.horizontal_layout1 = QHBoxLayout()


        Vertical_main_layout.addLayout(self.horizontal_layout1)
        # Create QHBoxLayout
        self.horizontal_layout2 = QHBoxLayout()
        
        # Add label and button 
        label_view = QLabel("Select View Options")
        fishing = QPushButton("Fishing")
        fishing.setToolTip("Click to view Fishing Vessels")
        fishing.setToolTipDuration(1000)

        non_fishing = QPushButton("Non Fishing")
        non_fishing.setToolTip("Click to view Non Fishing Vessels")
        non_fishing.setToolTipDuration(1000)

        fishing_and_non_fishing = QPushButton("Fishing and Non Fishing")
        fishing_and_non_fishing.setToolTip("Click to view All Vessels")
        fishing_and_non_fishing.setToolTipDuration(1000)

       
        # Add function to display the map
        fishing.clicked.connect(lambda: self.fishing_window(df))
        non_fishing.clicked.connect(lambda: self.non_fishing_window(df))
        fishing_and_non_fishing.clicked.connect(lambda: self.both_fishing_and_non_fishing(df))
        
        
        #Adding buttons to horizontal layout 
        self.horizontal_layout2.addWidget(label_view)
        self.horizontal_layout2.addWidget(fishing)
        self.horizontal_layout2.addWidget(non_fishing)
        self.horizontal_layout2.addWidget(fishing_and_non_fishing)

        # Add the horizontal layout to the main layout
        Vertical_main_layout.addLayout(self.horizontal_layout2)
        
    
        # Create the horizontal layout and add widgets to it
        horizontal_layout = QHBoxLayout()
        horizontal_layout1 = QHBoxLayout()

        # Add widgets to the horizontal layout
        Vessel_type = QLabel("Vessel Type")
        Drifting_longlines = QPushButton("Drifting_longlines")
        Drifting_longlines.setToolTip("Click to view Drifting_longlines Vessels")
        Drifting_longlines.setToolTipDuration(1000)

        Fixed_gear = QPushButton("Fixed_gear")
        Fixed_gear.setToolTip("Click to view Fixed_gear")
        Fixed_gear.setToolTipDuration(1000)

        Pole_and_line = QPushButton("Pole_and_line")
        Pole_and_line.setToolTip("Click to view Pole_and_line")
        Pole_and_line.setToolTipDuration(1000)
        
        Trollers = QPushButton("trollers")
        Trollers.setToolTip("Click to view trollers")
        Trollers.setToolTipDuration(1000)
        
        Purse_seines = QPushButton("Purse_seines")
        Purse_seines.setToolTip("Click to view Purse_seines")
        Purse_seines.setToolTipDuration(1000)
        
        All_vessels = QPushButton("ALL Types")
        All_vessels.setToolTip("Click to view All types of Vessels")
        All_vessels.setToolTipDuration(1000)

        Drifting_longlines.clicked.connect(lambda: self.drifting_longlines(df))
        Fixed_gear.clicked.connect(lambda: self.fixed_gear(df))
        Pole_and_line.clicked.connect(lambda: self.pole_and_line(df))
        Trollers.clicked.connect(lambda: self.trollers(df))
        Purse_seines.clicked.connect(lambda: self.purse_seiners(df))
        All_vessels.clicked.connect(lambda: self.all_boats(df))

        # Add Label to the horizontal Layout
        # Add stretchable space to left side of button
        horizontal_layout.addStretch(1)  
        horizontal_layout.addWidget(Vessel_type)
        horizontal_layout.addStretch(1)
        
        
        # Add buttons to the Horizontal Layout
        horizontal_layout1.addWidget(Drifting_longlines)
        horizontal_layout1.addWidget(Fixed_gear)
        horizontal_layout1.addWidget(Pole_and_line)
        horizontal_layout1.addWidget(Trollers)
        horizontal_layout1.addWidget(Purse_seines)
        horizontal_layout1.addWidget(All_vessels)

        # Add the horizontal layout to the main layout
        Vertical_main_layout.addLayout(horizontal_layout)
        Vertical_main_layout.addLayout(horizontal_layout1)
        
        # Create QHBoxLayout to import data
        horizontal_layout0 = QHBoxLayout()
        View_data = QLabel("Click to View your data")
        Import = QPushButton("Import")
       

        Import.clicked.connect(lambda: self.import_data(df))
        

        # Add widgets to Layout
        horizontal_layout0.addWidget(View_data)
        horizontal_layout0.addWidget(Import)
        

        #Add QHBoxLayout to main Layout
        Vertical_main_layout.addLayout(horizontal_layout0)


        central_widget = QWidget()
        central_widget.setLayout(Vertical_main_layout)

        self.setCentralWidget(central_widget)
    # Create drifting_longlines function to Display drifting_longline vessels
    def drifting_longlines(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(3,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create fixed_gear function to Display fixed_gear vessels
    def fixed_gear(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(4,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
    # Create pole_and_line function to Display pole_and_line vessels
    def pole_and_line(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(5,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create trollers function to Display troller vessels
    def trollers(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(6,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create purse_seiners function to Display purse_seiners vessels
    def purse_seiners(self, df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(7,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
    # Create all_boats function to Display All types of Boats
    def all_boats(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(8,df)
        self.horizontal_layout1.addWidget(self.map_window)

    # Create import_data function to import data from the user
    def import_data(self,df):
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
            df = pd.read_csv(file_path)
            df['date_time']=0
            df.columns = df.columns.str.lower()
            df.columns = df.columns.str.replace(" ","_")
            
            if not('mmsi' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file with mmsi ")
                message_box1.exec()
            elif not('timestamp' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with timestamp")
                message_box1.exec()
            elif not('distance_from_shore'):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with distance_from_shore ")
                message_box1.exec()
            elif not('distance_from_port' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with distance_from_port")
                message_box1.exec()
            elif not('speed' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with speed ")
                message_box1.exec()
            elif not('lat' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with lat ")
                message_box1.exec()
            elif not('lon' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with Following data lon ")
                message_box1.exec()
            elif not('type' in df.columns):
                message_box1 = QMessageBox()
                message_box1.setWindowTitle("Import CSV")
                message_box1.setText("Please select a CSV file to import with Type ")
                message_box1.exec()
            else:  
                print(df.head())
                sample_window.close()
                sample_window1 = SampleWindow(0,df)
                sample_window1.show()  
        
    # Create fishing_window to Display fishing vessels
    def fishing_window(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(1,df)
        self.horizontal_layout1.addWidget(self.map_window)
        
    # Create non_fishing_window to Display non fishing vessels
    def non_fishing_window(self,df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(2,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
    # Create both_fishing_and_non_fishing function to Display fishing and non fishing vessels
    def both_fishing_and_non_fishing(self, df):
        self.map_window.deleteLater()
        self.map_window = MapWindow(0,df)
        self.horizontal_layout1.addWidget(self.map_window)
    
if __name__ == '__main__':
    app = QApplication([]) 
    df = pd.read_csv('Dataset/Dataset.csv')
    df['date_time']=0 
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(" ","_")
    sample_window = SampleWindow(0,df)
    sample_window.show()
    app.exec()

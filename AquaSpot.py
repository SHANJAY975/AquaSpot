
from PySide6.QtWidgets import QMainWindow,  QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFileDialog,QMessageBox
import pandas as pd
from Mapwindow import MapWindow
from PySide6.QtWidgets import QApplication

# Create class SampleWindow to Display window
class Main_window(QMainWindow):
    def __init__( self, option, df ):
        super().__init__()
        self.setWindowTitle('AquaSpot')
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
        Download = QPushButton("Download plot")

        Import.clicked.connect(lambda: self.import_data(df))
        Download.clicked.connect(lambda: self.download())

        # Add widgets to Layout
        horizontal_layout0.addWidget(View_data)
        horizontal_layout0.addWidget(Import)
        horizontal_layout0.addWidget(Download)

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
                sample_window.deleteLater()
                sample_window1 = Main_window(0,df)
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
    
    # Create download method to download the map plot
    def download(self):

        # Open file dialog to select file path and name
        self.map_html = self.map_window.get_html()
        self.horizontal_layout1.addWidget(self.map_window)
        
        options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save map plot", "", "HTML Files (*.html)", options=options)
        
        # Add .html extension if not already included
        if not file_name.endswith('.html'):
            file_name += '.html'
        
        # Save map plot to file
        self.map_html.save(file_name)
        message_box2 = QMessageBox()
        message_box2.setWindowTitle("Download")
        message_box2.setText("Current map window is downloaded")
        message_box2.exec()
if __name__ == '__main__':
        app = QApplication([]) 
        df = pd.read_csv('Dataset/Dataset.csv')
        df['date_time']=0 
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(" ","_")
        sample_window = Main_window(0,df)
        sample_window.show()
        app.exec()
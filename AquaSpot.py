
from PySide6.QtWidgets import QMainWindow,  QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFileDialog,QMessageBox, QComboBox
import pandas as pd
from Mapwindow import MapWindow
from PySide6.QtWidgets import QApplication

# Create class SampleWindow to Display window
class Main_window(QMainWindow):
    def __init__( self, option, df ):
        super().__init__()
        self.setWindowTitle('AquaSpot')
        self.setMinimumSize(1200, 800)

        self.df = df
        # Create a QVBoxLayout
        Vertical_main_layout = QVBoxLayout()
       
        # calling MapWindow Function
        self.map_window = MapWindow(option, df)
        
        # Add map_window to Vertical Layout
        Vertical_main_layout.addWidget(self.map_window)
        
        # Create Horizontal Layout 
        self.horizontal_layout1 = QHBoxLayout()
        Vertical_main_layout.addLayout(self.horizontal_layout1)

         # Create QHBoxLayout for Label and Button 
        label_and_button_layout = QHBoxLayout()
        
        # Create QVBoxLayout for Adding Labels
        label_layout = QVBoxLayout()

        # Add QLabel for Description
        description_label = QLabel("Select View Options")
        view_label = QLabel("Vessel Type")
        View_data = QLabel("Click to View your data")
        
        # Add Labels to label_layout
        label_layout.addWidget(description_label)
        label_layout.addWidget(view_label)
        label_layout.addWidget(View_data)
        
        # Add label_layout to label_and_button_layout
        label_and_button_layout.addLayout(label_layout)
        
        # Create QVBoxLayout for adding Buttons
        button_layout = QVBoxLayout()
        
        # Create QHBoxLayout for adding Buttons
        fishing_info_layout = QHBoxLayout()
        
        # Create QPushButton 
        fishing = QPushButton("Fishing")
        non_fishing = QPushButton("Non Fishing")
        fishing_and_non_fishing = QPushButton("Fishing and Non Fishing")

        # Add function to display the map
        fishing.clicked.connect(lambda: self.fishing_window(df))
        non_fishing.clicked.connect(lambda: self.non_fishing_window(df))
        fishing_and_non_fishing.clicked.connect(lambda: self.both_fishing_and_non_fishing(df))
        
        # Add Wigets to fishing_info_layout
        fishing_info_layout.addWidget(fishing)
        fishing_info_layout.addWidget(non_fishing)       
        fishing_info_layout.addWidget(fishing_and_non_fishing)
 
        # Add fishing_info_layout to button_layout
        button_layout.addLayout(fishing_info_layout)
        
        # Create QHBoxLayout for adding Vessel type options
        Vessel_type_layout = QHBoxLayout()

        # Create QComboBox to add Vessel types
        Vessel_type = QComboBox()

        # Add Types of Vessel to Vessel_type ComboBox
        Vessel_type.addItems([ "Drifting_longlines", "Fixed_gear", "Pole_and_line", "trollers", "Purse_seines", "All_Vessels" ])

        # The default signal from currentIndexChanged sends the index
        Vessel_type.currentIndexChanged.connect(self.index_changed)
        
        # Add Wiget to Vessel_type_layout
        Vessel_type_layout.addWidget(Vessel_type)

        # Add Vessel_type_layout to button_layout
        button_layout.addLayout(Vessel_type_layout)
       

        # Create QHBoxLayout for adding import and download buttons
        import_and_download_layout = QHBoxLayout()
        
        # Create QPushbutton for import and Download button
        Import = QPushButton("Import")
        Download = QPushButton("Download plot")
        
        # Call methods to import and Download 
        Import.clicked.connect(lambda: self.import_data())
        Download.clicked.connect(lambda: self.download())

        # Add Widgets to import_and_download_layout 
        import_and_download_layout.addWidget(Import)
        import_and_download_layout.addWidget(Download)
        
        # Add import_and_download_layout to button_layout 
        button_layout.addLayout(import_and_download_layout)

        # Add button_layout to label_and_button_layout
        label_and_button_layout.addLayout(button_layout)

        # Add label_and_button_layout to Vertical_main_layout
        Vertical_main_layout.addLayout(label_and_button_layout)

        # Create QWidget
        central_widget = QWidget()

        # Set Main layout to Widget
        central_widget.setLayout(Vertical_main_layout)
        self.setCentralWidget(central_widget)
 
    # Create index_changed method to call vessel type methods
     # i is an int
    def index_changed(self, i):
        if (i == 0):
            self.drifting_longlines(self.df)
        elif ( i == 1):
            self.fixed_gear(self.df)
        elif ( i == 2):
            self.pole_and_line(self.df)
        elif ( i == 3):
            self.trollers(self.df)
        elif ( i == 4):
            self.purse_seiners(self.df)
        else:
            self.all_boats(self.df)


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
                sample_window1 = Main_window(0, df)
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
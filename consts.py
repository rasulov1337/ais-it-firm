DB_HOST_NAME = 'localhost'
DB_PORT = 5555
DB_NAME = 'it-firm'
DB_USERNAME = 'postgres'
DB_PASSWORD = '1'

DATE_FORMAT = 'yyyy-MM-dd'


STYLESHEET = """
QWidget {
	background: #262626;
	color: white;
	selection-background-color: #2cde85;
	selection-color: black;
}


QPushButton {
	border-radius: 5px;
	border: 1px solid white;
	color: white;
	min-width: 85px;
	min-height: 25px;
}

QPushButton#next_btn, #prev_btn {
		min-width: 60px;
}

QPushButton::hover {
	background: #2cde85;	
	color: black;
	border: none;

}

QFrame#frame {
	/*background-color: white;*/
	border: 1px solid white;
}


QLineEdit {
	min-height: 20px;
	border: 1px solid white;
}

QHeaderView::section {
	background-color: black;
	color: white;
}

QComboBox {
	color: white;
	border: 1px solid white;
}

QDateEdit {
	border: 1px solid white;
}
"""
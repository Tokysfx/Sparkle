def stylesheet (widget):

    widget.setStyleSheet("""
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QWidget {
                    background-color: #2b2b2b;
                    color: white;
                }
                QLabel {
                    color: white;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #db7515;
                    color: white;
                    border: 1px solid #db7515;
                    padding: 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #303030;
                }
                QPushButton:focus {
                    outline: none;
                    border: 1px solid #db7515;
                }
                QListWidget {
                    background-color: #3a3a3a;
                    color: white;
                    border: 1px solid #555;
                    padding: 5px;
                    outline: none;
                    show-decoration-selected: 0;
                }

                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #555;
                    outline: none;
                }

                QListWidget::item:selected {
                    background-color: #505050;
                }

                QListWidget::item:hover {
                    background-color: #404040;
                }
                QLineEdit {
                    background-color: #3a3a3a;
                    color: white;
                    border: 2px solid #555555;
                    padding: 2px;
                    border-radius: 6px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border-color: #db7515;
                    background-color: #404040;
                }
                QLineEdit:hover {
                    border-color: #666666;
                }
                QTreeWidget {
                    background-color: #3a3a3a;
                    color: white;
                    border: 1px solid #555;
                    font-size: 12px;
                    outline: none;
                    show-decoration-selected: 0;
                }
                QTreeWidget::item {
                    padding: 4px;
                    height: 20px;
                    outline: none;
                }
                QTreeWidget::item:selected {
                    background-color: #505050;
                }
                QTreeWidget::item:hover {
                    background-color: #404040;
                }
                QTreeWidget::item:focus {
                    outline: none;
                }
                QTreeWidget QHeaderView::section {
                    background-color: #db7515;
                    color: white;
                    padding: 6px;
                    border: none;
                    font-weight: bold;
                }
            """)
"""
Connection Indicator Widget

Visual connection status indicator for the Sparkle 3D Pipeline Management System.
Provides real-time feedback on server connectivity with professional iconography
and clear status messaging.

Features:
- Visual status icons for different connection states
- Color-coded status text with tooltips
- Professional styling with rounded corners
- Real-time status updates via signal connections
"""

from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ConnectionIndicator(QWidget):
    """
    Professional connection status indicator widget.
    
    Displays current server connection state with visual feedback including
    status icons, color-coded text, and informative tooltips.
    """
    
    def __init__(self):
        """
        Initialize the connection indicator widget.
        """
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """
        Initialize the user interface components.
        
        Creates the layout with status icon and text, applies styling,
        and sets initial state.
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
        # Status icon label
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(20, 20)
        self.status_icon.setAlignment(Qt.AlignCenter)
        
        # Configure font for icons/emojis
        icon_font = QFont()
        icon_font.setPointSize(16)
        self.status_icon.setFont(icon_font)
        
        # Status text label
        self.status_text = QLabel("Initializing...")
        self.status_text.setStyleSheet("color: #cccccc; font-size: 12px;")
        
        layout.addWidget(self.status_icon)
        layout.addWidget(self.status_text)
        
        self.setLayout(layout)
        self.setFixedHeight(30)
        
        # Apply professional widget styling
        self.setStyleSheet("""
            ConnectionIndicator {
                background-color: rgba(43, 43, 43, 100);
                border-radius: 8px;
                border: 1px solid #555555;
            }
        """)
        
        # Set initial status
        self.set_status("checking")
    
    def set_status(self, status):
        """
        Update the connection status display.
        
        Updates the visual elements (icon, text, color, tooltip) based on the
        provided connection status.
        
        Args:
            status (str): Connection status ('connected', 'disconnected', 'checking', 'error')
        """
        if status == "connected":
            # Server mode: Connected and collaborative
            self.status_icon.setText("🌐")
            self.status_text.setText("Collaborative")
            self.status_text.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold;")
            self.setToolTip("🌐 Collaborative Mode\n• Server connected\n• Auto-refresh (15s)\n• Team collaboration active")
            
        elif status == "disconnected":
            # Local mode: Server unavailable
            self.status_icon.setText("💻")
            self.status_text.setText("Local")
            self.status_text.setStyleSheet("color: #FF9800; font-size: 12px; font-weight: bold;")
            self.setToolTip("💻 Local Mode\n• Server unavailable\n• Offline work\n• Manual refresh only")
            
        elif status == "checking":
            # Verification in progress
            self.status_icon.setText("⚠️")
            self.status_text.setText("Checking...")
            self.status_text.setStyleSheet("color: #FFC107; font-size: 12px; font-style: italic;")
            self.setToolTip("⚠️ Connection Check\n• Testing server connectivity...")
            
        elif status == "error":
            # Connection error state
            self.status_icon.setText("❌")
            self.status_text.setText("Error")
            self.status_text.setStyleSheet("color: #F44336; font-size: 12px; font-weight: bold;")
            self.setToolTip("❌ Connection Error\n• Network problem\n• Check server configuration")
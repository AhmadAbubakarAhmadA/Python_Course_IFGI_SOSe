# Wikipedia_Excercise
# Python action to open QWebView with the district’s Wikipedia page
from qgis.PyQt.QtCore      import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# Create a browser widget to show the Wikipedia page
view = QWebView()

# Build the URL using the “Name” attribute of each feature:
#   [% "Name" %] is like the  QGIS’s placeholder for the field “Name”.
url_str = 'https://en.wikipedia.org/wiki/' + '[% "Name" %]'
view.load(QUrl(url_str))

# Show the popup window
view.show()

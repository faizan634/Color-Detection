import cv2
import pandas as pd

# Manually define the image path for Jupyter environment instead of argparse
img_path = 'colorpic.jpg'

# Reading image with OpenCV
img = cv2.imread(img_path)

# Reading CSV file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Initialize global variables for clicked event
clicked = False
r = g = b = xpos = ypos = 0

# Function to get color name based on the closest match in the CSV
def getColorName(R, G, B):
    minimum = 10000
    cname = ''
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse callback function
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:  # On double-click
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Create a window and set a mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

# Main loop to display the image
while True:
    cv2.imshow("image", img)
    
    if clicked:
        # Draw a rectangle with the selected color
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        
        # Display the color name and RGB values
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        # For very light colors, display the text in black instead of white
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        
        clicked = False

    # Break the loop when the user hits the 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Destroy all OpenCV windows
cv2.destroyAllWindows()

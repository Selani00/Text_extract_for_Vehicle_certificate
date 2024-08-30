import cv2
import difflib
import numpy as np

# Define the coordinates for each box (x, y, width, height)
boxes = [
    (20, 105, 170, 30),   # Registration No
    (450, 105, 250, 30),  # Chassis No
    (20, 190, 600, 55),   # Current Owner and Address
    (25, 265, 150, 40),   # Special Notes
    (20, 510, 400, 55),   # Absolute Owner
    (15, 583, 250, 20),   # Engine No.
    (460, 583, 250, 20),  # Cylinder Capacity.
    (15, 623, 250, 20),   # Class of Vehicle
    (460, 623, 250, 20),  # Taxation class
    (15, 659, 250, 20),   # Status when Registered
    (460, 658, 250, 20),  # Fuel Type
    (15, 695, 250, 20),   # Make
    (460, 695, 250, 20),  # Country of Origin
    (15, 733, 250, 20),   # Model
    (460, 733, 250, 20),  # Manufacture Description
    (15, 773, 250, 20),   # Wheel Base
    (460, 773, 250, 20),  # Over Hang
    (15, 813, 250, 20),   # Type of Body
    (460, 813, 250, 20),  # Year of Manufacture
    (15, 850, 250, 20),   # Color
    (460, 850, 400, 350), # Previous Owners
    (15, 882, 250, 20),   # seatingCapacity
    (200, 923, 100, 20),  # unladenWeight
    (270, 923, 100, 20),  # grossWeight
    (200, 970, 250, 20),  # Tyre Size   
    (15, 1050, 250, 20),  # provincialCouncil
    (15, 1090, 250, 20),  # dateOfFirstRegistration
    (15, 1125, 250, 20),  # taxesPayable    
]

labels = [
    'Registration No',
    'Chassis No',
    'Current Owner and Address',
    'Special Notes',
    'Absolute Owner',
    'Engine No.',
    'Cylinder Capacity',
    'Class of Vehicle',
    'Taxation class',
    'Status when Registered',
    'Fuel Type',
    'Make',
    'Country of Origin',
    'Model',
    'Manufacture Description',
    'Wheel Base',
    'Over Hang',
    'Type of Body',
    'Year of Manufacture',
    'Color',
    'Previous Owners',
    'seatingCapacity',
    'unladenWeight',
    'grossWeight',
    'Tyre Size',
    'provincialCouncil',
    'dateOfFirstRegistration',
    'taxesPayable'
]

# Lists of possible words for specific fields
word_lists = {
    "Class of Vehicle": ["Motor Car", "Motor Cycle", "Motor Lorry", "Motor Coach", "Dual Purpose Vehicle"],
    "Taxation class": ["Private Car", "Motor Cycle", "Three-Wheeler", "Dual Purpose Vehicle", "Heavy Goods Vehicle"],
    "Manufacture Description" : ["Private Car", "Motor Cycle", "Three-Wheeler", "Dual Purpose Vehicle", "Heavy Goods Vehicle"],
    "Status when Registered": ["Brand New", "Suspended", "Cancelled", "Transferred", "Pending", "De-registered", "Expired"],
    "Fuel Type": ["Petrol", "Diesel", "Electric", "Hybrid", "LPG"],
    "Make": ["HERO", "Toyota", "Honda", "Nissan", "Suzuki", "Hyundai"],
    "Country of Origin": ["India", "Japan", "Germany", "South Korea", "USA", "UK", "Italy", "France", "China"],
    "Type of Body": ["Open", "Sedan", "Hatchback", "SUV", "Coupe"],
    "Year of Manufacture": ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"],
    "Color": ["Red", "Sport red black", "Blue", "Green", "Yellow", "Black", "White", "Grey", "Brown", "Orange"],
    "provincialCouncil": ["Western", "Central", "Southern", "Northern", "Eastern", "North-Western", "North-Central", "Uva", "Sabaragamuwa"],
    "Special Notes": ["Original"]
}

def correct_word_ignore_case(word, possibilities):
    word_lower = word.lower()
    possibilities_lower = [possible_word.lower() for possible_word in possibilities]
    matches = difflib.get_close_matches(word_lower, possibilities_lower, n=1, cutoff=0.6)
    
    if matches:
        # Find the original case-sensitive word from the possibilities list
        original_word = possibilities[possibilities_lower.index(matches[0])]
        return original_word
    return None

def calculate_visibility(image):
    """
    Calculate a visibility score based on contrast and brightness.
    Higher values indicate better visibility.
    """
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the mean brightness
    brightness = np.mean(gray_image)

    # Calculate the standard deviation of pixel values (contrast)
    contrast = np.std(gray_image)

    # Normalize brightness and contrast to be between 0 and 1
    brightness_score = brightness / 255.0
    contrast_score = contrast / 128.0  # Using 128 as the midpoint of the std range

    # Calculate visibility as a weighted sum of brightness and contrast
    visibility = (0.5 * brightness_score) + (0.5 * contrast_score)

    # Convert to percentage
    visibility_percentage = visibility * 100

    return visibility_percentage

from PIL import Image
import math
from random import shuffle
from math import sqrt, log
image = Image.open("TokyoPanoramaShredded.png")
data = image.getdata() # This gets pixel data

def unshred_image():

    column_edges = get_column_edges()

    initial_column = column_edges[10]

    column_edges.remove(initial_column)

    matched_columns = find_column_matches([initial_column], column_edges)

    NUMBER_OF_COLUMNS = 20

    unshredded = Image.new("RGBA", [620, 359])

    for i, column in enumerate(matched_columns):

        shred_width = unshredded.size[0]/NUMBER_OF_COLUMNS
        width, height = image.size

        destination_point = (i * shred_width, 0)
        source_region = image.crop((column.right_edge, 0, column.left_edge, height))
        unshredded.paste(source_region, destination_point)

    unshredded.save("unshredded.png")

    for column in matched_columns:
        print(str(column.right_edge) + " " + str(column.left_edge))


        
def find_column_matches(matched_columns, column_edges):

    if len(matched_columns) == 20:
        return matched_columns

    left_column = matched_columns[0]
    right_column = matched_columns[len(matched_columns) - 1]

    left_match = None

    if not left_column.left_matched:
        left_match = right_column.find_left_match(column_edges)

    if left_match is not None:
        left_match.left_matched = True
        matched_columns.append(left_match)
        column_edges.remove(left_match)

    right_match = None

    if not right_column.right_matched:
        right_match = left_column.find_right_match(column_edges)

    if right_match is not None:
        right_match.right_matched = True
        matched_columns.insert(0, right_match)
        column_edges.remove(right_match)

    if right_match is None and left_match is None:
        print("Could not find a match")

    return find_column_matches(matched_columns, column_edges)

class Column:
    right_matched = False
    left_matched = False
    
    def __init__(self, right_edge, left_edge, right_edge_data, left_edge_data):
        self.right_edge = right_edge
        self.left_edge = left_edge
        self.right_edge_data = right_edge_data
        self.left_edge_data = left_edge_data

    def find_right_match(self, columns):
        best_column = None
        best_match = 30000
        for column in columns:
            match = self.match_column(column.left_edge_data, self.right_edge_data)
            if match < best_match and math.fabs(self.right_edge - column.left_edge) != 31:
                best_match = match
                best_column =  column

        return best_column

    def find_left_match(self, columns):
        best_column = None
        best_match = 300000
        for column in columns:
            match = self.match_column(column.right_edge_data, self.left_edge_data)
            if match < best_match and math.fabs(self.left_edge - column.right_edge) != 31:
                best_match = match
                best_column =  column

        return best_column

    def match_column(self, edge_data1, edge_data2):
        match_certainty = 0

        for i in range(len(edge_data1)):
            match_certainty += compare_pixels(edge_data1[i], edge_data2[i])

        return match_certainty

def compare_pixels(pixel1, pixel2):
    r_diff = math.fabs(pixel1[0] - pixel2[0])
    g_diff = math.fabs(pixel1[1] - pixel2[1])
    b_diff = math.fabs(pixel1[2] - pixel2[2])
    
    return r_diff + g_diff + b_diff

def get_column_edges():

    right_columns = filter(lambda x: x % 32 == 0, range(641))

    left_columns = map(lambda x: x - 1, right_columns)

    right_columns.remove(640)

    left_columns.remove(-1)
    
    right_column_data = get_columns(right_columns)

    left_column_data = get_columns(left_columns)

    columns = []

    for i in range(20):
        columns.append(Column(right_columns[i], left_columns[i], right_column_data[i], left_column_data[i]))

    return columns

def get_columns(columns):
    array = []
    for x in columns:
        array.append(get_column(x))
    return array

def get_column(x):
    array = []
    for y in range(359):
        array.append(get_pixel_value(x, y))
    return array
            
def get_pixel_value(x,y):
    width, height = image.size
    pixel = data[y * width + x]
    return pixel

unshred_image()

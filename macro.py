white = 0x1C00ff00
black = 0x000

desktop = XSCRIPTCONTEXT.getDesktop() 
doc = desktop.getCurrentComponent()
sheet = doc.Sheets[0]
alive_cells = []

def game_of_life(_):
    global alive_cells
    game_range = 26 #width and height of the board
    
    #calculating the next move
    for x in range(game_range):
        for y in range(game_range):
            algorithm(x, y)
        
    #cleaning the board
    for x in range(game_range):
        for y in range(game_range):
            sheet.getCellByPosition(x, y).CellBackColor = white

    #drawing new cells from alive_cells list
    for x in range(game_range):
        for y in range(game_range):
            if (x,y) in alive_cells:
                sheet.getCellByPosition(x, y).CellBackColor = black

    alive_cells.clear()
            

def algorithm(cell_x, cell_y):
    cell_count = get_neighbour_count(cell_x, cell_y) 
    cell = sheet.getCellByPosition(cell_x, cell_y)
    global alive_cells
    if (cell.CellBackColor == black and 2 <= cell_count <= 3) or (cell.CellBackColor == white and cell_count == 3):
        alive_cells.append((cell_x, cell_y))


def get_neighbour_count(cell_x, cell_y):
    cell_count = 0
    for cell in get_neighbouring_cells(cell_x, cell_y):
        if sheet.getCellByPosition(cell[0], cell[1]).CellBackColor == black:
            cell_count += 1
    return cell_count


def get_neighbouring_cells(cell_x, cell_y):
    neighbors = []
    for x in range(3):
        for y in range(3):
            if (x,y) != (1,1) and cell_x + x - 1 >= 0 and cell_y + y - 1 >= 0:
                neighbors.append((cell_x + x - 1, cell_y + y - 1))
    return neighbors
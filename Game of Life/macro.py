import time
import threading
import uno

white = 0x1C00ff00
black = 0x000

desktop = XSCRIPTCONTEXT.getDesktop() 
doc = desktop.getCurrentComponent()
sheet = doc.Sheets[0]

generation = 0
alive_cells = []

def main(): # nezapomenout na _ parametr (při nastavení jako event)
    t = threading.Thread(target=main_thread)
    t.start()

def main_thread():
    while True:
        if sheet.getCellRangeByName("AB1").String == "":
            game_of_life()
            sheet.getCellRangeByName("AB1").String = "SMAŽTE POLE PRO NOVÉ KOLO"
        time.sleep(0.1)

def game_of_life():
    global alive_cells
    global generation
    game_range = 26 #width and height of the board
    
    #calculating the next move
    for x in range(game_range):
        for y in range(game_range):
            algorithm(x, y)
        
    #cleaning the board
    sheet.getCellRangeByName("A1:Z26").CellBackColor = white

    #drawing new cells from alive_cells list
    for x in range(game_range):
        for y in range(game_range):
            if (x,y) in alive_cells:
                sheet.getCellByPosition(x, y).CellBackColor = black

    generation += 1
    add_to_graph(len(alive_cells))
    alive_cells.clear()

def add_to_graph(alive):
    death = 676
    sheet.getCellRangeByName("AB3").setString(f"Gen: {generation}")
    sheet.getCellByPosition(29 + generation, 0).setValue(alive)
    sheet.getCellByPosition(29 + generation, 1).setValue(death - alive)

    chartCollection = sheet.getCharts()
    chart = chartCollection.getByIndex(0)
    oAddresses = []
    newrange = getCurrentRegion(sheet.getCellByPosition(29,0))
    oAddress = newrange.getRangeAddress()
    oAddresses.append(oAddress)
    chart.setRanges(oAddresses)

def getCurrentRegion(range):
    cursor = range.Spreadsheet.createCursorByRange(range)
    cursor.collapseToCurrentRegion()
    return cursor

def algorithm(cell_x, cell_y):
    cell_count = get_neighbour_count(cell_x, cell_y) 
    cell = sheet.getCellByPosition(cell_x, cell_y)
    global alive_cells
    if (cell.CellBackColor == black and cell_count in (2, 3)) or (cell.CellBackColor != black and cell_count == 3):
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
            if (x,y) != (1,1) and (cell_x + x - 1 >= 0 and cell_y + y - 1 >= 0) and (cell_x + x - 1 <= 25 and cell_y + y - 1 <= 25):
                neighbors.append((cell_x + x - 1, cell_y + y - 1))
    return neighbors



    import time
import threading

white = 0x1C00ff00
black = 0x000

desktop = XSCRIPTCONTEXT.getDesktop() 
doc = desktop.getCurrentComponent()
sheet = doc.Sheets[0]

generation = 0
alive_cells = []

def main(_):
    t = threading.Thread(target=main_thread)
    t.start()

def main_thread():
    while True:
        if sheet.getCellRangeByName("AB1").String == "":
            game_of_life()
            sheet.getCellRangeByName("AB1").String = "SMAŽTE POLE PRO NOVÉ KOLO"
        time.sleep(0.1)

def game_of_life():
    global alive_cells
    global generation
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

    generation += 1
    add_to_graph(len(alive_cells))
    alive_cells.clear()

def add_to_graph(alive):
    death = 676
    sheet.getCellByPosition(29 + generation, 0).setString(generation)
    sheet.getCellByPosition(29 + generation, 1).setString(alive)
    sheet.getCellByPosition(29 + generation, 2).setString(death - alive)

    chart = doc.getCharts().getByIndex(0)
    chart.setDataSourceRange(sheet, sheet.getCellByPosition(29, 0), sheet.getCellByPosition(29 + generation, 2))

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



    

#!/usr/bin/env python3
"""Draw a sankey diagram using data from a given input file.
"""
import random
import sys
from ezgraphics import GraphicsWindow

WIDTH = 1000        # Width of the window in pixels
HEIGHT = 700        # Height of the window in pixels
GAP = 100           # Gap between disagram arrows in pixels
COLOURS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
(245,	130,	48),	(145,	30, 180), (70, 240,	240),	(240, 50, 230),
(210,	245,	60),	(250,	190, 212), (0, 128,	128),	(220, 190, 255),
(170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195),
(128,	128,	0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]

def read_file(file_name):
  try:
    f = open(file_name, "r")
  except FileNotFoundError:
    raise(FileNotFoundError)

  title = f.readline()
  title = title.strip()
  left_axis_label = f.readline()
  left_axis_label = left_axis_label.strip()
  data_list = f.readlines()
  f.close()
  return title, left_axis_label, data_list


def set_up_graph(title):
  graph = GraphicsWindow(WIDTH, HEIGHT)
  graph.setTitle(title)
  return graph

def process_data(data_list) :
    diction={}
    #diction adında dictionary oluşturulur.
    t=1
    #Satır sayısını vermek için t değeri 0 olarak başlatılır.
    for i in data_list:
        try:
            a=i.strip().split(",")
            #liste elemanları ',' den sonra ayrılır ve bir liste oluşturur.
            diction[a[0]]=float(a[1])
            #bu yeni oluşan listenin 0. indexindeki eleman dictionary'in
            #'key' değeri , 1. indexindeki değer de float a çevirilip 'value' değeri olur.
        except ValueError:
            print(f"\nError in line {t}: Value provided is not a number (as363)")
            raise(ValueError)
        t+=1
    return diction


def draw_sankey(window, title, data_dic, gap_size, border_size=100):
    lenght=len(data_dic)
    #process_data fonksiyonunda oluşturulan dictionary in boyutunu lenght değişkenine atadık.

    canvas=window.canvas()
    #yazı ve şekil eklemek için canvas değişkeni başlattık.

    diagram_width=WIDTH-2*border_size-((lenght-1)*gap_size)
    #diagram genişliği hesaplandı.

    sum_values=sum(data_dic.values())
    #sözlükteki sayıların toplamı alınır.

    pixel=diagram_width/sum_values
    #diagram genişliği ile sözlükteki değerlerin oranı alınır.

    x_value=border_size
    y_value=HEIGHT-border_size
    #Çizilecek ilk üçgenin x ve y indexi başlatılır.

    canvas.setTextAnchor("n")
    #yazı ortadan tutularak başlatılır.
    #(http://www.ezgraphics.org/ReferenceGuide/GraphicsCanvas#method-setTextAnchor buradan daha çok bilgi alabilirsin bu fonksiyon ile ilgili)

    canvas.setFill("black")
    main_x=(WIDTH/2)-(diagram_width/2)
    main_y=border_size
    canvas.drawRectangle(main_x,main_y,diagram_width,30)
    #Başlığın yazılacağı dikdörtgen çizilir.

    canvas.setColor("white")
    canvas.drawText(WIDTH/2,border_size,title)
    #çizilen dikdörtgenin ortasına başlık yazılır.


    len_color_list=len(COLOURS) #COLOURS listesinin boyutu alınır.
    temp=[] #geçici bir liste oluşturulur.
    canvas.setTextAnchor("center")
    for i in data_dic:
        color = random.randint(0, len_color_list-1)
        temp.append(color)
        while color in temp:
            color = random.randint(0, len_color_list-1)
    #Colours listesinden birbirinden farklı rastgele renkler alınır.

        cl=COLOURS[color] #(R,G,B) şeklindeki tuple cl değişkenine atanır.
        pixel_value = pixel * data_dic[i]
        canvas.setFill(cl[0],cl[1],cl[2])
        canvas.setColor(cl[0],cl[1],cl[2])
        canvas.drawPolygon(x_value, y_value - 30, x_value + pixel_value, y_value - 30, x_value + (pixel_value / 2),y_value)
        #Üçgenler değerlerinin büyüklüğüne orantılı olacak şekilde oluşturulur.

        #Sutun Kısmı
        x_gap=main_x-x_value    #Sütun çizilecek noktalar arasındaki x indexinin farkı hesaplanır.
        y_gap=main_y+30-y_value+30 #Sütun çizilecek noktalar arasındaki y indexinin farkı hesaplanır.
        x_gap/=abs(y_gap)
        #x_gaps değeri y_gaps değerinin mutlak değerine bölünür böylece her bir döngüde x indexinin ne kadar artacağı hesaplanır.


        k=x_value #x_value değişkeni geçici bir k değerine atanır.

        r = cl[0] / abs(y_gap)
        g = cl[1] / abs(y_gap)
        b = cl[2] / abs(y_gap)
        r1 = cl[0]
        g1 = cl[1]
        b1 = cl[2]
        #Rastegele seçilen rengin R,G,B sayı değerleri r1,g1,b1 değerlerine atanır.
        #(R,G,B) değeri (0,0,0) olması istendiğinden
        #Her bir döngüde azalacak r,g,b değerleri; /abs(y_gap) işlemiyle hesaplanır.

        for j in range(abs(y_gap)):
            k += x_gap #x indexi her döngüde artar.

            canvas.setColor(int(r1),int(g1),int(b1))
            #r1,g1,b1 değerleri int() değere dönüştürülerek renk ayarlanır.

            canvas.drawLine(k, y_value - 30-j, pixel_value+k, y_value - 30-j)
            #çizgi çekilir.

            r1-=r
            g1-=g
            b1-=b
            #r1,g1,b1 değerleri hesaplanan şekilde her döngüde azaltılır.


        canvas.setColor(255-cl[0],255-cl[1],255-cl[2])
        #arkaplan renginin zıttı olarak başlıklar yazılır.
        canvas.drawText(x_value + (pixel_value / 2), y_value - 30, i)

        x_value+=gap_size+pixel_value
        main_x+=pixel_value
        #Üçgenlerin y indexleri aynı iken x indexleri değişir.


def main():
    # DO NOT EDIT THIS CODE
    input_file = ""
    file_read = False
    # Try to read file name from input commands:
    args = sys.argv[1:]
    if len(args) == 0 or len(args) > 1:
      print('\n\nUsage\n\tTo visualise data using a sankey diagram type:\
            \n\n\t\tpython sankey.py infile\n\n\twhere infile is the name of the file containing the data.\n')
      print('\nWe will ask you for a filename, as no filename was provided')

    else:
      input_file = args[0]

    # Use file provided or ask user for valid filename (we will iterate until a valid file is provided)
    while not file_read:
        # Ask for filename if not available yet
        if input_file == "":
            input_file = input("Provide name of the file to load: ")

      # Try to Read the file contents
        try:
            title, left_axis_label, data_list = read_file(input_file)
            file_read = True
        except FileNotFoundError:
            print(f"File {input_file} not found or is not readable.")
            input_file = ""

    # Section 2: Create a window and canvas
    win = set_up_graph(title)

    # Section 3: Process the data
    try:
        data_dic = process_data(data_list)
    except ValueError as error:
        print("Content of file is invalid: ")
        print(error)
        return

    # # Section 4: Draw the graph
    draw_sankey(win, left_axis_label, data_dic, GAP, 100)
    win.wait()


main()
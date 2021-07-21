import MIR3_1 as crawl
import MIR3_2 as pr
import MIR3_3 as hits
import MIR3_4_1 as cb
import MIR3_4_2 as cf
import MIR3_4_3 as lf
import sys
import PySimpleGUI as sg

print = sg.Print
sg.theme('BluePurple')
font = ("Arial", 13, 'bold')


def window_crawl():
    sg.theme('BluePurple')

    layout = [
        [sg.Text('Input Parameters:                                                    ',)],
        [sg.Text('How many pages do you want to retrieve?                              '), sg.InputText()],
        [sg.Text('Specify IDs of initial pages (use whitespace between them            '), sg.InputText()],
        [sg.Text('Output file name (a name which is different from "CrawledPages.json")'), sg.InputText()],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Window Crawl', layout, margins=(400, 200), location=(0,0), font=font)
    event, values = window.read()

    n_p = int(values[0])
    list_of_initial_pages = values[1].split(' ')
    file_name = values[2]

    window.close()
    if event == 'Ok':
        crawl.crawl(n_p, list_of_initial_pages, file_name)

    window_I()

def window_hits():
    sg.theme('BluePurple')

    layout = [ 
        [sg.Text('Input Parameters:                                               ',)],
        [sg.Text('N ? (for example <10>)                                     '), sg.InputText(size=(10,10))],
        [sg.Text('Crawled papers file address ? (for example <CrawledPapers.json>)'), sg.InputText(size=(20,10))],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Window HITS', layout, margins=(400, 200), location=(0,0), font=font)
    event, values = window.read()
    
    N = int(values[0])
    int_addr = values[1]

    if event == 'Ok':
        print('please wait ...', keep_on_top=True, no_titlebar=True, erase_all=True,font=font, size=(30, 7))
        top_hits = hits.get_top_hit(int_addr, N)
        print(f"--- Top " + str(N) +  " Authoritized Authors ---", erase_all=True)
        [print(str(i+1) + ": " + str(top_hit), keep_on_top=True, no_titlebar=True, erase_all=False,font=font) for (i, top_hit) in enumerate(top_hits)]

    window.close()
    window_I()

def window_pagerank():
    sg.theme('BluePurple')

    layout = [ 
        [sg.Text('Input Parameters:                                               ',)],
        [sg.Text('alpha ? (for example <0.2>)                                     '), sg.InputText(size=(10,10))],
        [sg.Text('Crawled papers file address ? (for example <CrawledPapers.json>)'), sg.InputText(size=(20,10))],
        [sg.Text('Output file name ? (for example <PageRankTest.json>)            '), sg.InputText(size=(20,10))],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Window PageRank', layout, margins=(400, 200), location=(0,0), font=font)
    event, values = window.read()
    
    alpha = float(values[0])
    int_addr = values[1]
    out_addr = values[2]

    if event == 'Ok':
        print('please wait ...', keep_on_top=True, no_titlebar=True, erase_all=True,font=font, size=(30, 7))
        pagerank = pr.page_rank()
        pagerank.calc_page_rank(alpha, int_addr, out_addr)
        print("check out " + out_addr, keep_on_top=True, no_titlebar=True, erase_all=False,font=font, size=(30, 7))

    window.close()
    window_I()

def window_cb():
    sg.theme('BluePurple')

    layout = [ 
        [sg.Text('Input Parameters:                                               ',)],
        [sg.Text('user profile index ? (for example <12>)                           '), sg.InputText(size=(10,10))],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Window content based recommender', layout, margins=(400, 200), location=(0,0), font=font)
    event, values = window.read()
    
    idx = int(values[0])

    if event == 'Ok':
        print('please wait ...', keep_on_top=True, no_titlebar=True, erase_all=True,font=font, size=(30, 7))
        top_arts = cb.find_related_articles(idx)
        print(f"--- Top " + str(10) +  " Related Articles ---", erase_all=True)
        [print(str(i+1) + ": " + str(top_hit), keep_on_top=True, no_titlebar=True, erase_all=False,font=font) for (i, top_hit) in enumerate(top_arts)]
    window.close()
    window_I()

def window_cf():
    sg.theme('BluePurple')

    layout = [ 
        [sg.Text('Input Parameters:                                               ',)],
        [sg.Text('user profile index ? (for example <12>)                           '), sg.InputText(size=(10,10))],
        [sg.Text('N ? (for example <3000>)                           '), sg.InputText(size=(10,10))],
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Window collaborative filtering recommender', layout, margins=(400, 200), location=(0,0), font=font)
    event, values = window.read()
    
    idx = int(values[0])
    N = int(values[1])

    if event == 'Ok':
        print('please wait ...', keep_on_top=True, no_titlebar=True, erase_all=True,font=font, size=(30, 7))
        new_user_profile_vec, top_arts = cf.get_cf(idx, N)
        print("--- Top " + str(10) +  " Related Articles ---", erase_all=True)
        [print(str(i+1) + ": " + str(top_hit), keep_on_top=True, no_titlebar=True, erase_all=False,font=font) for (i, top_hit) in enumerate(top_arts)]
        print()
        print(f"--- New Vector for User " + str(idx) +  " ---",)
        [print(str(i) + " :: " + str(round(el, 5)), keep_on_top=True, no_titlebar=True, erase_all=False,font=font) for (i, el) in enumerate(new_user_profile_vec)]


    window.close()
    window_I()

def window_lf():
    sg.theme('BluePurple')

    layout = [ 
        [sg.Ok(), sg.Cancel()]
    ]
    window = sg.Window('Window latent factor', layout, margins=(400, 200), location=(0,0), font=font)
    event, values = window.read()

    if event == 'Ok':
        print('please wait ...', keep_on_top=True, no_titlebar=True, erase_all=True,font=font, size=(30, 7))
        err = lf.get_err_test()
        print("--- error = " + str(err) +  " ---",)


    window.close()
    window_I()

def window_I():
    sg.theme('BluePurple')

    layout = [
        [sg.Text('Hi there ;) Choose an option and press OK to continue or press cancel to close the Graphical UI.',)],
        [sg.Text('Which section do you want to go?', size=(30, 1), text_color='red'), sg.InputOptionMenu(['1. Crawling', '2. PageRank', '3. Authority',
        '4. Recommender System I(Content-based)', '5. Recommender System II(Collaborative Filtering)', '6. Finding P and Q'])],
        [sg.Ok(), sg.Cancel()]
    ]

    window = sg.Window('Window I', layout, margins=(400, 200), location=(0,0), font=font, keep_on_top=True)
    event, value = window.read()

    if event != 'Ok':
        window.close()
        sys.exit()


    if value[0][0] == '1':
        window.close()
        window_crawl()
        window_I()
        sys.exit()

    if value[0][0] == '2':
        window.close()
        window_pagerank()
        window_I()  
        sys.exit()
        
    if value[0][0] == '3':
        window.close()
        window_hits()
        window_I()  
        sys.exit()

    if value[0][0] == '4':
        window.close()
        window_cb()
        window_I()  
        sys.exit()

    if value[0][0] == '5':
        window.close()
        window_cf()
        window_I()  
        sys.exit()

    if value[0][0] == '6':
        window.close()
        window_lf()
        window_I()  
        sys.exit()

def window_zero():
    layout = [[sg.Text("Hello from sajad, please press OK to continue!")], [sg.Button("OK", size=(2,1), border_width=3, )]]

    window = sg.Window("MIR Third Project - Sajad F. Maqrebi", layout, margins=(400, 200), location=(0,0), font=font)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()
    if event:
        window_I()


window_zero()


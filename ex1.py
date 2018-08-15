import time
import psutil
import argparse
import requests

NUM_PIXELS = 8

def getParams():
    parser = argparse.ArgumentParser(description='Learning Python!')
    parser.add_argument('portlist', type=str, default='all', nargs='?', help='list of ports in usual Extreme format (no spaces)')
    parser.add_argument('-m', '--match', help='string to match output lines on')

    args = parser.parse_args()
    return args

def do_stuff():   
    for i in range(1,10):
        t=time.localtime()
        p= int(10.0*psutil.cpu_percent())
        show_graph_line(p)
        print(i,t[5],p)
        time.sleep(0.4)
    print("bye")


def show_graph(v, r, g, b):
    v *= NUM_PIXELS
    for x in range(NUM_PIXELS):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
        for l in [r, g, b]: show_graph_line(l)
        v -= 1

def show_graph_line(n):
    if n ==0:
        line = "-" 
    else:
        line = n*"*"
    print(line)


def main():
    args = getParams()

    r=requests.get('https://www.metoffice.gov.uk')
    print(r.status_code)
    print(r.headers['content-type']

  

   
if __name__  == '__main__':
    try:
        main()
    except SystemExit:
        pass

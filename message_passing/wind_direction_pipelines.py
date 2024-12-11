import os
import re
from multiprocessing import Pipe, Process
from os.path import join

import time

WIND_REGEX = "\d* METAR.*EGLL \d*Z [A-Z ]*(\d{5}KT|VRB\d{2}KT).*="
WIND_EX_REGEX = "(\d{5}KT|VRB\d{2}KT)"
VARIABLE_WIND_REGEX = ".*VRB\d{2}KT"
VALID_WIND_REGEX = "\d{5}KT"
WIND_DIR_ONLY_REGEX = "(\d{3})\d{2}KT"
TAF_REGEX = ".*TAF.*"
COMMENT_REGEX = "\w*#.*"
METAR_CLOSE_REGEX = ".*="


def parse_to_array(text_conn, metars_conn):
    '''instead of accepting  text string, it accepts a text connection
        This would be a connection to a pipe
        and it also accepts an output connection (metars_conn)
    '''
    text = text_conn.recv()  # extract text from the pipe.
    #We are going to receive a stream of these messages ( we have more messages on the pipe to process.).
    while text is not None:
        lines = text.splitlines()
        metar_str = ""
        metars = []
        for line in lines:
            if re.search(TAF_REGEX, line):
                break
            if not re.search(COMMENT_REGEX, line):
                metar_str += line.strip()
            if re.search(METAR_CLOSE_REGEX, line):
                metars.append(metar_str)
                metar_str = ""
        metars_conn.send(metars) #send to pipe the metars data
        text = text_conn.recv() #receive next text message from pipe
    metars_conn.send(None) # after we get text==None, send info that we reached the end of stream


def extract_wind_direction(metars_conn, winds_conn):
    metars = metars_conn.recv()
    while metars is not None:
        winds = []
        for metar in metars:
            if re.search(WIND_REGEX, metar):
                for token in metar.split():
                    if re.match(WIND_EX_REGEX, token):
                        winds.append(re.match(WIND_EX_REGEX, token).group(1))
        winds_conn.send(winds)
        metars = metars_conn.recv()
    winds_conn.send(None)


def mine_wind_distribution(winds_conn, wind_dist_conn):
    wind_dist = [0]*8    #  N NE E SE S SW NW W
    winds = winds_conn.recv()
    while winds is not None:
        for wind in winds:
            if re.search(VARIABLE_WIND_REGEX, wind):
                for i in range(8):
                    wind_dist[i] +=1
            elif re.search(VALID_WIND_REGEX, wind):
                d = int(re.match(WIND_DIR_ONLY_REGEX, wind).group(1))
                dir_index = round(d/45.8)%8
                wind_dist[dir_index] += 1
        winds = winds_conn.recv()
    wind_dist_conn.send(wind_dist)


if __name__ == '__main__':
    text_conn_a, text_conn_b = Pipe() #two ends of pipe
    metars_conn_a, metars_conn_b = Pipe()
    winds_conn_a, winds_conn_b = Pipe()
    winds_dist_conn_a, winds_dist_conn_b = Pipe()

    Process(target= parse_to_array, args=(text_conn_b, metars_conn_a)).start()
    Process(target= extract_wind_direction, args=(metars_conn_b, winds_conn_a)).start()
    Process(target= mine_wind_distribution, args=(winds_conn_b, winds_dist_conn_a)).start()

    path_with_files = "metarfiles/"
    start = time.time()
    for file in os.listdir(path_with_files):
        f = open(join(path_with_files, file), 'r')
        text = f.read()
        # do not need call this functions directly because they will be running in separate processes
        # metars = parse_to_array(text)
        # winds = extract_wind_direction(metars)
        # wind_dist = mine_wind_distribution(winds, wind_dist)
        # Instead, we need to pass on the messages onto the pipes and the information
        # that we need to pass is the text containing the weather reports itself.
        text_conn_a.send(text)
    text_conn_a.send(None)
    wind_dist = winds_dist_conn_b.recv()
    end = time.time()
    print(wind_dist)
    print(end - start)

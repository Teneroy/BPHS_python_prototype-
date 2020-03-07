import os
from playsound import playsound


def playTrack(t_folder, t_file):
    playsound(os.getcwd() + '\\' + t_folder + '\\' + t_file)

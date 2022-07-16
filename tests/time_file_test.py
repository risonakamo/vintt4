from os.path import join,dirname,realpath

from vintt4.vintt_time import incrementTime

HERE:str=dirname(realpath(__file__))

incrementTime(
    process="something.exe",
    category="cat3",
    time=1,
    path=join(HERE,"timefile.yml")
)
from pprint import pprint

from vintt4.vintt_config import loadVinttConfig

pprint(loadVinttConfig("testconfig.yml").dict())
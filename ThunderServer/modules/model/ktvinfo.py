
from modules.model.common import Serializable

class ktv_info(Serializable):
    def __init__(self):
        self.ktvid = None
        self.ktvname = None
        self.jd = None
        self.wd = None
        self.city = None
        self.classarea = None
        self.province = None
        self.provincename = None
        self.country = None
        self.hostaddress = None
        self.stbsystemboot = None
        self.mtype=None
        self.projectver = None
        self.updatetime = None



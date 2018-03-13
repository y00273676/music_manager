
import os
import re
#import hashlib
import threading
#def DownFileCompletHandler(object state, string localpath)

### 下载文件
class DownFileUtil():
    _ins = None
    def get_filename_key(url):
        return "filecache:{0}".format(url.MD5())
    _redis_str = RedisString(1)

    ### 中转服务器内网IP
    _tranktv_netip = None

    @property
    def TranKtvNetIp(self):
        return self._tranktv_netip
        pass

    @TranKtvNetIp.setter
    def TranKtvNetIp(self, value):
        self._tranktv_netip = value

    cloudktvsongpath = "cloudktvsong"
    ApacheDocsPath = os.path.join(Config.AppSet.GetCloudKtvIniValue("ApacheDocsPath", "c:\thunder\Apache\htdocs"), cloudktvsongpath)

    ##文件大小不能超过 10 MB
    filelengthlimit = 10485760

    @staticmethod
    def Ins():
        if not DownFileUtil._ins:
            DownFileUtil._ins = DownFileUtil()
        return DownFileUtil._ins

    ### 异步下载文件
    ### <param name="url"></param>
    def DownFileAsync(url, callback = None, state = None):
        ThreadPool.QueueUserWorkItem(new WaitCallback(p =>
        {
            try:
                filepath = self.DownFile(url)
                if callback != None:
                    callback(state, filepath)
            except Exception as ex:
                ClassLoger.Error("DownFileUtil/异步下载文件", ex, url)
        }))

    ### 同步下载文件，下载完成返回文件本地路径
    ### <param name="url"></param>
    ### <returns></returns>
    @staticmethod
    def DownFile(url):
        if not os.path.exists(url):
            self.Down(url)
        localurl = self.GetFileApachPath(url)
        return localurl

    def Down(url):
        if not url:
            logging.info('down url is None')
            return
        try:
            filename = self.GetFileName(url)
            if not filename:
                logging.error("获取url[{0}]文件名失败.".format(url))
                return

            localpath = os.path.join(ApacheDocsPath, filename)
            HttpUtils.DownFile(url, localpath, FileShare.ReadWrite, filelengthlimit)
        except Exception as ex:
            logging.error("DownLoadFile/Down excepted")
            logging.error(str(ex))
            logging.error(traceback.format_exc())
            
    @staticmethod
    def DownPath(url,path):
        if not url:
            logging.info('down url is None')
            return
        try:
            HttpUtils.DownFile(url, path, FileShare.ReadWrite, filelengthlimit)
        except Exception as ex:
            logging.error("DownLoadFile/Down excepted")
            logging.error(str(ex))
            logging.error(traceback.format_exc())

    def GetFileName(self, url):
        try:
            md5_name = md5(url)
            _re = None
            filename = ""
            try:
                wc = HttpUtils.HEAD(url)
                if wc:
                    content_type = wc["Content-Type"]
                    if content_type.startswith("image/"):
                        ext = ".bmp"
                        suf = content_type.replace("image/", "").lower()
                        if suf in ('jpeg', 'jpg'):
                            ext = ".jpg"
                        elif suf == 'png':
                            ext = ".png"
                        elif suf == 'gif':
                            ext = ".gif"

                        filename = md5_name + ext
                        return filename

                    disposition = wc["Content-disposition"]
                    if disposition:
                        _re = re.compile("filename=\"(.+)\"")
                        m = _re.match(disposition)
                        if m:
                            values = m.groups(1).value.split('.')
                            values[0] = md5_name
                            return '.'.join(values)
            except Exception as ex:
                logging.error("DownFileUtil/GetFileName internal excepted")
                logging.error(str(ex))
                logging.error('url:{0}'.format(url))
                logging.error(traceback.format_exc())

            logging.debug("DownFileUtil/GetFileName", url)

            _re = re.compile("/([\w-]+\.[0-9a-zA-Z]+)(\?.+)?$")
            mc = _re.match(url)
            if mc:
                values = mc.Groups(1).split('.')
                values[0] = md5_name
                return '.'.join(values)
        except Exception as ex:
            logging.error("DownFileUtil/GetFileName", ex)
            logging.error(str(ex))
            logging.error('url:{0}'.format(url))
            logging.error(traceback.format_exc())
        return ''


        ### 判断文件是否存在
        ### <param name="url"></param>
        ### <returns></returns>
        def IsLocalExists(url):
            localpath = self.GetFilePath(url)
            if localpath:
                return os.path.exists(localpath)
            else:
                logging.error('IsLocalExists localpath is None')
                return False



        ### 通过文件原始 url获取文件在 apach\cloudktvsong 磁盘物理路径
        ### <param name="url"></param>
        ### <returns></returns>
        def GetFilePath(url):
            if url:
                filename = self.GetFileName(url)
                if filename:
                    return self.GetFilePathForFileName(filename)
            return ""


        ### 通过文件名获取文件在 apach\cloudktvsong 磁盘物理路径
        ### <param name="filename"></param>
        ### <returns></returns>
        def GetFilePathForFileName(self, filename):
            return os.path.join(ApacheDocsPath, filename)


        ### 获取文件路径(Apach路径)
        ### <param name="url"></param>
        ### <returns></returns>
        def GetFileApachPath(self, url):
            try:
                if url and self.IsLocalExists(url):
                    filename = self.GetFileName(url)
                    return "http://{0}/{1}/{2}".format(self.TranKtvNetIp(), cloudktvsongpath, filename)
            except Exception as ex:
                logging.error("DownFileUtil/GetFileApachPath excepted")
                logging.error(str(ex))
                logging.error(traceback.format_exc())
            return ""

        ### 从Apach cloudktvsong 路径下的文件名获取其在apach的访问路径
        ### <param name="filename"></param>
        ### <returns></returns>
        def GetFileApachPathForCloudKtvSong(filename):
            return "http://{0}/{1}/{2}".format(self.TranKtvNetIp(), cloudktvsongpath, filename)

        ### URL 内容为 音频内容 如:arm ,mp3 下载成功后自动在转码为wav 格式
        ### <param name="url"></param>
        ### <returns></returns>
        def DownAudioFile_ConverWAV(self, url):
            if not url:
                logging.error('DownAudioFile_ConverWAV url is None')
                return ''

            filename = self.GetFileName(url)
            _re = re.compile("(\.mp3|\.aac|\.wav|\.amr|\.wma)$")
            if not _re.match(filename):
                logging.info("DownFileUtil/GetFileApachPathForMP3 {0} 不是音频文件".format(url))
                return None

            apachpath = self.DownFile(url)
            if apachpath:
                _re = re.compile(".+\.mp3$", re.I)
                if _re.match(filename):
                    FFMpeg.Convert2WAV(self.GetFilePathForFileName(filename), False)
                    return apachpath
                else:
                    mp3path = FFMpeg.Convert2Mp3(self.GetFilePathForFileName(filename), False)
                    FFMpeg.Convert2WAV(GetFilePathForFileName(filename), False)
                    return self.GetFileApachPathForCloudKtvSong(Path.GetFileName(mp3path))
            return None


        def Dispose(self):
            iswork = False
            if th_d:
                th_d.abort()

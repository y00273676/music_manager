#!/usr/bin/python
#-*-coding:utf8-*-

from enum import Enum
import threading
import time
import os
import logging
import traceback
import datetime


from config.appConfig import AppSet
#from common.HttpUtils import HttpUtils
from common.utils import md5, isWxHost
from common.types import try_to_decimal, try_to_int

pic_dl_lock=threading.Lock()

HttpUtils = None

class ImgType(Enum):
    bmp = 0
    png = 1
    jpeg = 2
    jpg = 3

class down_img():
    def __init__(self, w, h, url, imgtype):
        self.w = w
        self.h = h
        self.url = url
        self.imgtype = imgtype


class DownImageUtil():
    cloudktvsongpath = "cloudktvsong"
    ApacheDocsPath = os.path.join(AppSet.GetCloudKtvIniValue("ApacheDocsPath", r"c:\thunder\Apache\htdocs"), cloudktvsongpath)
    TranKtvNetIp = None
    _ins = None

    def __init__(self):
        self.th_d = None
        self.iswork = False
        self.urllist = []

    @staticmethod
    def Ins():
        if not DownImageUtil._ins:
            DownImageUtil._ins = DownImageUtil()
        return DownImageUtil._ins

    # 定义静态变量实例
    __instance = None
    # 创建锁
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print('DownImageUtil singleton is not exists')
            try:
                # 锁定
                cls.__lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(DownImageUtil, cls).__new__(cls, *args, **kwargs)
                    #cls.__instance.__init__()
            finally:
                # 锁释放
                cls.__lock.release()
        else:
            print('DownImageUtil singleton is exists')
        return cls.__instance

    def DownImageUtil(self):
        self.iswork = True
        self.th_d = threading.Thread(name='img_dl', target=self.worker)
        self.th_d.daemon = True
        self.th_d.start()

    def worker(self):
        while self.iswork:
            urlarray = []

            pic_dl_lock.acquire()
            urlarray = self.urllist
            self.urllist.clear()
            pic_dl_lock.release()

            if urlarray and len(urlarray) > 0:
                for u in urlarray:
                    self.Down(u)
            else:
                time.sleep(2)

    def Down(self, dimginfo):
        try:
            w = dimginfo['w']
            h = dimginfo['h']
            url = dimginfo['url']
            if not url:
                logging.info('Down empty url')
                return

            localpath = ''
            filename = ''
            ret, filename, localpath = self.IsLocalExists(url, dimginfo['imgtype'], w, h)
            if ret:
                statinfo = os.stat(localpath)
                #TODO not sure st_atime or st_mtime.
                lasttime = datetime.datetime.fromtimestamp(statinfo.st_mtime)
                if not HttpUtils.FileIsModified(url, lasttime):
                    logging.info('pic is not modified: {0}'.format(url))
                    return

            if not localpath:
                filename = md5(url + w + h) + "." + dimginfo['imgtype'].name
                localpath = os.path.join(DownImageUtil.ApacheDocsPath, filename)

            if not os.path.exists(DownImageUtil.ApacheDocsPath):
                os.makedirs(DownImageUtil.ApacheDocsPath)

            imgformat = System.Drawing.Imaging.ImageFormat.Bmp
            if dimginfo['imgtype'] == ImgType.png:
                imgformat = System.Drawing.Imaging.ImageFormat.Png
            elif dimginfo['imgtype'] in (ImgType.jpeg, ImgType.jpg):
                imgformat = System.Drawing.Imaging.ImageFormat.Jpeg
            else:
                imgformat = System.Drawing.Imaging.ImageFormat.Bmp

            logging.debug("DownImageUtil/Down {0}".format(url))

            img = HttpUtils.DownPic(url)
            if img:
                try:
                    if w <= 0 or h <= 0:
                            img.Save(localpath, imgformat)
                    else:
                        pass
                        '''
                        //创建一个bitmap类型的bmp变量来读取文件。
                        Bitmap bmp = new Bitmap(img)
                        //新建第二个bitmap类型的bmp2变量，我这里设置为图片原大小，且指定为非索引像素格式图像
                        Bitmap bmp2 = new Bitmap(img.Width, img.Height, PixelFormat.Format32bppArgb)
                        //将第一个bmp拷贝到bmp2中
                        Graphics draw = Graphics.FromImage(bmp2)
                        draw.DrawImage(bmp, 0, 0)

                        Image.GetThumbnailImageAbort callb = new Image.GetThumbnailImageAbort(ThumbnailCallback)
                        using (Image thumbnail = ((Image)bmp2).GetThumbnailImage(img.Width > w ? w : img.Width, img.Height > h ? h : img.Height, callb, IntPtr.Zero))
                            thumbnail.Save(localpath, imgformat)
                        '''
                except Exception as ex:
                    logging.error('DownImageUtil/Down_1 excepted')
                    logging.error(str(ex))
                    logging.error('url {0} width {1} height {2}'.format(dimginfo['url'], w, h))
                    logging.error(traceback.format_exc())
                img.Dispose()
        except Exception as ex:
            logging.error('DownImageUtil/Down excepted:{0}'.format(dimginfo['url']))
            logging.error(str(ex))
            logging.error(traceback.format_exc())


    # <summary>
    # 异步下载
    # </summary>
    # <param name="w"></param>
    # <param name="h"></param>
    # <param name="url"></param>
    def DownPicAsync(w, h, url, imgtype = ImgType.bmp):
        pic_dl_lock.acquire()
        urllist.append({'url':url, 'h': h, 'w':w, 'imgtype':imgtype})
        pic_dl_lock.release()

    # <summary>
    # 同步下载，并获取文件路径(Apach路径)
    # </summary>
    # <param name="url"></param>
    # <param name="w"></param>
    # <param name="h"></param>
    # <param name="imgtype"></param>
    # <returns></returns>
    @staticmethod
    def DownPicSync(self, url, w = 0, h = 0, imgtype = ImgType.bmp):
        self.Down({ 'url':url, 'h':h, 'w':w, 'imgtype':imgtype })
        return self.GetPicPath(url, imgtype, w, h)

    # <summary>
    # 同步下载图片，自动识别图片格式
    # </summary>
    # <param name="url"></param>
    # <param name="w"></param>
    # <param name="h"></param>
    # <returns></returns>
    def DownPicSyncAuto(self, url, w, h):
        imgtype = self.GetImgType(url)
        return self.DownPicSync(url, w, h, imgtype)

    # <summary>
    #  下载图片支持等比缩放,自动识别文件格式
    # </summary>
    # <param name="url"></param>
    # <param name="w"></param>
    # <param name="h"></param>
    # <returns></returns>
    def DownPicProportionAuto(self, url, w = 0, h = 0):
        imgtype = self.GetImgType(url)
        return self.DownPicProportionSync(url, imgtype, w, h)

    # <summary>
    # 下载图片支持等比缩放
    # </summary>
    # <param name="url"></param>
    # <param name="w"></param>
    # <param name="h"></param>
    # <returns></returns>
    def DownPicProportionSync(self, url, imgtype, w = 0, h = 0):
        if w <= 0 or h <= 0:
            return self.DownPicSync(url, w, h, imgtype)
        try:
            filename = ''
            localpath = ''
            ret, filename, localpath = self.IsLocalExists(url, imgtype, w, h)
            if ret: 
                return self.GetPicPath(url, w, h)

            img = HttpUtils.DownPic(url)
            h1 = h
            w1 = w
            if img:
                if img['Width'] > w or img['Height'] > h:
                    rate1 = h.TryToDecimal() / try_to_decimal(img['Height'])
                    rate2 = w.TryToDecimal() / try_to_decimal(img['Width'])
                    if rate1 < rate2:
                        w1 = try_to_int(img['Width'] * rate1 + 0.5)
                        h1 = try_to_int(img['Height'] * rate1 + 0.5)
                    else:
                        w1 = try_to_int(img['Width'] * rate2 + 0.5)
                        h1 = try_to_int(img['Height'] * rate2 + 0.5)

                    self.SavePic(img, w1, h1, localpath)
                    img.Dispose()
                else:
                    pass
                    '''
                    if img.RawFormat.Guid == System.Drawing.Imaging.ImageFormat.Jpeg.Guid or \
                            img.RawFormat.Guid == System.Drawing.Imaging.ImageFormat.Png.Guid or \
                            img.RawFormat.Guid == System.Drawing.Imaging.ImageFormat.Bmp.Guid:
                        img.Save(localpath, img.RawFormat)
                    img.Dispose()
                    '''
                return self.GetPicPath(url, w, h)
        except Exception as ex:
            logging.error('DownPicProportion excepted {0}'.format(url))
            logging.error(str(ex))
            logging.error(traceback.format_exc())
        return ''


    # <summary>
    # 异步下载图片支持等比缩放
    # </summary>
    # <param name="url"></param>
    # <param name="w"></param>
    # <param name="h"></param>
    def DownPicProportionAsync(self, w, h, url):
        pass
        '''
        ThreadPool.QueueUserWorkItem(new WaitCallback(p =>
        {
            try
            {
                DownPicProportion(url, w, h)
            }
            catch (Exception ex)
            {
                ClassLoger.Error("DownImageUtil/DownPicProportion", ex, url)
            }
        }))
        '''


    # <summary>
    # 通过图片后缀获取图片类型
    # </summary>
    # <param name="url"></param>
    # <returns></returns>
    def GetImgType(self, url):
        imgtype = ImgType.bmp
        pictype = ""
        try:
            para = url.split('/')
            name = para[len(para)- 1]
            p = name.split('.')

            if len(p) > 1:
                pictype = p[1]
            else:
                if isWxHost(url):
                    pictype = "jpg"
        except Exception as ex:
            logging.error('GetImgType excepted:{0}'.format(url))
            logging.error(str(ex))
            logging.error(traceback.format_exc())


        pictype = pictype.lower()
        if pictype in ('jpeg', 'jpg'):
            imgtype = ImgType.jpg
        elif pictype == "png":
            imgtype = ImgType.png
        else:
            imgtype = ImgType.bmp
        return imgtype

    #lockObj = object()
    lockObj = None

    def Down(self, dimginfo):
        try:
            w = dimginfo['w']
            h = dimginfo['h']
            url = dimginfo['url']

            if not url:
                return

            localpath = ''
            filename = ''
            ret, filename, localpath = self.IsLocalExists(url, dimginfo['imgtype'], w, h)
            if ret:
                lasttime = File.GetLastAccessTime(localpath)
                if not HttpUtils.FileIsModified(url, lasttime):
                    return

            if not localpath:
                filename = md5(url + w + h) + "." + dimginfo['imgtype'].name
                localpath = os.path.join(DownImageUtil.ApacheDocsPath, filename)

            if not os.path.exist(DownImageUtil.ApacheDocsPath):
                os.path.makedirs(DownImageUtil.ApacheDocsPath)

            imgformat = System.Drawing.Imaging.ImageFormat.Bmp
            if dimginfo['imgtype'] == ImgType.png:
                imgformat = System.Drawing.Imaging.ImageFormat.Png
            elif dimginfo['imgtype'] in (ImgType.jpeg, ImgType.jpg):
                imgformat = System.Drawing.Imaging.ImageFormat.Jpeg
            else:
                imgformat = System.Drawing.Imaging.ImageFormat.Bmp

            logging.debug("DownImageUtil/Down {0}".format(url))

            img = HttpUtils.DownPic(url)
            if img:
                try:
                    if w <= 0 or h <= 0:
                            img.Save(localpath, imgformat)
                    else:
                        pass
                        '''
                        #//创建一个bitmap类型的bmp变量来读取文件。
                        Bitmap bmp = new Bitmap(img)
                        //新建第二个bitmap类型的bmp2变量，我这里设置为图片原大小，且指定为非索引像素格式图像
                        Bitmap bmp2 = new Bitmap(img.Width, img.Height, PixelFormat.Format32bppArgb)
                        //将第一个bmp拷贝到bmp2中
                        Graphics draw = Graphics.FromImage(bmp2)
                        draw.DrawImage(bmp, 0, 0)

                        Image.GetThumbnailImageAbort callb = new Image.GetThumbnailImageAbort(ThumbnailCallback)
                        using (Image thumbnail = ((Image)bmp2).GetThumbnailImage(img.Width > w ? w : img.Width, img.Height > h ? h : img.Height, callb, IntPtr.Zero))
                            thumbnail.Save(localpath, imgformat)
                        '''
                except Exception as ex:
                    logging.error('DownImageUtil/Down_1 excepted')
                    logging.error('url:{0} width:{1} height:{2}'.format(dimginfo['url'], w, h))
                    logging.error(str(ex))
                    logging.error(traceback.format_exc())
                img.Dispose()
        except Exception as ex:
            logging.error("DownImageUtil/Down excepted")
            logging.error('url:{0}'.format(dimginfo['url']))
            logging.error(str(ex))
            logging.error(traceback.format_exc())



    # <summary>
    # 保存图片原格式的指定宽高缩略图
    # </summary>
    # <param name="srcImg">原图片</param>
    # <param name="wi"></param>
    # <param name="hi"></param>
    # <param name="targetFolder">保存路径</param>
    def SavePic(self, srcImg, wi, hi, targetFolder):
        encoderParams = System.Drawing.Imaging.EncoderParameters()
        quality = [1]
        quality[0] = 75
        encoderParam = System.Drawing.Imaging.EncoderParameter(System.Drawing.Imaging.Encoder.Quality, quality)
        encoderParams.Param[0] = encoderParam

        arrayICI = System.Drawing.Imaging.ImageCodecInfo.GetImageEncoders()
        jpegICI = None
        for x in range(len(arrayICI)):
            if arrayICI[x].FormatDescription.Equals("JPEG"):
                jpegICI = arrayICI[x]
                break

        '''
        using (Bitmap source = new Bitmap(srcImg))
        {
            using (System.Drawing.Bitmap thumb = new Bitmap(wi, hi))
            {
                using (Graphics g = Graphics.FromImage(thumb))
                {
                    g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic
                    g.FillRectangle(Brushes.White, 0, 0, wi, hi)
                    g.DrawImage(source, 0, 0, wi, hi)
                }
                thumb.Save(targetFolder, jpegICI, encoderParams)
            }
        }
        '''


    def ThumbnailCallback(self):
        return False

    # <summary>
    # 获取图片路径(Apach路径)
    # </summary>
    # <param name="url"></param>
    # <param name="imgtype"></param>
    # <param name="width"></param>
    # <param name="height"></param>
    # <param name="checkfile">true 验证图片是否存在  false:不验证图片是否存在</param>
    # <returns></returns>
    def GetPicPath(self, url, imgtype, width = 0, height = 0, checkfile = True):
        try:
            filename = ''
            localpath = ''
            if checkfile:
                ret, filename, localpath = self.IsLocalExists(url, imgtype, width, height)
                if ret:
                    return "http://{0}/{1}/{2}".format(TranKtvNetIp, cloudktvsongpath, filename)
            else:
                return self.GetPicPath1(url, width, height)
        except Exception as ex:
            logging.error('DownImageUtil/GetPicPath excepted')
            logging.error(str(ex))
            logging.error(traceback.format_exc())
        return ""

    # <summary>
    # 获取图片路径(Apach路径),自动识别图片格式
    # </summary>
    # <param name="url"></param>
    # <param name="width"></param>
    # <param name="height"></param>
    # <param name="checkfile">true 验证图片是否存在  false:不验证图片是否存在</param>
    # <returns></returns>
    def GetPicPath(self, url, width = 0, height = 0, checkfile = True):
        imgtype = self.GetImgType(url)
        return self.GetPicPath(url, imgtype, width, height, checkfile)

    #region 获取图片Apach路径
    # <summary>
    # 获取图片路径本地保存路径，自动识别图片格式 不验证图片是否存在 
    # </summary>
    # <returns></returns>
    def GetPicPath1(self, url, width = 0, height = 0):
        imgtype = self.GetImgType(url)
        return self.GetPicPath1(url, width, height, imgtype)


    # <summary>
    # 获取图片Apach路径，不验证图片是否存在
    # </summary>
    # <returns></returns>
    def GetPicPath1(self, url, width=0, height=0, imgtype=ImgType.bmp):
        filename = md5(url + width + height) + "." + imgtype.name
        localpath = os.path.join(DownImageUtil.ApacheDocsPath, filename)
        return "http://{0}/{1}/{2}".format(TranKtvNetIp, cloudktvsongpath, filename)



    # <summary>
    # 判断图片本地是否存在
    # </summary>
    # <param name="url"></param>
    # <param name="loaclpath"></param>
    # <returns></returns>
    def IsLocalExists(self, url, imgtype, width = 0, height = 0):
        filename = ""
        localpath = ""
        try:
            isexits = False
            filename = md5(url + width + height) + "." + imgtype.name
            localpath = os.path.join(DownImageUtil.ApacheDocsPath, filename)
            #TODO need to implete
            '''
            fi = FileInfo(localpath)
            if (fi.Exists)
                fi.LastAccessTimeUtc = DateTime.UtcNow
                isexits = True
            '''

            return isexits, filename, localpath
        except Exception as ex:
            logging.error('IsLocalExists excepted')
            logging.error(str(ex))
            logging.error(traceback.format_exc())
        return False, filename, localpath


    def IsLocalExists(self, url, width = 0, height = 0):
        filename = ""
        localpath = ""
        try:
            #imgtypes = [ImgType.bmp, ImgType.png, ImgType.jpeg, ImgType.jpg]  
            imgtypes = [0, 1, 2, 3]
            for imgtype in imgtypes:
                ret, filename, localpath = self.IsLocalExists(url, ImgType(imgtype), width, height)
                if ret:
                    return True
            return False
        except Exception as ex:
            logging.error('DownImageUtil/IsLocalExist excepted')
            logging.error(str(ex))
            logging.error(traceback.format_exc())
        return False

    def Dispose(self):
        self.iswork = False
        if self.th_d:
            self.th_d.Abort()

import gphoto2 as gp
import logging
import os
import shutil
import getpass

from datetime import datetime

global camera

IMAGE_PATH = '/home/'+getpass.getuser()+'/Pictures/Canon_700D/'

if not os.path.isdir(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)


def init_camera():
    os.system("pkill vfsd-gphoto2")
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    camera = gp.Camera()
    camera.init()


def set_shutter_speed(sh):
    config = camera.get_config()

    shutterspeed_config = gp.gp_widget_get_child_by_name(config, 'shutterspeed')
    shutterspeed_config.set_value(sh)

    camera.set_config(config)


def set_iso(iso):
    config = camera.get_config()

    shutterspeed_config = gp.gp_widget_get_child_by_name(config, 'iso')
    shutterspeed_config.set_value(iso)

    camera.set_config(config)


def capture_image(shutterspeed, iso):
    os.system('gphoto2 --set-config /main/capturesettings/shutterspeed=' + str(shutterspeed))
    os.system('gphoto2 --set-config /main/imgsettings/iso=' + str(iso))

    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    camera = gp.Camera()
    camera.init()
    # config = camera.get_config()
    #
    # shutterspeed_config = gp.gp_widget_get_child_by_name(config, 'shutterspeed')
    # shutterspeed_config.set_value(shutter_speed)
    #
    # shutterspeed_config = gp.gp_widget_get_child_by_name(config, 'iso')
    # shutterspeed_config.set_value(iso)
    #
    # camera.set_config(config)

    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    # SET FILE NAME
    data = datetime.now()
    data_str = 'PIC_' + data.strftime("%d-%m-%y--%H:%M:%S") + ".jpg"

    target = os.path.join('/tmp', file_path.name)

    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    if not os.path.exists(IMAGE_PATH):
        os.mkdir(IMAGE_PATH)
    shutil.move(target, IMAGE_PATH)
    os.rename(IMAGE_PATH + file_path.name, IMAGE_PATH + data_str)
    camera.exit()
    return IMAGE_PATH + data_str

import logging, os, subprocess, sys, gphoto2 as gp, shutil
from datetime import datetime

def capture_image():
    logging.basicConfig(
                format = '%(levelname)s: %(name)s: %(message)s', level = logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()

    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    #SET FILE NAME
    data = datetime.now()
    data_str = 'PIC_' + data.strftime("%d-%m-%y--%H:%M:%S") + ".jpg"

    target = os.path.join('/tmp', file_path.name)

    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    if not os.path.exists('/home/pi/Pictures/Canon_700D'):
        os.mkdir('/home/pi/Pictures/Canon_700D')
    shutil.move(target, '/home/pi/Pictures/Canon_700D')
    os.rename('/home/pi/Pictures/Canon_700D/' + file_path.name, '/home/pi/Pictures/Canon_700D/' + data_str)
    camera.exit()
    return '/home/pi/Pictures/Canon_700D/' + data_str

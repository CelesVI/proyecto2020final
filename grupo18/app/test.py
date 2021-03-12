import os

class Test():
    PROTOCOLO_UPLOADS = "{}/uploads/".format(os.getcwd())
    ALLOWED_FILES_EXTENSIONS = {'PDF'}


    @classmethod
    def dir_uploads(cls):
        ruta = os.getcwd()
        return "{}/uploads/".format(os.getcwd())
    
    @classmethod
    def allowd_files(cls):
        return {'PDF'}
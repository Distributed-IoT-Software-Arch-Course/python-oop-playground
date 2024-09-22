class Device:
    """ Base class for devices """

    def __init__(self, device_id, device_type, device_manufacturer):
        """ Initialize the devices with a devices ID and a devices type """
        self.device_id = device_id
        self.device_type = device_type
        self.device_manufacturer = device_manufacturer



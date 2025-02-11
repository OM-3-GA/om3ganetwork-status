from .services.mcserver import MCServer
from .services.webservice import WebService
from .services.thirdpartyservice import ThirdPartyService

from .utils.datetimeutils import DateTimeUtils

import json
import os
import time

class Data(): 
  class ServiceGroup():
    def __init__(self, type, json_path):
      self.services = []
      self.last_loaded = 0
      
      self.type = type
      self.json_path = json_path
      
    def load(self):
      # Load the json for this service group only when it has been changed
      if os.path.getmtime(self.json_path) > self.last_loaded:
        print("Loading {} group from {}...".format(self.type.__name__, self.json_path))
      
        with open(self.json_path) as json_file:
          self.services = json.load(json_file, object_hook = self.type.from_json) 

        self.last_loaded = int(time.time())
    
  def __init__(self, app):
    self.last_updated = None    

    services_path = os.path.join(app.instance_path, 'services')

    self.service_groups = {}    
    self.service_groups[MCServer] = Data.ServiceGroup(MCServer, os.path.join(services_path, 'mc_servers.json'))
    self.service_groups[WebService] = Data.ServiceGroup(WebService, os.path.join(services_path, 'web_services.json'))
    self.service_groups[ThirdPartyService] = Data.ServiceGroup(ThirdPartyService, os.path.join(services_path, 'third_party_services.json'))

  def load_services(self):
    for key in self.service_groups:
      self.service_groups[key].load()
     
  def get_all_statuses(self):
    for key in self.service_groups:
      for service in self.service_groups[key].services:
        service.get_status()
     
    self.last_updated = DateTimeUtils.get_current_datetime_as_string()

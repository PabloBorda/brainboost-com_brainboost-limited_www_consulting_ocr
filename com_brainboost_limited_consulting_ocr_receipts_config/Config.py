class Config:
    
    _conf = {}
    
    @classmethod
    def read_config(cls):
        content = ''
        with open('global.config') as f:
            content = f.readlines()
        
        for l in content:
            if len(l) > 3:
                if not '#' in l:
                    a = l.split('=')[0].replace(' ','').replace('  ','').replace('\n','')
                    b = l.split('=')[1].replace(' ','').replace('  ','').replace('\n','')
                    cls._conf[a] = b
        return cls._conf
    
    
    @classmethod
    def get(cls,k):
        if cls._conf=={}:
            cls.read_config()
        return cls._conf[k]
            
    @classmethod
    def sandbox(cls):
        return cls.get(k='mode')=='sandbox'
        
    @classmethod
    def obtain_keys_with_pattern(cls,pattern):
        cls.read_config()
        keys_found_in_config_file = cls._conf.keys()
        filtered_dict = {}
        for k in keys_found_in_config_file:
            if pattern in k:
                filtered_dict[k] = cls.get(k)
        return filtered_dict
        
  
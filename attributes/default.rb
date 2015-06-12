# Packages for different platforms
default['junos-config']['packages']['debian'] = [
    'python-pip', 'python-dev', 'libxml2-dev', 'libxslt-dev', 'zlib1g-dev'
    ]

default['junos-config']['packages']['rhel'] = [
    'python-pip', 'python-devel', 'libxml2-devel', 'libxslt-devel', 
    'gcc', 'openssl'
    ]


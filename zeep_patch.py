import os
import sys
import zeep

def patch_zeep():
    zeep_utils = os.path.join(os.path.dirname(sys.modules['zeep'].__file__), 'utils.py')
    with open(zeep_utils, 'r') as f:
        content = f.read()
    
    patched_content = content.replace(
        'import cgi',
        'from email.message import Message'
    ).replace(
        'ctype, pdict = cgi.parse_header(content_type)',
        'msg = Message()\nmsg["content-type"] = content_type\nctype = msg.get_content_type()\npdict = dict(msg.get_params()[1:])'
    )
    
    with open(zeep_utils, 'w') as f:
        f.write(patched_content)

if __name__ == '__main__':
    patch_zeep() 
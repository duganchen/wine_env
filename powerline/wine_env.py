import os
from powerline.theme import requires_segment_info

@requires_segment_info
def bottle(pl, segment_info, create_watcher, *args):
    prefix = segment_info['environ'].get('WINEPREFIX', '')
    if not prefix:
        return prefix
    return os.path.basename(prefix)

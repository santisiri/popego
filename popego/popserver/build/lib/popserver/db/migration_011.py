# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 011
# Last update - Account

migration = [
    ("""\
        ALTER TABLE user_items ALTER COLUMN item_id SET NOT NULL;
        ALTER TABLE videothumbnails DROP CONSTRAINT videothumbnails_video_item_id_fk;
        ALTER TABLE videothumbnails ADD CONSTRAINT videothumbnails_video_item_id_fk FOREIGN KEY (video_item_id) 
          REFERENCES videos (item_id) ON DELETE CASCADE;
     """, 
     """\
        ALTER TABLE user_items ALTER COLUMN item_id DROP NOT NULL;
        ALTER TABLE videothumbnails DROP CONSTRAINT videothumbnails_video_item_id_fk;
        ALTER TABLE videothumbnails ADD CONSTRAINT videothumbnails_video_item_id_fk FOREIGN KEY (video_item_id) 
          REFERENCES videos (item_id);
     """),
]


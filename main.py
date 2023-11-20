bl_info = {
    "name": "Auto Save with UI Messages",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 6, 5),
    "location": "Automatically",
    "description": "Automatically saves the file after undo/redo operations with UI messages",
    "warning": "",
    "wiki_url": "",
    "category": "System",
}

import bpy
from bpy.app.handlers import persistent
import time

# 设置自动保存的时间间隔（以秒为单位）
AUTO_SAVE_INTERVAL = 30  # 例如，5分钟

last_save_time = 0

def show_status_message(message):
    """ 显示状态栏消息 """
    bpy.context.workspace.status_text_set(message)

@persistent
def auto_save_post(scene):
    global last_save_time
    current_time = time.time()
    if current_time - last_save_time > AUTO_SAVE_INTERVAL:
        if bpy.data.is_saved and bpy.data.filepath:
            try:
                show_status_message("Auto Saving...")
                bpy.ops.wm.save_mainfile()
                show_status_message("Auto Save Complete: " + bpy.data.filepath)
                last_save_time = current_time
                
                print("AUTO SAVE: save file success")
            except Exception as e:
                show_status_message("Auto Save Failed: " + str(e))
            finally:
                # 清除状态栏消息
                bpy.context.workspace.status_text_set(None)

def register():
    bpy.app.handlers.undo_post.append(auto_save_post)
    bpy.app.handlers.redo_post.append(auto_save_post)

def unregister():
    if auto_save_post in bpy.app.handlers.undo_post:
        bpy.app.handlers.undo_post.remove(auto_save_post)
    if auto_save_post in bpy.app.handlers.redo_post:
        bpy.app.handlers.redo_post.remove(auto_save_post)

if __name__ == "__main__":
    register()

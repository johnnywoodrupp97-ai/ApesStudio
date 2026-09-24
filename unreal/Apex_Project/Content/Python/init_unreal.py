"""Runs when the Unreal Editor starts (Python Editor Script Plugin): adds the Exodus menu and, the first time the
project opens, builds the vertical slice map (imports the SourceArt FBX files and places everything)."""
import unreal

import exodus_ue.exodus_setup as setup

MENU_OWNER = "ExodusMenu"


def _add_menu():
    menus = unreal.ToolMenus.get()
    main = menus.find_menu("LevelEditor.MainMenu")
    if not main:
        return
    sub = main.add_sub_menu(MENU_OWNER, "", "Exodus", "Exodus", "Exodus: vertical slice tools")
    entries = [
        ("BuildAll", "Build Vertical Slice (import + map)", "Import the SourceArt FBX and rebuild L_VerticalSlice",
         "import exodus_ue.exodus_setup as s; s.build(reimport=True)"),
        ("BuildMap", "Rebuild Map Only", "Rebuild L_VerticalSlice from slice_layout.json, keeping imported assets",
         "import exodus_ue.exodus_setup as s; s.build(reimport=False)"),
    ]
    for name, label, tip, command in entries:
        e = unreal.ToolMenuEntry(name=name, type=unreal.MultiBlockType.MENU_ENTRY)
        e.set_label(label)
        e.set_tool_tip(tip)
        e.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, "", command)
        sub.add_menu_entry("Slice", e)
    menus.refresh_all_widgets()


_first_tick = {}


def _auto_build(_dt):
    # Wait a few frames so the editor has finished loading before building the map.
    _first_tick["n"] = _first_tick.get("n", 0) + 1
    if _first_tick["n"] < 60:
        return
    unreal.unregister_slate_post_tick_callback(_first_tick.pop("handle"))
    if not setup.map_exists():
        unreal.log("[Exodus] L_VerticalSlice not found: building the vertical slice (first run, a few minutes)")
        setup.build(reimport=True)


_add_menu()
if not setup.map_exists():
    _first_tick["handle"] = unreal.register_slate_post_tick_callback(_auto_build)

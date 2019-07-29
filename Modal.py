import sublime
import sublime_plugin

currentMode = "Normal"

def updateView(view):
    if currentMode != None:
        view.set_status("mode", "Mode: " + str(currentMode))
        view.set_read_only(currentMode != "Insert")

        settings = view.settings()
        settings.set("block_caret", currentMode != "Insert")
        settings.set("highlight_line", currentMode == "Insert")
    else:
        view.erase_status("mode")

def updateMode(view, mode):
    global currentMode
    currentMode = mode

    updateView(view)

class ModalSetModeCommand(sublime_plugin.WindowCommand):
    def run(self, mode):
        updateMode(self.window.active_view(), mode)

class WithViewEvents(sublime_plugin.ViewEventListener):
    def on_activated(self):
        updateMode(self.view, "Normal")

    def on_deactivated(self):
        updateMode(self.view, None)

    def on_text_command(self, command, args):
        self.view.set_read_only(False)

    def on_post_text_command(self, command, args):
        updateView(self.view)

class WithEvents(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        value = None

        if key == "modal.mode":
            value = currentMode
        else:
            return

        if operator == sublime.OP_EQUAL:
            return value == operand
        elif operator == sublime.OP_NOT_EQUAL:
            return value != operand

class ModalInsertLine(sublime_plugin.TextCommand):
    def run(self, edit, before = False, switch_mode = None):
        if before:
            self.view.run_command(
                "run_macro_file",
                {"file": "res://Packages/Default/Add Line Before.sublime-macro"}
            )
        else:
            self.view.run_command(
                "run_macro_file",
                {"file": "res://Packages/Default/Add Line.sublime-macro"}
            )

        if switch_mode != None:
            updateMode(self.view, switch_mode)

class ModalReplicateLine(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("expand_selection", {"to": "line"})
        self.view.run_command("duplicate_line")

class ModalInMode(sublime_plugin.TextCommand):
    def run(self, edit, mode, command, args = {}):
        prevMode = currentMode
        updateMode(self.view, mode)
        self.view.run_command(command, args)
        updateMode(self.view, prevMode)

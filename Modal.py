import sublime
import sublime_plugin

currentMode = "Normal"

def updateMode(view, mode):
    global currentMode
    currentMode = mode

    updateVew(view)

def updateVew(view):
    if currentMode != None:
        view.set_status("mode", "Mode: " + str(currentMode))
        view.set_read_only(currentMode != "Insert")

        settings = view.settings()
        settings.set("block_caret", currentMode != "Insert")
        settings.set("highlight_line", currentMode == "Insert")
    else:
        view.erase_status("mode")

class ModalSetModeCommand(sublime_plugin.WindowCommand):
    def run(self, mode):
        updateMode(self.window.active_view(), mode)

class WithViewEvents(sublime_plugin.ViewEventListener):
    def on_activated_async(self):
        updateVew(self.view)

    def on_text_command(self, command, args):
        self.view.set_read_only(False)

    def on_post_text_command(self, command, args):
        updateVew(self.view)

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

#include <dshell/windows/shell.h>

#include <gtk-layer-shell/gtk-layer-shell.h>

GtkApplicationWindow* dshell_windows_shell_init(GtkApplication* app) {
    GtkWidget* window = gtk_application_window_new(app);
    return GTK_APPLICATION_WINDOW(window);
}
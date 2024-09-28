#include <windows/corners.h>
#include <gtk-layer-shell/gtk-layer-shell.h>

GtkWidget *shell_windows_corners_new(GtkApplication *app)
{
    GtkWidget *window = gtk_application_window_new(app);
    return window;
}
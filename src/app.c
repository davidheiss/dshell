#include <dshell/app.h>
#include <dshell/windows/shell.h>

#include <gtk/gtk.h>

static void on_activate(GtkApplication* app) {
    GtkApplicationWindow* window = dshell_windows_shell_init(app);
    gtk_window_present(GTK_WINDOW(window));
}

int dshell_application_run(int argc, char *argv[])
{
    GtkApplication *app;
    int status;

    app = gtk_application_new(NULL, G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(on_activate), 0);
    status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    return status;
}
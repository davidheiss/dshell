#include <application.h>
#include <utils.h>
#include <windows/corners.h>

static void shell_application_on_activate(GtkApplication *app)
{
    GtkWidget *windows[] = {
        shell_windows_corners_new(app),
    };

    for (size_t i = 0; i < ARRAY_SIZE(windows); i++) {
        GtkWindow* window =  GTK_WINDOW(windows[i]);
        gtk_window_present(window);
    }
}

GtkApplication *shell_application_new()
{
    GtkApplication *app = gtk_application_new(NULL, G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(shell_application_on_activate), 0);
    return app;
}

int shell_application_run(int argc, char *argv[])
{
    GtkApplication *app = shell_application_new();
    const int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    return status;
}
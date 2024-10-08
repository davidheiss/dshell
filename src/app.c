#include <dshell/app.h>
#include <dshell/windows/panel.h>
#include <dshell/windows/corners.h>

#include <gtk/gtk.h>
#include <gio/gio.h>

void update_css(GFileMonitor *monitor,
                GFile *file,
                GFile *other_file,
                GFileMonitorEvent event_type,
                GtkCssProvider *provider)
{
    if (event_type == G_FILE_MONITOR_EVENT_CHANGED)
    {
        gtk_css_provider_load_from_file(provider, file);
    }
}

static void on_activate(GtkApplication *app)
{
    GdkDisplay *display = gdk_display_get_default();

    GtkCssProvider *provider = gtk_css_provider_new();
    GFile *file = g_file_new_for_path("style.css");
    gtk_css_provider_load_from_file(provider, file);
    gtk_style_context_add_provider_for_display(display, GTK_STYLE_PROVIDER(provider), GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);
    GFileMonitor *monitor = g_file_monitor_file(file, G_FILE_MONITOR_NONE, NULL, NULL);
    g_signal_connect(monitor, "changed", G_CALLBACK(update_css), provider);

    GtkApplicationWindow *window; 
    window = dshell_windows_panel_new(app);
    gtk_window_present(GTK_WINDOW(window));

    window = dshell_windows_corners_new(app);
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
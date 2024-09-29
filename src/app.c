#include <app.h>
#include <utils.h>
#include <windows/corners.h>
#include <gio/gio.h>

static void css_changed(GFileMonitor *monitor, GFile *file, GFile *other_file,
                        GFileMonitorEvent event_type, gpointer user_data)
{
    if (event_type == G_FILE_MONITOR_EVENT_CHANGED) {
        gtk_css_provider_load_from_file(GTK_CSS_PROVIDER(user_data), file);
    }
}

static void listen_css(GtkApplication *app)
{
    GtkCssProvider *css_provider = gtk_css_provider_new();

    GdkDisplay *display = gdk_display_get_default();

    gtk_style_context_add_provider_for_display(display, GTK_STYLE_PROVIDER(css_provider), GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);

    GFile *file = g_file_new_for_path("style.css");
    gtk_css_provider_load_from_file(css_provider, file);

    GFileMonitor *monitor = g_file_monitor_file(file, G_FILE_MONITOR_NONE, NULL, NULL);
    g_signal_connect(monitor, "changed", G_CALLBACK(css_changed), css_provider);
}

static void present_windows(GtkApplication *app)
{
    GtkApplicationWindow *windows[] = {
        shell_windows_corners_new(app),
    };

    for (size_t i = 0; i < ARRAY_SIZE(windows); i++)
    {
        GtkWindow *window = GTK_WINDOW(windows[i]);
        gtk_window_present(window);
    }
}

static void on_activate(GtkApplication *app)
{
    listen_css(app);
    present_windows(app);
}

int shell_application_run(int argc, char *argv[])
{
    GtkApplication *app = gtk_application_new(NULL, G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(on_activate), NULL);
    const int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);
    return status;
}
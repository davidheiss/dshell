#include <dshell/windows/panel.h>

#include <gtk-layer-shell/gtk-layer-shell.h>

GtkApplicationWindow* dshell_windows_panel_new(GtkApplication *app) {
    GtkWidget *window = gtk_application_window_new(app);
    gtk_widget_add_css_class(window, "panel");
    gtk_window_set_default_size(GTK_WINDOW(window), 0, 32);

    gtk_layer_init_for_window(GTK_WINDOW(window));

    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_LEFT, true);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_TOP, true);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_RIGHT, true);

    gtk_layer_set_layer(GTK_WINDOW(window), GTK_LAYER_SHELL_LAYER_BOTTOM);

    gtk_layer_auto_exclusive_zone_enable(GTK_WINDOW(window));

    return GTK_APPLICATION_WINDOW(window);
 }
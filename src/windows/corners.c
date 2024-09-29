#include <windows/corners.h>
#include <gtk-layer-shell/gtk-layer-shell.h>

GtkApplicationWindow *shell_windows_corners_new(GtkApplication *app)
{
    GtkWidget *widget = gtk_application_window_new(app);

    gtk_widget_set_name(widget, "corners");

    gtk_layer_init_for_window(GTK_WINDOW(widget));

    gtk_layer_set_layer(GTK_WINDOW(widget), GTK_LAYER_SHELL_LAYER_BOTTOM);

    gtk_layer_set_anchor(GTK_WINDOW(widget), GTK_LAYER_SHELL_EDGE_TOP, true);
    gtk_layer_set_anchor(GTK_WINDOW(widget), GTK_LAYER_SHELL_EDGE_RIGHT, true);
    gtk_layer_set_anchor(GTK_WINDOW(widget), GTK_LAYER_SHELL_EDGE_BOTTOM, true);
    gtk_layer_set_anchor(GTK_WINDOW(widget), GTK_LAYER_SHELL_EDGE_LEFT, true);

    return GTK_APPLICATION_WINDOW(widget);
}
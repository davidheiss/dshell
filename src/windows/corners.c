#include <dshell/windows/corners.h>
#include <gtk-layer-shell/gtk-layer-shell.h>

GtkApplicationWindow *dshell_windows_corners_new(GtkApplication *app)
{
    GtkWidget *window = gtk_application_window_new(app);
    gtk_widget_add_css_class(window, "corners");
    gtk_widget_set_vexpand(window, true);

    gtk_layer_init_for_window(GTK_WINDOW(window));

    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_LEFT, true);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_TOP, true);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_RIGHT, true);
    gtk_layer_set_anchor(GTK_WINDOW(window), GTK_LAYER_SHELL_EDGE_BOTTOM, true);

    gtk_layer_set_layer(GTK_WINDOW(window), GTK_LAYER_SHELL_LAYER_BACKGROUND);

    gtk_layer_auto_exclusive_zone_enable(GTK_WINDOW(window));

    gtk_layer_set_keyboard_mode(GTK_WINDOW(window), GTK_LAYER_SHELL_KEYBOARD_MODE_NONE);


    return GTK_APPLICATION_WINDOW(window);
}
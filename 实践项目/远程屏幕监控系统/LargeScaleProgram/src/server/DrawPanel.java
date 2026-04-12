package server;

import javax.swing.JPanel;
import java.awt.Graphics;
import java.awt.image.BufferedImage;

public class DrawPanel extends JPanel {
    private BufferedImage image;

    public DrawPanel(BufferedImage image) {
        this.image = image;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (image != null) {
            g.drawImage(image, 0, 0, null);
        }
    }
}

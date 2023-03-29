import javax.swing.DefaultListModel;
import javax.swing.JFrame;
import javax.swing.JOptionPane;

public class myFrame extends JFrame {

    shared myShared = shared.getInstance();

    public myFrame() {
        init();
    }

    public myFrame(int width, int height) {
        init();
    }

    public static double getDistanceBetweenPointsNew(double latitude1, double longitude1, double latitude2,
            double longitude2, String unit) {
        double theta = longitude1 - longitude2;
        double distance = 60 * 1.1515 * (180 / Math.PI) * Math.acos(
                Math.sin(latitude1 * (Math.PI / 180)) * Math.sin(latitude2 * (Math.PI / 180)) +
                        Math.cos(latitude1 * (Math.PI / 180)) * Math.cos(latitude2 * (Math.PI / 180))
                                * Math.cos(theta * (Math.PI / 180)));
        if (unit.equals("miles")) {
            return Math.round(distance * 100) / 100;
        } else if (unit.equals("kilometers")) {
            return Math.round(distance * 1.609344 * 100) / 100;
        } else {
            return 0;
        }
    }

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) { // calculate button
        if (selectedFromPlace != null && selectedToPlace != null) {
            Double res = getDistanceBetweenPointsNew(selectedFromPlace.latitudine, selectedFromPlace.longitudine,
                    selectedToPlace.latitudine, selectedToPlace.longitudine, "kilometers");
            JOptionPane.showMessageDialog(this.getContentPane(), res.toString() + " Km");
        }

    }

    private void jTextField1ActionPerformed(java.awt.event.ActionEvent evt) { // text change from
        Thread t = new Thread() {
            @Override
            public void run() {
                lstModel = shared.getInstance().getResults(jTextField1.getText());
                jList1.setModel(lstModel);
                isSelectedFrom = true;
            }

        };
        t.start();
    }

    private void jTextField2ActionPerformed(java.awt.event.ActionEvent evt) { // text change to
        Thread t = new Thread() {
            @Override
            public void run() {
                lstModel = shared.getInstance().getResults(jTextField2.getText());
                jList1.setModel(lstModel);
                isSelectedFrom = false;

            }
        };
        t.start();

    }

    private void jList1MouseClicked(java.awt.event.MouseEvent evt) {
        if (evt.getClickCount() == 2 && !evt.isConsumed()) {
            evt.consume();
            if (jList1.getSelectedValue() != null) {
                Place p = jList1.getSelectedValue();
                if (isSelectedFrom == true) {
                    selectedFromPlace = p;
                    String txt = "";
                    if (p.town != null) {
                        txt += p.town;
                    } else if (p.city != null) {
                        txt += p.city;
                    } else if (p.village != null) {
                        txt += p.village;
                    } else if (p.display_name != null) {
                        txt += p.display_name;
                    } else if (p.county != null) {
                        txt += p.county;
                    }
                    if (p.country != null) {
                        txt += ", " + p.country;
                    } else if (p.state != null) {
                        txt += ", " + p.state;
                    }
                    jTextField1.setText(txt);
                    // jTextField1.setForeground(Color.BLUE);
                    // jTextField1.setEnabled(false);
                } else if (isSelectedFrom == false) {
                    selectedToPlace = p;
                    String txt = "";
                    if (p.town != null) {
                        txt += p.town;
                    } else if (p.city != null) {
                        txt += p.city;
                    } else if (p.village != null) {
                        txt += p.village;
                    } else if (p.display_name != null) {
                        txt += p.display_name;
                    } else if (p.county != null) {
                        txt += p.county;
                    }
                    if (p.country != null) {
                        txt += ", " + p.country;
                    } else if (p.state != null) {
                        txt += ", " + p.state;
                    }

                    jTextField2.setText(txt);
                    // jTextField2.setForeground(Color.BLUE);
                }
                // System.out.println("selected");
            }
            isSelectedFrom = null;
            lstModel.clear();

        }
    }

    public void init() {

        jTextField1 = new javax.swing.JTextField();
        jLabel1 = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        jTextField2 = new javax.swing.JTextField();
        jLabel2 = new javax.swing.JLabel();
        jScrollPane2 = new javax.swing.JScrollPane();
        jList1 = new javax.swing.JList<>();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        jList1.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                jList1MouseClicked(evt);
            }
        });

        jTextField1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jTextField1ActionPerformed(evt);
            }
        });

        jLabel1.setText("From:");

        jButton1.setText("CALCULATE");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        jTextField2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jTextField2ActionPerformed(evt);
            }
        });

        jLabel2.setText("To:");

        jScrollPane2.setViewportView(jList1);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                        .addComponent(jScrollPane2)
                                        .addGroup(layout.createSequentialGroup()
                                                .addGroup(layout
                                                        .createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING,
                                                                false)
                                                        .addGroup(layout.createSequentialGroup()
                                                                .addComponent(jLabel2)
                                                                .addGap(18, 18, 18)
                                                                .addComponent(jTextField2))
                                                        .addGroup(layout.createSequentialGroup()
                                                                .addComponent(jLabel1)
                                                                .addPreferredGap(
                                                                        javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                                                .addComponent(jTextField1,
                                                                        javax.swing.GroupLayout.PREFERRED_SIZE, 191,
                                                                        javax.swing.GroupLayout.PREFERRED_SIZE)))
                                                .addGap(18, 18, 18)
                                                .addComponent(jButton1)
                                                .addGap(0, 260, Short.MAX_VALUE)))
                                .addContainerGap()));
        layout.setVerticalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                                .addContainerGap()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                                        .addComponent(jTextField1, javax.swing.GroupLayout.PREFERRED_SIZE,
                                                javax.swing.GroupLayout.DEFAULT_SIZE,
                                                javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addComponent(jLabel1))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                                        .addComponent(jTextField2, javax.swing.GroupLayout.PREFERRED_SIZE,
                                                javax.swing.GroupLayout.DEFAULT_SIZE,
                                                javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addComponent(jLabel2)
                                        .addComponent(jButton1))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 354, Short.MAX_VALUE)
                                .addContainerGap()));

        pack();
    }

    // Variables declaration - do not modify
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JList<Place> jList1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTextField jTextField1;
    private javax.swing.JTextField jTextField2;
    public DefaultListModel<Place> lstModel = new DefaultListModel<Place>();
    public Place selectedFromPlace = null;
    public Place selectedToPlace = null;
    public Boolean isSelectedFrom = null;

    // End of variables declaration

}

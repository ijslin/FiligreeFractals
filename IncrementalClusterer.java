import weka.clusterers.ClusterEvaluation;
import weka.clusterers.EM;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import weka.core.Instances;
import weka.gui.visualize.*;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.awt.*;

import javax.swing.*;


/**
 * This example trains Cobweb incrementally on data obtained
 * from the ArffLoader.
 *
 */
public class IncrementalClusterer extends Component {

    //Get arff Link
    public static File getGui(){
        final JFileChooser fc = new JFileChooser();
        int returnVal = fc.showOpenDialog(fc);
        File file = fc.getSelectedFile();
        return file;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader breader;
        Instances Train;

        File arffInput = getGui();
        // load data
        breader = new BufferedReader(new FileReader(
                arffInput));

        Train = new Instances(breader);
        EM clusterer = new EM();
        clusterer.buildClusterer(Train);
        ClusterEvaluation eval = new ClusterEvaluation();
        eval.setClusterer(clusterer);
        eval.evaluateClusterer(Train);

        // setup visualization
        // taken from: ClustererPanel.startClusterer()
//        PlotData2D predData = ClustererPanel .;
        String name = (new SimpleDateFormat("HH:mm:ss - ")).format(new Date());
        String cname = clusterer.getClass().getName();
        if (cname.startsWith("weka.clusterers."))
            name += cname.substring("weka.clusterers.".length());
        else
            name += cname;

        VisualizePanel vp = new VisualizePanel();
        vp.setName(name + " (" + Train.relationName() + ")");
//        predData.setPlotName(name + " (" + Train.relationName() + ")");
//        vp.addPlot(predData);
//        vp.addPlot(clusterer);
        String plotName = vp.getName();
        final javax.swing.JFrame jf =
                new javax.swing.JFrame("Weka Clusterer Visualize: " + plotName);
        jf.setSize(500,400);
        jf.getContentPane().setLayout(new BorderLayout());
        jf.getContentPane().add(vp, BorderLayout.CENTER);

        jf.addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent e) {
                jf.dispose();
            }
        });
        jf.setVisible(true);


//         output generated model
        System.out.println(clusterer);
    }
}
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;


import javax.swing.DefaultListModel;

public class shared {
    //&polygon_geojson=1
    public final String APIURL = "https://nominatim.openstreetmap.org/search?q=%REPLACE%&format=xml&addressdetails=1&limit=5";// url
    public XMLParser xmlParser;

    // public HashMap<LocalDate, HashMap<String, Float>> listCube = new HashMap<>();
    // public String fileName = "value.xml";

    private static shared instance = null;

    private shared() {
        xmlParser = new XMLParser();
    }

    public static shared getInstance() {
        if (instance == null)
            instance = new shared();
        return instance;
    }

    public DefaultListModel<Place> getResults(String query) {
        DefaultListModel<Place> lst = new DefaultListModel<Place>();
        if (query.trim() != "") {
            String res = APIURL.replace("%REPLACE%", URLEncoder.encode(query, StandardCharsets.UTF_8));

            try {
                URL url = new URL(res);
                lst = xmlParser.getXMLQuery("results.xml", "place", url);

            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
            return lst;
        }
        return null;
    }

}

import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class shared {
    public final String APIURL = "https://nominatim.openstreetmap.org/search?q=%REPLACE%&format=xml&polygon_geojson=1&addressdetails=1";// url
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

    public List<Place> getResults(String query) {
        List<Place> lst = new ArrayList<>();
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

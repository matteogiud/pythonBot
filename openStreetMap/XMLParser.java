import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class XMLParser {
    DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder;
    Document document;
    Element root;
    NodeList nodeList;

    public XMLParser() {
    }

    public List<Place> getXMLQuery(String fileName, String tagName, URL url) {
        List<Place> ListPlace = new ArrayList<>();

        try {
            /**
             * creo l'url e salvo il file in locale
             */
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            PrintWriter out = new PrintWriter(fileName);
            String line = "";
            while ((line = in.readLine()) != null) {
                out.println(line);
            }
            in.close();
            out.close();

            builder = documentBuilderFactory.newDocumentBuilder();
            document = builder.parse(fileName);
            root = document.getDocumentElement();
            nodeList = root.getElementsByTagName(tagName);

            if (nodeList != null && nodeList.getLength() > 0) {

                int numEl = nodeList.getLength();
                for (int i = 0; i < numEl; i++) {
                    Node node = nodeList.item(i);
                    Element nodoElement = (Element) node;
                    

                    // #region campi
                    
                        Place place = new Place();
                        if (nodoElement.hasAttribute("lon"))
                            place.longitudine = Double.parseDouble(nodoElement.getAttribute("lon"));
                        if (nodoElement.hasAttribute("lat"))
                            place.latitudine = Double.parseDouble(nodoElement.getAttribute("lon"));
                        NodeList childNodeList = nodoElement.getChildNodes();
                        int numEl2 = childNodeList.getLength();
                        for (int j = 0; j < numEl2; j++) {
                            if (childNodeList.item(j).getNodeType() == Element.ELEMENT_NODE) {
                                Element childElementNode = (Element) childNodeList.item(j);
                                String tagNameChild = childElementNode.getNodeName();
                                //System.out.println(tagNameChild);
                                if (tagNameChild.equals("building"))
                                    place.building = childElementNode.getTextContent();
                                else if (tagNameChild.equals("road"))
                                    place.road = childElementNode.getTextContent();
                                else if (tagNameChild.equals("village"))
                                    place.village = childElementNode.getTextContent();
                                else if (tagNameChild.equals("town"))
                                    place.town = childElementNode.getTextContent();
                                else if (tagNameChild.equals("county"))
                                    place.county = childElementNode.getTextContent();
                                else if (tagNameChild.equals("state"))
                                    place.state = childElementNode.getTextContent();
                                else if (tagNameChild.equals("postcode"))
                                    place.postcode = Integer.parseInt(childElementNode.getTextContent());
                                else if (tagNameChild.equals("country"))
                                    place.country = childElementNode.getTextContent();
                                else if (tagNameChild.equals("country_code"))
                                    place.country_code = childElementNode.getTextContent();
                            }
                        }

                        ListPlace.add(place);
                    
                    // #endregion

                }
            }
        } catch (Exception e) {
            return null;
        }
        System.out.println(ListPlace.toString());

        return ListPlace;

    }

    public HashMap<LocalDate, HashMap<String, Float>> getListSpecific(URL url, String fileName, String rootName)
            throws MalformedURLException {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            PrintWriter out = new PrintWriter(fileName);
            String line = "";
            while ((line = in.readLine()) != null) {
                out.println(line);
            }
            in.close();
            out.close();

            builder = documentBuilderFactory.newDocumentBuilder();
            document = builder.parse(fileName);
            root = document.getDocumentElement();
            nodeList = root.getElementsByTagName(rootName);
            HashMap<LocalDate, HashMap<String, Float>> lst = new HashMap<>();

            if (nodeList != null && nodeList.getLength() > 0) {
                try {
                    int numEl = nodeList.getLength();
                    for (int i = 0; i < numEl; i++) {
                        try {
                            Node node = nodeList.item(i);
                            Element nodoElement = (Element) node;
                            if (node.getNodeName().equals("Cube") == false || nodoElement.hasAttributes() == false)// controlli
                                throw new Exception();

                            // #region campi

                            if (nodoElement.hasAttribute("time")) {
                                LocalDate date = LocalDate.parse(nodoElement.getAttribute("time"));
                                HashMap<String, Float> hMap = new HashMap<>();

                                NodeList nodeList2 = nodoElement.getChildNodes();
                                int numEl2 = nodeList2.getLength();

                                for (int j = 0; j < numEl2; j++) {
                                    Node node2 = nodeList2.item(j);
                                    Element nodoElement2 = (Element) node2;
                                    if (nodoElement2.hasAttribute("currency") && nodoElement2.hasAttribute("rate")) {

                                        String curr = nodoElement2.getAttribute("currency");
                                        Float rate = Float.parseFloat(nodoElement2.getAttribute("rate"));
                                        hMap.put(curr, rate);// salvo le curr e rate su un hashmap che poi sarà salvato
                                                             // sull'hashmap principale
                                    }
                                }

                                lst.put(date, hMap);// salvo il cube contenente date

                            }
                        } catch (Exception e) {

                        }

                        // #endregion

                    }
                } catch (Exception e) {

                }
            } else
                return null;
            return lst;
        } catch (Exception e) {
            return null;
        }

    }
}

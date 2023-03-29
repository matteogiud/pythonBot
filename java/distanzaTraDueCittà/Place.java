public class Place {
    public String building;
    public String city;
    public String road;
    public String village;
    public String town;
    public String county;
    public String state;
    public int postcode = 0;
    public String country;
    public String country_code;
    public double latitudine;
    public double longitudine;
    public String display_name;

    public Place() {
    }

    public Place(String building, String road, String village, String town, String county, String state, int postcode,
            String country, String country_code, double latitudine, double longitudine, String display_name) {
        this.building = building;
        this.road = road;
        this.village = village;
        this.town = town;
        this.county = county;
        this.state = state;
        this.postcode = postcode;
        this.country = country;
        this.country_code = country_code;
        this.latitudine = latitudine;
        this.longitudine = longitudine;
        this.display_name = display_name;
    }

    @Override
    public String toString() {
        String Name = display_name == null ? "" : "Name: " + display_name + " ";
        String Village = village == null ? "" : "Village: " + village + " ";
        String State = state == null ? "" : "State: " + state + " ";
        String PostCode = postcode == 0 ? "" : "Postcode: " + postcode + " ";
        String Country = country == null ? "" : "Country: " + country + " ";
        String County = county == null ? "" : "County: " + county + " ";
        String Town = town == null ? "" : "Town: " + town + " ";

        return Name +  Village + State + PostCode + Country + County + Town;
    }
}

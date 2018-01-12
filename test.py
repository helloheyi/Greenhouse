  #!wing
#!version=6.0
##################################################################
# Wing IDE project file                                          #
##################################################################
[project attributes]
proj.directory-list = [{'dirloc': loc('../../../Documents/WS'),
                        'excludes': (),
                        'filter': u'*',
                        'include_hidden': False,
                        'recursive': True,
                        'watch_for_changes': True}]
proj.file-type = 'shared'
Redshift:
    user : "hang"
    pw : "Woaijianada1026+"
    host : "pantheon-dw.c9qtpydth0xz.us-east-1.redshift.amazonaws.com"
    port : "5439"
    db : "production"




####third change
/**
    * Create a Point class to represent any point in a Cartesian coordinate system.
        * The following instance methods must be supported:
            *
                * @author Yi.He
                    *
                        */

// make variables
public class Point {
    private int ID;
    private double x;
    private double y;
    private int countPoint = 0;
    private static int countActiveNumber = 0;
    
    /**
        * 1.constructor: one that allows you to specify the x and y coordinates of
            * the point, and one that initializes the coordinates to 0.0.
                *
                    * @param x
                        *            the value of x
                            * @param y
                                *            the value of y
                                    */

// two constructors
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
        countPoint++;
        this.ID = countPoint;
        countActiveNumber++;
}

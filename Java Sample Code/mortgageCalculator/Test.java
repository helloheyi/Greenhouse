package mortgageCalculator;
/**
 * Test class to actually run the Mortgage Calculator program.
 * @author yihe
 *
 */

public class Test {
	//This is main method to start the program.
	public static void main(String[] args) {
		View myView= new View();
		Mortgage myMortgage = new Mortgage();
		myView.setVisible(true);
		Controller aController = new Controller(myView, myMortgage);

	}

}

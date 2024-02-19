package mortgageCalculator;

import java.awt.event.*;

/**
 * The main Controller for the program. All my listeners go here
 * 
 * @author yihe
 *
 */

public class Controller {
	private View myView;
	private Mortgage myMortgage;

	/**
	 * This the constructor for the controller, the controller can link the View
	 * class and Mortgage class
	 * 
	 * @param myView
	 *            myView is an object from my View class
	 * @param myMortgage
	 *            myMortgage is an object from my Mortgage class
	 */

	public Controller(View myView, Mortgage myMortgage) {
		this.myView = myView;
		this.myMortgage = myMortgage;

		// Attach listeners using methods from the View
		myView.addWindowListener(new myWindowAdapter());
		myView.attachComboBoxListener(new myComboBoxListener());
		myView.attachRadioButtonListener(new myRadioButtonListener());
		myView.attachButtonListener(new myButtonListener());

	}

	// This is the one of WindowEvents
	private class myWindowAdapter extends WindowAdapter {
		public void windowClosing(WindowEvent e) {

			// If we close the JFrame window, exit the program.
			System.exit(0);
		}
	}

	// This is the handler for my Calculate button.
	// After chick the button the results will display
	private class myButtonListener implements ActionListener {
		@Override
		public void actionPerformed(ActionEvent e) {

			myMortgage.setPrincipal(myView.getInputOfPrincipal());
			myMortgage.setRate(myView.getInputOfRate());
			myMortgage.setnumberOfMonthlyPayments(myView.getNumberOfPayments());
			myView.monthlyPayment.setText(String.format(" The monthlyPayment: $%.2f ", myMortgage.amountOfpayment()));
			myView.totalInterest.setText(String.format(" The total interest : $%.2f", myMortgage.totalInterest()));
			myView.totalPrincipal
					.setText(String.format(" The total interest and principal : $%.2f", myMortgage.total()));
			myView.interestRatio.setText(
					String.format(" The precentage of interest/principal ratio is : %.2f ", myMortgage.ratio()));
			myView.interestPerYear.setText(
					String.format(" The average interest paid per month is : $%.2f", myMortgage.paidMonthly()));
			myView.interestPerMonth
					.setText(String.format(" The average interest paid per year is : $%.2f", myMortgage.paidYear()));
			myView.amortizationOfYear.setText(
					String.format(" The amortization expressed in years is: %.2f", myMortgage.amortizationYears()));

		}
	}

	// This is the handler for my PaymentFrequency combo box.
	// The user can choose one of options for the frequency
	private class myComboBoxListener implements ActionListener {
		@Override
		public void actionPerformed(ActionEvent e) {
			myMortgage.setPaymentFrequency(myView.getSelectedComboBox());

		}
	}

	// This is the handler for my interest compounding frequency radio buttons.
	// Store selected interest compounding frequency option
	private class myRadioButtonListener implements ActionListener {
		@Override
		public void actionPerformed(ActionEvent e) {
			myMortgage.setCompoundingFrequency(e.getActionCommand());
		}
	}

	/**
	 * Method to change String to double
	 * 
	 * @param stringObject
	 *            This is the String Object
	 * @return double value
	 */
	public static double stringtoDouble(String stringObject) {
		return Double.parseDouble(stringObject.trim());
	}

}

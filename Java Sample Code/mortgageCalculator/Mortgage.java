package mortgageCalculator;

/**
 * Mortgage class, this is the Model which stores everything about my mortgage
 * 
 * @author yihe
 *
 */
public class Mortgage {

	private double numberOfMonthlyPayments = 0;
	private double principal;
	private double rate;
	private double frequency = 12;
	private double compoundingFrequency = 2;

	/**
	 * The constructor of the Mortgage class
	 */

	public Mortgage() {
		this.numberOfMonthlyPayments = 12;
	}

	/**
	 * set the annual interest rate
	 * 
	 * @param rate
	 *            The annual interest rate as a double
	 */
	// set rate
	public void setRate(double rate) {
		this.rate = rate;
	}

	/**
	 * get the annual interest rate
	 * 
	 * @return The annual interest rate as a double
	 */
	// get the number of payment's rate
	public double getRate() {
		return this.rate;
	}

	/**
	 * set the number of monthly payments
	 * 
	 * @param numberOfMonthlyPayments
	 *            how many month you want to paid
	 */

	// set the number of monthly payments
	public void setnumberOfMonthlyPayments(double numberOfMonthlyPayments) {
		this.numberOfMonthlyPayments = numberOfMonthlyPayments;
	}

	// get the number of monthly payments
	/**
	 * get the number of monthly payments for the loan
	 * 
	 * @return the number of monthly payments for the loan
	 */
	public double getnumberOfMonthlyPayments() {
		return this.numberOfMonthlyPayments;
	}

	/**
	 * set the the number of principal
	 * 
	 * @param principal
	 *            how many money you want to loan
	 */
	// set the principal how many money you want to loan
	public void setPrincipal(double principal) {
		this.principal = principal;
	}

	// get the principal how many money you want to loan
	/**
	 * get the principal how many money you want to loan
	 * 
	 * @return how many money you want to loan
	 */
	public double getPrincipal() {
		return this.principal;
	}

	/**
	 * Set the number of interest compounding frequency
	 * 
	 * @param compoundingFrequency
	 *            we change the string of the compounding frequency to the
	 *            number
	 */
	public void setCompoundingFrequency(String compoundingFrequency) {
		if (compoundingFrequency.equals("daily")) {
			this.compoundingFrequency = 365;
		} else if (compoundingFrequency.equals("weekly")) {
			this.compoundingFrequency = 52;
		} else if (compoundingFrequency.equals("monthly")) {
			this.compoundingFrequency = 12;
		} else if (compoundingFrequency.equals("semi-annually")) {
			this.compoundingFrequency = 2;
		}

	}

	/**
	 * Set the number of payment frequency
	 * 
	 * @param paymentFrequency
	 *            we change the string of the frequency to the number
	 */
	public void setPaymentFrequency(String paymentFrequency) {
		if (paymentFrequency.equals("monthly")) {
			this.frequency = 12;
		} else if (paymentFrequency.equals("bi-weekly")) {
			this.frequency = 26;
		} else if (paymentFrequency.equals("weekly")) {
			this.frequency = 52;
		}
	}

	/**
	 * Calculate the interest factor
	 * 
	 * @param frequency
	 *            the frequency of payments per year
	 * @param compoundingFrequency
	 *            compounding frequency per year
	 * @return the interest factor
	 */

	// calculate interest factor
	public double rate(double frequency, double compoundingFrequency) {
		return Math.pow(((rate / 100) / compoundingFrequency) + 1, (double) compoundingFrequency / frequency) - 1;
	}

	/**
	 * calculate the amount of the periodic blended payment(principal +
	 * interest)
	 * 
	 * @return the amount of the periodic blended payment(principal + interest)
	 */
	// calculate blended monthly payment
	public double amountOfpayment() {
		double denominator = (principal * this.rate(frequency, compoundingFrequency));
		double numerator = 1 - Math.pow(this.rate(frequency, compoundingFrequency) + 1, (-1) * numberOfMonthlyPayments);
		return denominator / numerator;
	}

	/**
	 * calculate the total interest
	 * 
	 * @return the total interest paid over the length of the mortgage
	 */
	// total interest paid
	public double totalInterest() {
		return this.amountOfpayment() * numberOfMonthlyPayments - principal;

	}

	/**
	 * calculate the total interest and principal
	 * 
	 * @return the total interest and principal
	 */
	// total interest and principal
	public double total() {
		return this.amountOfpayment() * numberOfMonthlyPayments;

	}
	
	/**
	 * calculate the interest/principal ratio
	 * @return the interest/principal ratio
	 */

	// The interest/principal ratio

	public double ratio() {
		double ratio = this.totalInterest() / principal;
		return ratio * 100;

	}
	
	/**
	 * calculate the average interest paid per year
	 * @return /the average interest paid per year
	 */

	public double paidYear() {
		return this.totalInterest() / (numberOfMonthlyPayments / 12);
	}

	/**
	 * calculate the average interest paid per month
	 * @return the average interest paid per month
	 */
	public double paidMonthly() {
		return this.totalInterest() / (numberOfMonthlyPayments);
	}

	/**
	 * calculate the amortization expressed in years
	 * @return the amortization expressed in years
	 */
	public double amortizationYears() {
		return numberOfMonthlyPayments / 12;

	}

}

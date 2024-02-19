package mortgageCalculator;

import javax.swing.JFrame;
import javax.swing.JTextField;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JLabel;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JTextArea;

import java.awt.Dimension;
import java.awt.GridLayout;

import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;

/**
 * This is GUI. It extends JFrame to create a window, and all of layouts and
 * elements are defined here. I also need get/set methods to manipulate the
 * values in my elements (label text, text fields, etc.). Also, I use some
 * methods which allow my Controller to attach listeners to my elements.
 * 
 * @author yihe
 *
 */
public class View extends JFrame {

	// use the label to explain the input
	private JLabel explainOfPayment = new JLabel("Principal");
	private JLabel explainOfPrincipal = new JLabel("Number of monthly payments");
	private JLabel explainOfRate = new JLabel("The precentage of Annual interest rate ");

	// use textField for input
	private JTextField inputOfPrincipal = new JTextField();
	private JTextField inputOfNumber = new JTextField();
	private JTextField inputOfRate = new JTextField();

	// set calculate button
	public JButton button = new JButton("Calculate");

	// use label to show output
	protected JLabel monthlyPayment = new JLabel();
	protected JLabel totalInterest = new JLabel();;
	protected JLabel totalPrincipal = new JLabel();;
	protected JLabel interestRatio = new JLabel();;
	protected JLabel interestPerYear = new JLabel();
	protected JLabel interestPerMonth = new JLabel();
	protected JLabel amortizationOfYear = new JLabel();

	// use JComboBox to choose monthly, bi-weekly, weekly
	private JLabel frequency = new JLabel("Frequency of payments:");
	private String[] paymentFrequencyStrings = { "weekly", "bi-weekly", "monthly" };
	private JComboBox<String> cbPaymentFrequency = new JComboBox<String>(paymentFrequencyStrings);

	// use ButtonGruop to compounding frequency button
	private JLabel compoundOfFrequency = new JLabel("Compounding frequency:");
	private ButtonGroup compoundFrequency = new ButtonGroup();
	private JRadioButton compoundFrequencyDaily = new JRadioButton("daily");
	private JRadioButton compoundFrequencyWeekly = new JRadioButton("weekly");
	private JRadioButton compoundFrequencyMonthly = new JRadioButton("monthly");
	private JRadioButton compoundFrequencySemiAnnual = new JRadioButton("semi-annually", true);
	
	// cretae JComboBox to choose monthly, semi-annually, annually
	private JLabel amortization = new JLabel("Amortization Schedule: ");
	private String[] amortizationSchedule = { "monthly", "semi-annually", "annually" };
	private JComboBox<String> cbAmortizationSchedule = new JComboBox<String>(amortizationSchedule);

	public View() {
		// set the properties of window
		// note the grid layout; 2 rows, 1 column, 20 padding
		this.setTitle("Simplified mortgageCalculator");
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setSize(1000, 1000);
		this.setLayout(new GridLayout(3, 1, 10, 20));

		// create a table on Panel
		// create a label and combo box.
		String[] columnNames = { "Blended Payment", "Interest Component", "Principal Component", "New Balance Owing" };
		Object[][] data = {};
		JPanel schedule = new JPanel();
		final JTable table = new JTable(data, columnNames);
		table.setPreferredScrollableViewportSize(new Dimension(500, 200));
		table.setFillsViewportHeight(true);
		JScrollPane scrollPane = new JScrollPane(table);
		schedule.add(amortization);
		schedule.add(cbAmortizationSchedule);
		schedule.add(scrollPane);
		this.add(schedule);
		cbAmortizationSchedule.setSelectedIndex(2);

		// the Frame contains 6 panels
		JPanel comboBoxPanel = new JPanel();
		JPanel radioPanel = new JPanel();
		JPanel explain = new JPanel();
		JPanel textPanel = new JPanel();
		JPanel outPut = new JPanel();
		JPanel otherPanel = new JPanel(new GridLayout(2, 2, 20, 20));

		// set the layouts for the 5 JPanels
		comboBoxPanel.setLayout(new GridLayout(1, 2));
		radioPanel.setLayout(new GridLayout(5, 1));
		explain.setLayout(new GridLayout(3, 0));
		textPanel.setLayout(new GridLayout(3, 1));
		outPut.setLayout(new GridLayout(8, 1));

		// Add all radio buttons to a group, so that only one option can be
		// selected
		// and choose the 2 is default option
		compoundFrequency.add(compoundFrequencyDaily);
		compoundFrequency.add(compoundFrequencyWeekly);
		compoundFrequency.add(compoundFrequencyMonthly);
		compoundFrequency.add(compoundFrequencySemiAnnual);
		cbPaymentFrequency.setSelectedIndex(2);

		// add frequency to the JPanels
		comboBoxPanel.add(frequency);
		comboBoxPanel.add(cbPaymentFrequency);

		// add compounding to the JPanels
		radioPanel.add(compoundOfFrequency);
		radioPanel.add(compoundFrequencyDaily);
		radioPanel.add(compoundFrequencyWeekly);
		radioPanel.add(compoundFrequencyMonthly);
		radioPanel.add(compoundFrequencySemiAnnual);

		// add labels to explain the input to JPanels
		explain.add(explainOfPayment);
		explain.add(explainOfPrincipal);
		explain.add(explainOfRate);

		// add text to JPanels
		textPanel.add(inputOfPrincipal);
		textPanel.add(inputOfNumber);
		textPanel.add(inputOfRate);

		// add output elements to JPanels
		outPut.add(button);
		outPut.add(monthlyPayment);
		outPut.add(totalInterest);
		outPut.add(totalPrincipal);
		outPut.add(interestRatio);
		outPut.add(interestPerYear);
		outPut.add(interestPerMonth);
		outPut.add(amortizationOfYear);

		// Add all our JPanels to the JFrame window
		otherPanel.add(explain);
		otherPanel.add(textPanel);
		otherPanel.add(comboBoxPanel);
		otherPanel.add(radioPanel);
		this.add(otherPanel);
		this.add(outPut);

	}

	/**
	 * Method for Controller to attach a listener to the JFrame window
	 * 
	 * @param myWindowAdapter
	 *            The event handler for window
	 */
	public void attachWindowListener(WindowAdapter myWindowAdapter) {
		this.addWindowListener(myWindowAdapter);
	}

	/**
	 * Method for Controller to a listener to the combo box
	 * 
	 * @param myCBHandler
	 *            The event handler for combo box
	 */
	public void attachComboBoxListener(ActionListener myCBHandler) {
		cbPaymentFrequency.addActionListener(myCBHandler);
	}

	/**
	 * Method for Controller to a listener to the combo box for the schedule
	 * 
	 * @param myCBHandler
	 *            The event handler for combo box for the schedule
	 */
	public void attachComboListener(ActionListener myCBHandler) {
		cbAmortizationSchedule.addActionListener(myCBHandler);
	}

	/**
	 * Method for Controller to attach a listener to the radio buttons
	 * 
	 * @param myRadioHandler
	 *            The event handler for the radio buttons.
	 */
	public void attachRadioButtonListener(ActionListener myRadioHandler) {
		compoundFrequencyDaily.addActionListener(myRadioHandler);
		compoundFrequencyWeekly.addActionListener(myRadioHandler);
		compoundFrequencyMonthly.addActionListener(myRadioHandler);
		compoundFrequencySemiAnnual.addActionListener(myRadioHandler);
	}

	/**
	 * Method for my Controller to attach a listener to the Calculate button
	 * 
	 * @param myButtonHandler
	 *            The event handler for the Calculate button
	 */
	public void attachButtonListener(ActionListener myButtonHandler) {
		button.addActionListener(myButtonHandler);
	}

	/**
	 * Method to get the input for the number of monthly payments
	 * 
	 * @return The number of payments entered by the user, parsed as an integer
	 */
	public int getNumberOfPayments() {
		return Integer.parseInt(this.inputOfNumber.getText());
	}

	/**
	 * Method to get the input for the principal
	 * 
	 * @return The number of principal entered by the user, parsed as double
	 */
	public double getInputOfPrincipal() {
		return Double.parseDouble(this.inputOfPrincipal.getText());
	}

	/**
	 * Method to get the input for the rate
	 * 
	 * @return The number of rate entered by the user, parsed as double
	 */
	public double getInputOfRate() {
		return Double.parseDouble(this.inputOfRate.getText());
	}

	/**
	 * Method to get the payment frequency
	 * 
	 * @return The user can choose the frequency to paid the loan.
	 */
	public String getSelectedComboBox() {
		return this.cbPaymentFrequency.getSelectedItem().toString();
	}

}

package greenHouse;

import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GridLayout;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

/**
 * This class is the temperature view.
 * 
 * @author yihe
 *
 */
public class TempView extends JPanel {

	// use the label to explain the input

	// currentTemp is an output
	protected JLabel lblCurrentTemp = new JLabel("Current Temperature(�C)");
	protected JLabel lblDesiredTemp = new JLabel("Desired Temperature(�C)");
	protected JLabel lblCoolingRate = new JLabel("Cooling (�C/Min)");
	protected JLabel lblHeatingRate = new JLabel("Heating (�C/Min)");
	protected JLabel lblRefreshRate = new JLabel("Refresh Rate(seconds)");
	protected JLabel lblFurnaceStatus = new JLabel("Furnace on/off");
	protected JLabel lblACStatus = new JLabel("Air Conditioner on/off");

	// use textField for input
	protected JTextField txtCurrentTemp = new JTextField();
	protected JTextField txtDesiredTemp = new JTextField();
	protected JTextField txtCoolingRate = new JTextField();
	protected JTextField txtHeatingRate = new JTextField();
	protected JTextField txtRefreshRate = new JTextField();

	// use label to explain the output
	protected JLabel lblFurnaceStatusValue = new JLabel();
	protected JLabel lblACStatusValue = new JLabel();

	public TempView() {

		// set properties of panel
		this.setSize(300, 300);
		this.setLayout(new GridLayout(7, 1));
		this.setBorder(new EmptyBorder(10, 10, 10, 10));

		// add components to the temperature JPanel

		// create current temperature panel
		JPanel currentTempPanel = new JPanel();
		currentTempPanel.setLayout(new GridLayout(2, 1));
		currentTempPanel.add(lblCurrentTemp);
		currentTempPanel.add(txtCurrentTemp);

		// create desired temperature panel
		JPanel desiredTempPanel = new JPanel();
		desiredTempPanel.setLayout(new GridLayout(2, 1));
		desiredTempPanel.add(lblDesiredTemp);
		desiredTempPanel.add(txtDesiredTemp);

		// create the heating rate Panel
		JPanel heatingRatePanel = new JPanel();
		heatingRatePanel.setLayout(new GridLayout(2, 1));
		heatingRatePanel.add(lblHeatingRate);
		heatingRatePanel.add(txtHeatingRate);

		// create the cooling rate panel
		JPanel coolingRatePanel = new JPanel();
		coolingRatePanel.setLayout(new GridLayout(2, 1));
		coolingRatePanel.add(lblCoolingRate);
		coolingRatePanel.add(txtCoolingRate);

		// create the refresh rate panel
		JPanel refreshRatePanel = new JPanel();
		refreshRatePanel.setLayout(new GridLayout(2, 1));
		refreshRatePanel.add(lblRefreshRate);
		refreshRatePanel.add(txtRefreshRate);

		// create the furnace status panel
		JPanel furnaceStatusPanel = new JPanel();
		furnaceStatusPanel.setLayout(new GridLayout(2, 1));
		furnaceStatusPanel.add(lblFurnaceStatus);
		furnaceStatusPanel.add(lblFurnaceStatusValue);

		// create the air conditionor status panel
		JPanel acStatusPanel = new JPanel();
		acStatusPanel.setLayout(new GridLayout(2, 1));
		acStatusPanel.add(lblACStatus);
		acStatusPanel.add(lblACStatusValue);

		// add these panel to the temperature panel
		this.add(currentTempPanel);
		this.add(desiredTempPanel);
		this.add(heatingRatePanel);
		this.add(coolingRatePanel);
		this.add(refreshRatePanel);
		this.add(furnaceStatusPanel);
		this.add(acStatusPanel);
	}
}
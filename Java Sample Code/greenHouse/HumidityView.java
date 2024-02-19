package greenHouse;

import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GridLayout;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

/**
 * The class of humidity view.
 * @author yihe xinyin
 *
 */
public class HumidityView extends JPanel {
	
	// use the label to explain the input
	protected JLabel lblCurrentHumidity = new JLabel("Current Humidity(%)");
	protected JLabel lblDesiredHumidityMax = new JLabel(" Desired Max Humidity(%) ");
	protected JLabel lblDesiredHumidityMin = new JLabel(" Desired Min Humidity(%)");
	protected JLabel lblHumidityRate = new JLabel("Humidity Change Rate(% Min)");
	protected JLabel lblRefreshRate = new JLabel("Refresh Rate(seconds)");
	protected JLabel lblHumifierStatus = new JLabel("Humidifier off/on outPut");
	
	// use textField for input
	protected JTextField txtCurrentHumidity = new JTextField();
	protected JTextField txtDesiredHumidityMax= new JTextField();
	protected JTextField txtDesiredHumidityMin= new JTextField();
	protected JTextField txtHumidityRate = new JTextField();
	protected JTextField txtRefreshRate = new JTextField();

	// use label to explain the output
	protected JLabel lblHumidifierStatusValue = new JLabel();
	
	//protected JPanel humPanel;
	public HumidityView() {
		
		// set properties of panel
		this.setSize(300, 300);
		this.setLayout(new GridLayout(7,1));
		this.setBackground(Color.gray);
		this.setBorder(new EmptyBorder(10, 10, 10, 10));
		
		// create a initial humidity panel 
		JPanel initialHumidityPanel = new JPanel();
		initialHumidityPanel.setLayout(new GridLayout(2,1));
		initialHumidityPanel.add(lblCurrentHumidity);
		initialHumidityPanel.add(txtCurrentHumidity);
		initialHumidityPanel.setBackground(Color.gray);
		
		// create a desired humidity max panel
		JPanel desiredHumidityMaxPanel = new JPanel();
		desiredHumidityMaxPanel.setLayout(new GridLayout(2,1));
		desiredHumidityMaxPanel.add(lblDesiredHumidityMax);
		desiredHumidityMaxPanel.add(txtDesiredHumidityMax);
		desiredHumidityMaxPanel.setBackground(Color.gray);
		
		//create a desired humidity min panel 
		JPanel desiredHumidityMinPanel = new JPanel();
		desiredHumidityMinPanel.setLayout(new GridLayout(2,1));
		desiredHumidityMinPanel.add(lblDesiredHumidityMin);
		desiredHumidityMinPanel.add(txtDesiredHumidityMin);
		desiredHumidityMinPanel.setBackground(Color.gray);
		
		// create a humidity rate a panel.
		JPanel humidityRatePanel = new JPanel();
		humidityRatePanel.setLayout(new GridLayout(2,1));
		humidityRatePanel.add(lblHumidityRate);
		humidityRatePanel.add(txtHumidityRate);
		humidityRatePanel.setBackground(Color.gray);
		
		// create a refresh rate panel 
		JPanel refreshRatePanel = new JPanel();
		refreshRatePanel.setLayout(new GridLayout(2,1));
		refreshRatePanel.add(lblRefreshRate);
		refreshRatePanel.add(txtRefreshRate);
		refreshRatePanel.setBackground(Color.gray);
		
		// create a hunidifier status panel 
		JPanel humidiferStatusPanel = new JPanel();
		humidiferStatusPanel.setLayout(new GridLayout(2,1));
		humidiferStatusPanel.add(lblHumifierStatus);
		humidiferStatusPanel.add(lblHumidifierStatusValue);
		humidiferStatusPanel.setBackground(Color.gray);
		
		// add these panel to humidity view
		this.add(initialHumidityPanel);
		this.add(desiredHumidityMaxPanel);
		this.add(desiredHumidityMinPanel);
		this.add(humidityRatePanel);
		this.add(refreshRatePanel);
		this.add(humidiferStatusPanel);
	}
}
package greenHouse;

import java.awt.Color;

import java.awt.FlowLayout;

import java.awt.GridLayout;

import javax.swing.JLabel;

import javax.swing.JPanel;

import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;
/**
 * This is class for moisture view
 * @author yihe
 *
 */
public class MoistureView extends JPanel {
	
	// use the label to explain the input
	protected JLabel lblCurrentMoisture = new JLabel("Current Moisture(%)");
	protected JLabel lblDesiredMoistureMax = new JLabel(" Desired Max Moisture(%) ");
	protected JLabel lblDesiredMoistureMin = new JLabel(" Desired Min Moisture(%)");
	protected JLabel lblMoistureRate = new JLabel("Moisture Change Rate(% Min)");
	protected JLabel lblRefreshRate = new JLabel("Refresh Rate(seconds)");
	protected JLabel lblSprinklerStatus = new JLabel("Sprinkler off/on");

	// use textField for input
	protected JTextField txtCurrentMoisture = new JTextField();
	protected JTextField txtDesiredMoistureMax = new JTextField();
	protected JTextField txtDesiredMoistureMin = new JTextField();
	protected JTextField txtMoistureRate = new JTextField();
	protected JTextField txtRefreshRate = new JTextField();

	// use label to explain the output
	protected JLabel lblSprinklerStatusValue = new JLabel();

	// this the constructor for moisture view
	public MoistureView() {
		
		// set properties of panel
		this.setSize(300, 300);
		this.setLayout(new GridLayout(7, 1));
		this.setBackground(Color.gray);
		this.setBorder(new EmptyBorder(10, 10, 10, 10));

		// create initial Moisture Panel
		JPanel initialMoisturePanel = new JPanel();
		initialMoisturePanel.setLayout(new GridLayout(2, 1));
		initialMoisturePanel.add(lblCurrentMoisture);
		initialMoisturePanel.add(txtCurrentMoisture);
		initialMoisturePanel.setBackground(Color.gray);
		
		// create desired moisture max panel
		JPanel desiredMoistureMaxPanel = new JPanel();
		desiredMoistureMaxPanel.setLayout(new GridLayout(2, 1));
		desiredMoistureMaxPanel.add(lblDesiredMoistureMax);
		desiredMoistureMaxPanel.add(txtDesiredMoistureMax);
		desiredMoistureMaxPanel.setBackground(Color.gray);

		// create desired moisture min panel
		JPanel desiredMoistureMinPanel = new JPanel();
		desiredMoistureMinPanel.setLayout(new GridLayout(2, 1));
		desiredMoistureMinPanel.add(lblDesiredMoistureMin);
		desiredMoistureMinPanel.add(txtDesiredMoistureMin);
		desiredMoistureMinPanel.setBackground(Color.gray);
		
		// create moisture rate panel
		JPanel moistureRatePanel = new JPanel();
		moistureRatePanel.setLayout(new GridLayout(2, 1));
		moistureRatePanel.add(lblMoistureRate);
		moistureRatePanel.add(txtMoistureRate);
		moistureRatePanel.setBackground(Color.gray);
		
		// create refresh rate panel 
		JPanel refreshRatePanel = new JPanel();
		refreshRatePanel.setLayout(new GridLayout(2, 1));
		refreshRatePanel.add(lblRefreshRate);
		refreshRatePanel.add(txtRefreshRate);
		refreshRatePanel.setBackground(Color.gray);
		
		//create sprinkler status panel 
		JPanel sprinklerStatusPanel = new JPanel();
		sprinklerStatusPanel.setLayout(new GridLayout(2, 1));
		sprinklerStatusPanel.add(lblSprinklerStatus);
		sprinklerStatusPanel.add(lblSprinklerStatusValue);
		sprinklerStatusPanel.setBackground(Color.gray);
		
		// add these panel to the moisture model
		this.add(initialMoisturePanel);
		this.add(desiredMoistureMaxPanel);
		this.add(desiredMoistureMinPanel);
		this.add(moistureRatePanel);
		this.add(refreshRatePanel);
		this.add(sprinklerStatusPanel);

	}

}
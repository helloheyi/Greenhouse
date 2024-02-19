package greenHouse;

import java.awt.Component;

import java.awt.GridLayout;

import javax.swing.JButton;

import javax.swing.JFrame;

import javax.swing.JLabel;

import javax.swing.JPanel;

import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

/**
 * This class is the environment view
 * 
 * @author yihe xinyin
 *
 */
public class EnvironmentView extends JPanel {

	// use the label to explain the input
	public JLabel lblEnvironmentTemperature = new JLabel(" Evironment temperature (�C)");
	public JLabel lblEnvironmentHumidity = new JLabel(" Evironment humidity (%)");
	public JLabel lblEnvironmentMoisture = new JLabel(" Evironment soil moisture(%)");
	public JLabel lblEnvTempEffect = new JLabel(" Temperature effect (�C/Min )");
	public JLabel lblEnvHumidityEffect = new JLabel(" Humidity effect (%/Min)");
	public JLabel lblEnvMoistureEffect = new JLabel(" Moisture effect (%/Min)");

	// use textField for input
	public JTextField txtEnvironmentTemperature = new JTextField();
	public JTextField txtEnvironmentHumidity = new JTextField();
	public JTextField txtEnvironmentMoisture = new JTextField();
	public JTextField txtEnvTempEffect = new JTextField();
	public JTextField txtEnvHumidityEffect = new JTextField();
	public JTextField txtEnvMoistureEffect = new JTextField();

	// constructor for the environment view
	public EnvironmentView() {
		this.setBorder(new EmptyBorder(10, 10, 10, 10));

		// add component to the environment panel
		JPanel envTempPanel = new JPanel();
		envTempPanel.setLayout(new GridLayout(2, 1));
		envTempPanel.add(lblEnvironmentTemperature);
		envTempPanel.add(txtEnvironmentTemperature);

		// create an environment humidity panel
		JPanel envHumidityPanel = new JPanel();
		envHumidityPanel.setLayout(new GridLayout(2, 1));
		envHumidityPanel.add(lblEnvironmentHumidity);
		envHumidityPanel.add(txtEnvironmentHumidity);

		// create an environment moisture panel
		JPanel envMoisturePanel = new JPanel();
		envMoisturePanel.setLayout(new GridLayout(2, 1));
		envMoisturePanel.add(lblEnvironmentMoisture);
		envMoisturePanel.add(txtEnvironmentMoisture);

		// create an environment temperature rate panel
		JPanel envTempRatePanel = new JPanel();
		envTempRatePanel.setLayout(new GridLayout(2, 1));
		envTempRatePanel.add(lblEnvTempEffect);
		envTempRatePanel.add(txtEnvTempEffect);

		// create an environment humidity rate panel
		JPanel envHumidityRatePanel = new JPanel();
		envHumidityRatePanel.setLayout(new GridLayout(2, 1));
		envHumidityRatePanel.add(lblEnvHumidityEffect);
		envHumidityRatePanel.add(txtEnvHumidityEffect);

		// create an environment moisture rate panel
		JPanel envMoistureRatePanel = new JPanel();
		envMoistureRatePanel.setLayout(new GridLayout(2, 1));
		envMoistureRatePanel.add(lblEnvMoistureEffect);
		envMoistureRatePanel.add(txtEnvMoistureEffect);

		// add these panel to environment view
		this.setLayout(new GridLayout(7, 1));
		this.add(envHumidityPanel);
		this.add(envTempPanel);
		this.add(envMoisturePanel);
		this.add(envHumidityRatePanel);
		this.add(envTempRatePanel);
		this.add(envMoistureRatePanel);
	}
}
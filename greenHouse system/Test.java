package greenHouse;

import java.awt.Component;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import java.io.*;
import java.util.Arrays;

/**
 * This the test class
 * @author yihe
 *
 */
public class Test extends JFrame {
	
	// create three button 
	public static JButton startButton = new JButton("Start");
	public static JButton stopButton = new JButton("Stop");
	
	// create four class object
	public static HumidityView humidityView = new HumidityView();
	public static TempView tempView = new TempView();
	public static MoistureView moistureView = new MoistureView();
	public static EnvironmentView environmentView = new EnvironmentView();
	
	// saving file 
	public static PrintWriter outFile;
	
	// constructor for test 
	public Test() throws IOException {
		this.setTitle(" GREENHOUSE ");
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setSize(1100, 500);
		this.setLayout(new GridLayout(1, 5));		
		
		// create panel to add button
		JPanel buttonsPanel = new JPanel();
		buttonsPanel.setLayout(new GridLayout(2, 1));
		buttonsPanel.add(startButton);
		buttonsPanel.add(stopButton);
		
		// add panel of humidity view, temp view, moisture view, environment view and button to JFrame 
		this.add(buttonsPanel);
		this.add(humidityView);
		this.add(tempView);
		this.add(moistureView);
		this.add(environmentView);
		
		// create outFile
		this.outFile = new PrintWriter(new FileWriter("sample.txt"));
		
		// get the file form temp, humidity, moisture and environment controller 
		TempController.setWriter(outFile);
		HumidityController.setWriter(outFile);
		MoistureController.setWriter(outFile);
		EnvironmentController.setWriter(outFile);
		
	}

		
	public static void main(String[] args) throws IOException {
		
		// This is the main method to start the program 
		Test simulator = new Test();
		simulator.setVisible(true);

		TempModel tempModel = new TempModel();
		TempController tempController = new TempController(tempView, tempModel);

		HumidityModel humidityModel = new HumidityModel();
		HumidityController humidityController = new HumidityController(humidityView, humidityModel);

		MoistureModel moistureModel = new MoistureModel();
		MoistureController moistureController = new MoistureController(moistureView, moistureModel);

		EnvironmentModel environmentModel = new EnvironmentModel();
		EnvironmentController environmentController = new EnvironmentController(environmentView, environmentModel,
			
				tempModel, humidityModel, moistureModel, tempView, humidityView, moistureView);
		
		
		// button listener to start the program.
		ActionListener startButtonListener = new ActionListener() {
			public void actionPerformed(ActionEvent e) {	

				humidityController.start();
				tempController.start();
				moistureController.start();
				environmentController.start();
			}
		};
		
		// button listener to stop the program
		ActionListener stopButtonListener = new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				humidityController.interrupt();
				tempController.interrupt();
				moistureController.interrupt();
				environmentController.interrupt();
				outFile.close();
			}
		};
		
	
		// use start button and stop button to start the program and stop the program
		startButton.addActionListener(startButtonListener);
		stopButton.addActionListener(stopButtonListener);
	}
}

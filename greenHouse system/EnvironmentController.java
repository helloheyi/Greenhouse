package greenHouse;

import java.io.PrintWriter;

/**
 * The class is the environment controller
 * 
 * @author yihe 
 *
 */
public class EnvironmentController extends Thread {
	public EnvironmentView environmentView;
	public EnvironmentModel environmentModel;
	public TempModel tempModel;
	public HumidityModel humidityModel;
	public MoistureModel moistureModel;
	public TempView tempView;
	public HumidityView humidityView;
	public MoistureView moistureView;
	public static PrintWriter outfile;

	/**
	 * This is class method to set the out file
	 * 
	 * @param outFile
	 *            saving file for UI on environment View
	 */
	public static void setWriter(PrintWriter outFile) {
		EnvironmentController.outfile = outFile;
	}
	
	/**
	 * The constructor can link the TempView class,TempModel class,MoistureView class, MoistureModel class, HumidityView class
	 * HumidityModel class, EnvironmentView class, EnvironmentModel class
	 * @param environmentView
	 *  This is the class of environment view
	 * @param environmentModel
	 * This is the class of environment model
	 * @param tempModel
	 *   This is the class of temperature model
	 * @param humidityModel
	 * This is the class of humidity view
	 * @param moistureModel
	 *   This is the class of moisture model
	 * @param tempView
	 *  This is the class of temperature view
	 * @param humidityView
	 * This is the class of humidity model
	 * @param moistureView
	 *  This is the class of moisture view
	 */
	public EnvironmentController(EnvironmentView environmentView, EnvironmentModel environmentModel,
			TempModel tempModel, HumidityModel humidityModel, MoistureModel moistureModel, TempView tempView,
			HumidityView humidityView, MoistureView moistureView)
	{
		this.environmentView = environmentView;
		this.tempView = tempView;
		this.humidityView = humidityView;
		this.moistureView = moistureView;
		this.environmentModel = environmentModel;
		this.tempModel = tempModel;
		this.humidityModel = humidityModel;
		this.moistureModel = moistureModel;

		// Set the three models into environment model, so that environment
		// controller can directly modify
		// temperature in tempModel, humidity in humidityModel, and moisture in
		// moistureModel.
		this.environmentModel.setModels(tempModel, humidityModel, moistureModel);
	}

	public void run() {
		while (!Thread.interrupted()) {
			try {
				
				// save input to model
				environmentModel.setTemperature(stringToDouble(environmentView.txtEnvironmentTemperature.getText()));
				environmentModel.setHumidity(stringToDouble(environmentView.txtEnvironmentHumidity.getText()));
				environmentModel.setMoisture(stringToDouble(environmentView.txtEnvironmentMoisture.getText()));
				environmentModel.setTempRate(stringToDouble(environmentView.txtEnvTempEffect.getText()));
				environmentModel.setHumidityRate(stringToDouble(environmentView.txtEnvHumidityEffect.getText()));
				environmentModel.setMoistureRate(stringToDouble(environmentView.txtEnvMoistureEffect.getText()));

				// calculate new temperature, output to UI
				environmentModel.updateTemperature();
				//// calculate new moisture , output to UI
				environmentModel.updateMoisture();
				// calculate new humidity , output to UI
				environmentModel.updateHumidity();
				
				// saving the file from UI
				outfile.print(" Environment Humidity: "+environmentView.txtEnvironmentHumidity.getText() + " "
						+ " Environment Temperature: "+environmentView.txtEnvironmentTemperature.getText() + " "
						+ " Environment Moisture: "+environmentView.txtEnvironmentMoisture.getText() + " "
						+ " Environment Humidity Effect: "+environmentView.txtEnvHumidityEffect.getText() + " "
						+ " Environment Temperature Effect: "+environmentView.txtEnvTempEffect.getText() + " "
						+ " Environment Moisture Effect: "+environmentView.txtEnvMoistureEffect.getText() + " \n"
						);
				
				//wait for user-specified time interval
				Thread.sleep((int) environmentModel.refreshRate * 1000);
			} catch (InterruptedException e) {
				Thread.currentThread().interrupt();
			}
		}
	}

	/**
	 * Method to change String to double
	 * 
	 * @param stringToParse
	 *            This is the String Object
	 * @return double value
	 */

	public static double stringToDouble(String stringToParse) {
		return Double.parseDouble(stringToParse);
	}
}

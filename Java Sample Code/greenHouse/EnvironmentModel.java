package greenHouse;

/**
 * This is the class environment model
 * 
 * @author xinyin yihe
 *
 */
public class EnvironmentModel {
	protected double envTemp;
	protected double envHumidity;
	protected double envMoisture;
	protected double envTempRate;
	protected double envHumidityRate;
	protected double envMoistureRate;
	protected double refreshRate = 1;
	protected TempModel tempModel;
	protected HumidityModel humidityModel;
	protected MoistureModel moistureModel;

	/**
	 * This method is to set the temperature model, humidity model and moisture model
	 * to environment model
	 * 
	 * @param tempModel
	 *            this is the temperature model
	 * @param humidityModel
	 *            this is the humidity model
	 * @param moistureModel
	 *            this is the moisture model
	 */
	public void setModels(TempModel tempModel, HumidityModel humidityModel, MoistureModel moistureModel) {
		this.tempModel = tempModel;
		this.humidityModel = humidityModel;
		this.moistureModel = moistureModel;
	}
	
	/**
	 * This method is to set the environment temperature rate 
	 * @param envTempRate
	 * the value of environment temperature rate 
	 */
	public void setTempRate(double envTempRate) {
		this.envTempRate = envTempRate;
	}
	
	/**
	 * This method is to get the environment temperature rate 
	 * @return environment temperature rate 
	 * the value of environment temperature rate 
	 */
	public double getTempRate() {
		return this.envTempRate;
	}
	
	/**
	 * This method is to set the environment humidity rate 
	 * @param envHumidityRate
	 * the value of environment humidity rate 
	 */
	public void setHumidityRate(double envHumidityRate) {
		this.envHumidityRate = envHumidityRate;
	}
	
	/**
	 * This method is to get the environment humidity rate 
	 * @return environment humidity rate 
	 * the value of environment humidity rate 
	 */
	public double getHumidityRate() {
		return this.envHumidityRate;
	}
	
	/**
	 * This method is to set the environment moisture rate 
	 * @param envMoistureRate
	 * the value of environment moisture rate 
	 */
	public void setMoistureRate(double envMoistureRate) {
		this.envMoistureRate = envMoistureRate;
	}
	
	/**
	 * This method is to get the environment moisture rate 
	 * @return environment moisture rate 
	 * the value of environment moisture rate 
	 */
	public double getMoistureRate() {
		return this.envMoistureRate;
	}
	
	/**
	 * This method is to set the refresh rate 
	 * @param refreshRate
	 * the value of refresh rate
	 */
	public void setRefreshRate(double refreshRate) {
		this.refreshRate = refreshRate;
	}
	
	/**
	 * This method is to get the refresh rate 
	 * @param refreshRate
	 * the value of refresh rate
	 * @return
	 * return the value of refresh rate
	 */
	public double getEnRefresh() {
		return this.refreshRate;
	}

	/**
	 * This method allow to set the environment initial temperature.
	 * 
	 * @param outTempValue
	 *            that is a value of environment temperature which is the
	 *            temperature be approached while the devices shut down.
	 * 
	 */
	public void setTemperature(double outTempValue) {
		this.envTemp = outTempValue;
	}

	/**
	 * This method will return a value of environment initial temperature.
	 * 
	 * @return outTempValue which is environment initial temperature.
	 */
	public double getOutTempValue() {
		return envTemp;
	}

	/**
	 * This method allow to set the environment humidity.
	 * 
	 * @param outHumValue
	 *            which is the environment humidity.
	 */
	public void setHumidity(double outHumValue) {
		this.envHumidity = outHumValue;
	}

	/**
	 * This method will return a value of environment humidity.
	 * 
	 * @return outHunValue which is environment humidity.
	 */
	public double getOutHumValue() {
		return envHumidity;
	}

	/**
	 * This method allow to set the soil moisture of environment.
	 * 
	 * @param outMosValue
	 *            which is the soil moisture of environment.
	 */
	public void setMoisture(double outMosValue) {
		this.envMoisture = outMosValue;
	}

	/**
	 * This method will return a value of soil moisture of environment.
	 * 
	 * @return outMosValue which is the soil moisture of environment.
	 */
	public double getOutMosValue() {
		return envMoisture;
	}
	
	/**
	 * The method is to get the update temperature
	 * current temperature + envTempRate * refreshRate
	 * current temperature - envTempRate * refreshRate
	 */
	public synchronized void updateTemperature() {
		if (envTemp < tempModel.getCurrentTemp()) {
			tempModel.changeCurrentTemp(-envTempRate * refreshRate);
		} else if (envTemp > tempModel.getCurrentTemp()) {
			tempModel.changeCurrentTemp(envTempRate * refreshRate);
		}
	}
	
	/**
	 * The method is to get the update humidity
	 * current humidity + envHumidityRate * refreshRate
	 * current humidity - envHumidityRate * refreshRate
	 */
	public synchronized void updateHumidity() {
		if (envHumidity < humidityModel.getCurrentHumidity()) {
			humidityModel.changeCurrentHumidity(-envHumidityRate * refreshRate);
		}

		else if (envHumidity > humidityModel.getCurrentHumidity()) {
			humidityModel.changeCurrentHumidity(envHumidityRate * refreshRate);
		}
	}

	/**
	 * The method is to get the update moisture
	 * current moisture + envMoistureRate * refreshRate
	 * current moisture -envMoistureRate * refreshRate
	 */
	public synchronized void updateMoisture() {
		if (envMoisture < moistureModel.getCurrentSoilMoisture()) {
			moistureModel.changeCurrentMoisture(-envMoistureRate * refreshRate);
		} else if (envMoisture > moistureModel.getCurrentSoilMoisture()) {
			moistureModel.changeCurrentMoisture(envMoistureRate * refreshRate);
		}
	}
}
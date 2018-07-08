package greenHouse;

/**
 * The class of the humidity model
 * 
 * @author yihe
 *
 */
public class HumidityModel {
	protected double currentHumidity;
	protected double desiredHumidityMax;
	protected double desiredHumidityMin;
	protected double humidityRate;
	protected String humidifierStatus = "";
	protected double refreshRate;

	/**
	 * This method is designed for setting a value of current humidity.
	 * 
	 */
	public synchronized void setCurrentHumidity(double curHum) {
		this.currentHumidity = curHum;
	}

	/**
	 * This method is designed for setting a value of changed humidity
	 * 
	 * @param deltaHum
	 *            the value of changed humidity
	 */
	public synchronized void changeCurrentHumidity(double deltaHum) {
		this.currentHumidity += deltaHum;
	}

	/**
	 * This method will return a value of current humidity once it is invoked.
	 * 
	 * @return curHum that is a value of current humidity
	 * 
	 */
	public synchronized double getCurrentHumidity() {
		return currentHumidity;
	}

	/**
	 * This method is designed for setting a value of desired maximum humidity.
	 */
	public void setDesiredHumidityMax(double desiredHumidityMax) {
		this.desiredHumidityMax = desiredHumidityMax;
	}

	/**
	 * This method will return a value of desired maximum humidity once it is
	 * invoked.
	 * 
	 * @return desMaxHum that us a value of desired maximum humidity.
	 *
	 */
	public double getDesiredHumidityMax() {
		return this.desiredHumidityMax;
	}

	/**
	 * This method is designed for setting a value of desired minimum humidity.
	 */
	public void setDesiredHumidityMin(double desiredHumidityMin) {
		this.desiredHumidityMin = desiredHumidityMin;
	}

	/**
	 * This method will return a value of desired minimum humidity once it is
	 * invoked.
	 * 
	 * @return desMinHum that is a value of desired minimum humidity.
	 * 
	 */
	public double getDesiredMinHumidity() {
		return this.desiredHumidityMin;
	}

	/**
	 * This method is designed for setting a value of humidity change rate.
	 */
	public void setHumidityRate(double humidityRate) {
		this.humidityRate = humidityRate;
	}

	/**
	 * This method will return a value of humidity change rate once it is
	 * invoked.
	 * 
	 * @return humChRate that is a value of humidity change rate.
	 * 
	 */
	public double getHumidityRate() {
		return this.humidityRate;
	}

	/**
	 * This method is designed for setting a value of humidifier refresh rate.
	 */
	public void setRefreshRate(double refreshRate) {
		this.refreshRate = refreshRate;
	}

	/**
	 * This method will return a value of humidity refresh rate once it is
	 * invoked.
	 * 
	 * @return hRefreahRate that is a value of humidity refresh rate.
	 */
	public double getRefreshRate() {
		return this.refreshRate;
	}

	/**
	 * Once the desired maximum and minimum humidity is known, the status of
	 * humidifier would be return.
	 * 
	 * @return humStatus that is the status of humidifier.
	 * 
	 */
	public String getHumidiferStatus() {
		if (currentHumidity < desiredHumidityMin) {
			humidifierStatus = "Humidifier ON";
		} else
			humidifierStatus = "Humidifier OFF";
		return this.humidifierStatus;
	}

	/**
	 * This method will get a value according to the humidity change rate and
	 * humidity refresh rate.
	 * 
	 */
	public synchronized void updateHumidity() {
		if (this.getCurrentHumidity() < desiredHumidityMin) {
			this.changeCurrentHumidity(humidityRate * (refreshRate));

		}
	}
}
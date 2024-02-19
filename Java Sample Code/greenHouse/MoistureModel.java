package greenHouse;

/**
 * This is the moisture model class
 * 
 * @author xinyin yihe
 *
 */
public class MoistureModel {
	protected double curMos;
	protected double desMaxMos;
	protected double desMinMos;
	protected double mosChRate;
	protected String mosStatus = "";
	protected double mosRefreshRate;

	/**
	 * This is the method to set the current soil moisture
	 * 
	 * @param curMos
	 *            this is the value of current soil moisture
	 */
	public synchronized void setCurrentSoilMoisture(double curMos) {
		this.curMos = curMos;
	}

	/**
	 * This is the method to set the changed soil moisture
	 * 
	 * @param deltaMOi
	 *            this is the value of changed soil moisture ( current soil
	 *            moisture + delta soil moisture)
	 */
	public synchronized void changeCurrentMoisture(double deltaMOi) {
		this.curMos += deltaMOi;
	}

	/**
	 * This method will return a value of current soil moisture
	 * 
	 * @return curMos that is a value of current soil moisture .
	 * 
	 */
	public synchronized double getCurrentSoilMoisture() {
		return curMos;
	}

	/**
	 * This method will set a value of desired maximum soil moisture once it is
	 * invoked.
	 * 
	 * @param desMaxMos
	 *            that is a value of desired maximum soil moisture.
	 * 
	 */
	public void setDesiredMaxSoilMoisture(double desMaxMos) {
		this.desMaxMos = desMaxMos;
	}

	/**
	 * This method will return a value of desired maximum soil moisture once it
	 * is invoked.
	 * 
	 * @return desMaxMos that is a value of desired maximum soil moisture.
	 * 
	 */
	public double getDesiredMaxSoilMoisture() {
		return desMaxMos;
	}

	/**
	 * This method allow to set a value for desired minimum soil moisture.
	 * 
	 * @param desMinMos
	 *            that is desired minimum soil moisture.
	 */
	public void setDesiredMinSoilMoisture(double desMinMos) {
		this.desMinMos = desMinMos;
	}

	/**
	 * This method will return a value of desired minimum soil moisture once it
	 * is invoked.
	 * 
	 * @return desMinMos that is desired minimum soil moisture.
	 */
	public double getDesiredMinSoilMoisture() {
		return desMinMos;
	}

	/**
	 * This method allow to set a value for soil moisture.
	 * 
	 * @param mosChRate
	 *            that is soil moisture change rate.
	 */
	public void setSoilMoistureChangeRate(double mosChRate) {
		this.mosChRate = mosChRate;
	}

	/**
	 * This method will return a value of soil moisture change rate once it is
	 * invoked.
	 * 
	 * @return mosChRate that is soil moisture change rate.
	 */
	public double getSoilMositureChangeRate() {
		return mosChRate;
	}

	/**
	 * This method allow to set a value for soil moisture refresh rate.
	 * 
	 * @param mosRefreshRate
	 *            that is soil moisture refresh rate.
	 */
	public void setMosRefreshRate(double mosRefreshRate) {
		this.mosRefreshRate = mosRefreshRate;
	}

	/**
	 * This method will return a value of soil moisture refresh rate.
	 * 
	 * @return mosRefreshRate that is soil moisture refresh rate.
	 */
	public double getMosRefreshRate() {
		return mosRefreshRate;
	}

	/**
	 * This method will return a string which represents the status of
	 * sprinkler.
	 * 
	 * @return mosStatus that is the status of sprinkler.
	 */
	public String getSprinklerStatus() {
		if (curMos < desMinMos) {
			mosStatus = "Sprinkler ON";
		}

		else
			mosStatus = "Sprinkler OFF";
		return mosStatus;
	}

	/**
	 * This method will get a value of changed soil moisture once it is invoked.
	 */
	public synchronized void updateMoisture() {
		if (this.getCurrentSoilMoisture() < desMinMos) {
			this.changeCurrentMoisture(mosChRate * (mosRefreshRate));
		}

	}

}
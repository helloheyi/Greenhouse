package edu.gatech.seclass.jobcompare6300.model;

import java.io.Serializable;

public class OfferDetail implements Serializable{
    String title;
    String name;
    private Location location;
    private float salary;
    private float bonus;
    private int stockOptions;
    private Benefits benefits;

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Location getLocation() {
        return location;
    }

    public void setLocation(Location location) {
        this.location = location;
    }

    public float getSalary() {
        return salary;
    }

    public void setSalary(float salary) {
        this.salary = salary;
    }

    public float getBonus() {
        return bonus;
    }

    public void setBonus(float bonus) {
        this.bonus = bonus;
    }
    public int getStockOptions() {
        return stockOptions;
    }

    public void setStockOptions(int stockOptions) {
        this.stockOptions = stockOptions;
    }

    public Benefits getBenefits() {
        return benefits;
    }

    public void setBenefits(Benefits benefits) {
        this.benefits = benefits;
    }

    public float getAYS() {
        return this.salary / this.location.costOfLiving * 100;
    }

    public float getAYB() {
        return this.bonus / this.location.costOfLiving * 100;
    }

    public boolean addLocation(String city, String state, float costIndex) {
        this.location = new Location();
        if (location != null) {
            location.city = city;
            location.state = state;
            location.costOfLiving = costIndex;
            return true;
        } else {
            return false;
        }
    }

    public boolean editLocation(String city, String state, float costIndex) {
        if (location != null) {
            location.city = city;
            location.state = state;
            location.costOfLiving = costIndex;
            return true;
        } else {
            return false;
        }
    }

    public boolean addBenefits(float homeFund, float holiday, float internet) {
        this.benefits = new Benefits();
        if(benefits != null) {
            benefits.setHomeProgramFund(homeFund);
            benefits.setHolidays(holiday);
            benefits.setInternetStipend(internet);
            return true;
        } else {
            return false;
        }
    }

    public boolean editBenefits(float homeFund, float holiday, float internet) {
        if(benefits != null) {
            benefits.setHomeProgramFund(homeFund);
            benefits.setHolidays(holiday);
            benefits.setInternetStipend(internet);
            return true;
        } else {
            return false;
        }
    }
}
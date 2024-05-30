package edu.gatech.seclass.jobcompare6300.database;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.BaseColumns;

import androidx.annotation.Nullable;

public class DBHelper extends SQLiteOpenHelper {

    public static final String DATABASE_NAME = "OfferDetail.db";
    public static final int DATABASE_VERSION = 2;

    private static final String SQL_CREATE_ENTRIES =
            "CREATE TABLE " + OffersEntry.TABLE_NAME + " (" +
                    OffersEntry._ID + " INTEGER PRIMARY KEY," +
                    OffersEntry.COLUMN_NAME_IS_JOB + " INTEGER," +
                    OffersEntry.COLUMN_NAME_TITLE + " TEXT," +
                    OffersEntry.COLUMN_NAME_COMPANY_NAME + " TEXT," +
                    OffersEntry.COLUMN_NAME_CITY + " TEXT," +
                    OffersEntry.COLUMN_NAME_STATE + " TEXT," +
                    OffersEntry.COLUMN_NAME_COST_OF_LIVING + " INTEGER," +
                    OffersEntry.COLUMN_NAME_YEARLY_SALARY + " REAL," +
                    OffersEntry.COLUMN_NAME_YEARLY_BONUS + " REAL," +
                    OffersEntry.COLUMN_NAME_NUMBER_OF_STOCK + " REAL," +
                    OffersEntry.COLUMN_NAME_HOME_FUND + " REAL," +
                    OffersEntry.COLUMN_NAME_HOLIDAYS + " REAL," +
                    OffersEntry.COLUMN_NAME_INTERNET_STIPEND + " REAL)"
            ;

    public DBHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(SQL_CREATE_ENTRIES);
        db.execSQL(SQL_CREATE_JOB_WEIGHT_SETTINGS);
    }
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }

    public static class OffersEntry implements BaseColumns {
        public static final String TABLE_NAME = "offersEntry";
        public static final String COLUMN_NAME_IS_JOB = "is_job";
        public static final String COLUMN_NAME_TITLE = "title";
        public static final String COLUMN_NAME_COMPANY_NAME = "company";
        public static final String COLUMN_NAME_CITY = "city";
        public static final String COLUMN_NAME_STATE = "state";
        public static final String COLUMN_NAME_COST_OF_LIVING = "costOfLiving";
        public static final String COLUMN_NAME_YEARLY_SALARY = "yearlySalary";
        public static final String COLUMN_NAME_YEARLY_BONUS = "yearlyBonus";
        public static final String COLUMN_NAME_NUMBER_OF_STOCK = "numberOfStock";
        public static final String COLUMN_NAME_HOME_FUND = "HomeFund";
        public static final String COLUMN_NAME_HOLIDAYS = "Holidays";
        public static final String COLUMN_NAME_INTERNET_STIPEND = "InternetStipend";
    }



    // create a table for weight setting
    public static final String SQL_CREATE_JOB_WEIGHT_SETTINGS =
            "CREATE TABLE " + JobWeightSettingsEntry.TABLE_NAME + " (" +
                    JobWeightSettingsEntry._ID + " INTEGER PRIMARY KEY," +
                    JobWeightSettingsEntry.COLUMN_NAME_AYS + " INTEGER," +
                    JobWeightSettingsEntry.COLUMN_NAME_AYB + " INTEGER," +
                    JobWeightSettingsEntry.COLUMN_NAME_CSO + " INTEGER," +
                    JobWeightSettingsEntry.COLUMN_NAME_HBP + " INTEGER," +
                    JobWeightSettingsEntry.COLUMN_NAME_PCH + " INTEGER," +
                    JobWeightSettingsEntry.COLUMN_NAME_MIS + " INTEGER" +
                    ")";



    public static class JobWeightSettingsEntry implements BaseColumns {
        public static final String TABLE_NAME = "job_weight_settings";
        public static final String COLUMN_NAME_AYS = "ays";
        public static final String COLUMN_NAME_AYB = "ayb";
        public static final String COLUMN_NAME_CSO = "cso";
        public static final String COLUMN_NAME_HBP = "hbp";
        public static final String COLUMN_NAME_PCH = "pch";
        public static final String COLUMN_NAME_MIS = "mis";

    }



}
